#!/usr/bin/env python3
"""
PAPER·QUANT bot — laboratorio de estrategias de paper trading (educativo).

Corre continuamente sin navegador, guarda su estado y registra cada operación.
Incluye varias estrategias clásicas y un modo comparación que las enfrenta
sobre los mismos precios, con comisiones y slippage realistas.

Modos:
  python3 paper_bot.py                        estrategia ema con precios reales
  python3 paper_bot.py --sim                  precios simulados (sin internet)
  python3 paper_bot.py --strategy rsi         elegir estrategia (ema/rsi/breakout/random)
  python3 paper_bot.py --compare --sim        torneo: todas a la vez + referencia buy&hold
  python3 paper_bot.py --no-fees              desactivar costes (solo para comparar su efecto)

IMPORTANTE: todo el dinero es ficticio. Ninguna orden es real y nada de esto
predice ganancias reales. No existe el bot que "gana dinero garantizado".
"""

import argparse
import csv
import json
import math
import os
import random
import signal
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

START_CASH = 10_000.0
RISK_PCT = 0.01          # 1% del capital en juego por operación (1R)
STOP_SIGMAS = 6          # stop a 6 sigmas de la entrada
TP_R = 1.5               # take profit a +1.5R
MAX_HOLD = 120           # muestras máximas por posición
MAX_POSITIONS = 3

# costes realistas de un exchange minorista
FEE_SIDE = 0.0010        # 0.10% de comisión por lado (entrada y salida)
SLIPPAGE = 0.0002        # 0.02% de slippage/spread por lado

STRATEGIES = ("ema", "rsi", "breakout", "random")

SIM_VOL = {"BTC": 0.0009, "ETH": 0.0012, "SOL": 0.0016}
SIM_PX = {"BTC": 77_800.0, "ETH": 3_410.0, "SOL": 178.4}
BINANCE_SYMBOLS = {"BTCUSDT": "BTC", "ETHUSDT": "ETH", "SOLUSDT": "SOL"}
COINBASE_PAIRS = {"BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD"}
DONCHIAN = 40            # ventana del canal de ruptura


# ---------------------------------------------------------------- precios

def fetch_binance():
    q = urllib.parse.quote('["BTCUSDT","ETHUSDT","SOLUSDT"]')
    url = "https://api.binance.com/api/v3/ticker/price?symbols=" + q
    with urllib.request.urlopen(url, timeout=8) as r:
        rows = json.load(r)
    return {BINANCE_SYMBOLS[row["symbol"]]: float(row["price"])
            for row in rows if row["symbol"] in BINANCE_SYMBOLS}


def fetch_coinbase():
    out = {}
    for asset, pair in COINBASE_PAIRS.items():
        url = f"https://api.coinbase.com/v2/prices/{pair}/spot"
        with urllib.request.urlopen(url, timeout=8) as r:
            out[asset] = float(json.load(r)["data"]["amount"])
    return out


def fetch_prices():
    try:
        return fetch_binance(), "binance"
    except Exception:
        return fetch_coinbase(), "coinbase"


# ---------------------------------------------------------------- indicadores

def new_indicators(sim):
    return {
        k: {"px": SIM_PX[k], "prev": SIM_PX[k],
            "ema8": SIM_PX[k], "ema21": SIM_PX[k],
            "vol": SIM_VOL[k], "primed": sim,
            "rsi_g": 0.0, "rsi_l": 0.0, "rsi": 50.0,
            "window": [SIM_PX[k]]}
        for k in SIM_PX
    }


def update_indicators(ind, sim, prices):
    for k, a in ind.items():
        if sim:
            a["px"] *= math.exp(SIM_VOL[k] * random.gauss(0, 1))
        elif k in prices:
            a["px"] = prices[k]
            a["primed"] = True
        if not a["primed"]:
            continue
        r = math.log(a["px"] / a["prev"]) if a["prev"] else 0.0
        if not sim:
            a["vol"] = max(0.0002, math.sqrt(0.94 * a["vol"] ** 2 + 0.06 * r ** 2))
        d = a["px"] - a["prev"]
        a["prev"] = a["px"]
        a["ema8"] += (a["px"] - a["ema8"]) * 2 / 9
        a["ema21"] += (a["px"] - a["ema21"]) * 2 / 22
        # RSI de Wilder (14)
        a["rsi_g"] = (a["rsi_g"] * 13 + max(d, 0)) / 14
        a["rsi_l"] = (a["rsi_l"] * 13 + max(-d, 0)) / 14
        a["rsi"] = 100.0 if a["rsi_l"] == 0 else 100 - 100 / (1 + a["rsi_g"] / a["rsi_l"])
        a["window"].append(a["px"])
        if len(a["window"]) > DONCHIAN + 1:
            a["window"].pop(0)


# ---------------------------------------------------------------- estrategias

def entry_signal(name, a):
    """Devuelve 'LONG', 'SHORT' o None para el activo con indicadores a."""
    if name == "ema":
        spread = (a["ema8"] - a["ema21"]) / a["ema21"]
        thr = max(0.0002, a["vol"] * 1.5)
        conf = min(0.99, 0.48 + 0.12 * abs(spread) / thr + random.random() * 0.2)
        if abs(spread) > thr and conf > 0.55 and random.random() < 0.35:
            return "LONG" if spread > 0 else "SHORT"
    elif name == "rsi":
        if len(a["window"]) < 15:
            return None
        if a["rsi"] < 30:
            return "LONG"          # sobreventa: apuesta a rebote
        if a["rsi"] > 70:
            return "SHORT"         # sobrecompra: apuesta a recorte
    elif name == "breakout":
        w = a["window"]
        if len(w) <= DONCHIAN:
            return None
        prior = w[:-1]
        if a["px"] > max(prior):
            return "LONG"          # ruptura del máximo de 40 muestras
        if a["px"] < min(prior):
            return "SHORT"         # ruptura del mínimo
    elif name == "random":
        if random.random() < 0.02:  # el grupo de control: moneda al aire
            return random.choice(("LONG", "SHORT"))
    return None


def flip_signal(name, a, side):
    """True si la estrategia pide cerrar la posición por señal contraria."""
    if name == "ema":
        spread = a["ema8"] - a["ema21"]
        return (spread < 0) if side == "LONG" else (spread > 0)
    if name == "rsi":
        return (a["rsi"] >= 50) if side == "LONG" else (a["rsi"] <= 50)
    if name == "breakout":
        w = a["window"]
        if len(w) <= DONCHIAN:
            return False
        mid = (max(w[:-1]) + min(w[:-1])) / 2
        return (a["px"] < mid) if side == "LONG" else (a["px"] > mid)
    return False                    # random solo sale por stop/TP/tiempo


# ---------------------------------------------------------------- cartera

def new_portfolio(name):
    return {"name": name, "equity": START_CASH, "positions": [],
            "closed": 0, "wins": 0, "gross_win": 0.0, "gross_loss": 0.0,
            "fees_paid": 0.0}


def maybe_open(pf, ind, fees_on):
    if len(pf["positions"]) >= MAX_POSITIONS:
        return
    held = {p["asset"] for p in pf["positions"]}
    for k, a in ind.items():
        if k in held or not a["primed"]:
            continue
        side = entry_signal(pf["name"], a)
        if not side:
            continue
        risk_cash = pf["equity"] * RISK_PCT
        stop_dist = STOP_SIGMAS * a["vol"] * a["px"]
        size = risk_cash / stop_dist
        max_hold = random.randint(10, 30) if pf["name"] == "random" else MAX_HOLD
        pf["positions"].append({"asset": k, "side": side, "entry": a["px"],
                                "size": size, "stop_dist": stop_dist,
                                "held": 0, "max_hold": max_hold})


def maybe_close(pf, ind, fees_on, log, quiet):
    for p in list(pf["positions"]):
        a = ind[p["asset"]]
        p["held"] += 1
        sign = 1 if p["side"] == "LONG" else -1
        diff = (a["px"] - p["entry"]) * sign

        reason = None
        if diff <= -p["stop_dist"]:
            reason = "stop -1R"
        elif diff >= TP_R * p["stop_dist"]:
            reason = f"take-profit +{TP_R}R"
        elif p["held"] > 3 and flip_signal(pf["name"], a, p["side"]):
            reason = "señal invertida"
        elif p["held"] >= p["max_hold"]:
            reason = "tiempo máximo"
        if not reason:
            continue

        cost = (p["entry"] + a["px"]) * p["size"] * (FEE_SIDE + SLIPPAGE) if fees_on else 0.0
        pnl = diff * p["size"] - cost
        pf["equity"] += pnl
        pf["fees_paid"] += cost
        pf["closed"] += 1
        if pnl > 0:
            pf["wins"] += 1
            pf["gross_win"] += pnl
        else:
            pf["gross_loss"] += -pnl
        pf["positions"].remove(p)

        if log:
            log([time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), pf["name"],
                 p["asset"] + "USD", p["side"], f"{p['entry']:.2f}", f"{a['px']:.2f}",
                 f"{p['size']:.6f}", f"{pnl:.2f}", f"{cost:.2f}", reason,
                 f"{pf['equity']:.2f}"])
        if not quiet:
            tag = "GANA " if pnl > 0 else "PIERDE"
            print(f"[{tag}] {pf['name']:>8} {p['side']} {p['asset']}USD  "
                  f"{pnl:+,.2f} $ (costes {cost:.2f})  ({reason})  "
                  f"equity ${pf['equity']:,.2f}")


# ---------------------------------------------------------------- persistencia

def state_path(name):
    return os.path.join(HERE, f"state_{name}.json")


def load_portfolio(name, sim):
    path = state_path(name)
    if os.path.exists(path):
        try:
            with open(path) as f:
                data = json.load(f)
            if data.get("sim") == sim:
                print(f"[estado] retomando '{name}': equity ${data['pf']['equity']:,.2f}, "
                      f"{data['pf']['closed']} trades")
                return data["pf"], data.get("ind")
            print("[estado] el estado guardado es de otro modo (sim/real); empiezo de cero")
        except Exception as e:
            print(f"[estado] no se pudo leer {os.path.basename(path)} ({e}); empiezo de cero")
    return new_portfolio(name), None


def save_portfolio(pf, ind, sim):
    tmp = state_path(pf["name"]) + ".tmp"
    with open(tmp, "w") as f:
        json.dump({"pf": pf, "ind": ind, "sim": sim}, f)
    os.replace(tmp, state_path(pf["name"]))


def make_trade_logger():
    path = os.path.join(HERE, "trades.csv")
    def log(row):
        new = not os.path.exists(path)
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["utc", "estrategia", "mercado", "lado", "entrada",
                            "salida", "tamaño", "pnl", "costes", "motivo", "equity"])
            w.writerow(row)
    return log


# ---------------------------------------------------------------- informes

def profit_factor(pf):
    if pf["gross_loss"] == 0:
        return float("inf") if pf["gross_win"] else 0.0
    return pf["gross_win"] / pf["gross_loss"]


def compare_table(portfolios, hold_final):
    rows = [(pf["name"], pf["closed"],
             (pf["wins"] / pf["closed"] * 100) if pf["closed"] else 0.0,
             profit_factor(pf), pf["fees_paid"], pf["equity"])
            for pf in portfolios]
    rows.append(("buy&hold BTC", 1, 0.0, 0.0, 0.0, hold_final))
    rows.sort(key=lambda r: -r[5])
    out = ["", "  estrategia      trades   WR%     PF   costes($)   equity final",
          "  " + "-" * 62]
    for name, n, wr, pfac, fees, eq in rows:
        pnl = eq - START_CASH
        out.append(f"  {name:<14} {n:>6} {wr:>6.1f} {pfac:>6.2f} {fees:>10,.0f}"
                   f"   ${eq:>9,.2f} ({pnl:+,.0f})")
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- bucle

def main():
    ap = argparse.ArgumentParser(description="Laboratorio de paper trading (educativo)")
    ap.add_argument("--sim", action="store_true", help="precios simulados (sin internet)")
    ap.add_argument("--strategy", choices=STRATEGIES, default="ema",
                    help="estrategia a operar (por defecto: ema)")
    ap.add_argument("--compare", action="store_true",
                    help="torneo: todas las estrategias sobre los mismos precios")
    ap.add_argument("--no-fees", action="store_true",
                    help="desactivar comisiones y slippage")
    ap.add_argument("--interval", type=float, default=None,
                    help="segundos entre muestras (real: 5, sim: 0.75)")
    ap.add_argument("--max-ticks", type=int, default=0,
                    help="detenerse tras N muestras (0 = sin límite)")
    args = ap.parse_args()

    interval = args.interval if args.interval is not None else (0.75 if args.sim else 5.0)
    fees_on = not args.no_fees
    log = make_trade_logger()

    if args.compare:
        portfolios = [new_portfolio(n) for n in STRATEGIES]
        ind = new_indicators(args.sim)
    else:
        pf, saved_ind = load_portfolio(args.strategy, args.sim)
        portfolios = [pf]
        ind = saved_ind or new_indicators(args.sim)

    print("=" * 72)
    print("PAPER·QUANT bot — SIMULADOR EDUCATIVO, dinero 100% ficticio")
    modo = "torneo de estrategias" if args.compare else f"estrategia '{args.strategy}'"
    print(f"{modo} · {'precios simulados' if args.sim else 'precios reales (papel)'}"
          f" · costes {'ON (0.10% + slippage por lado)' if fees_on else 'OFF'}")
    print("Ctrl+C para detener" + ("" if args.compare else " (el estado se guarda y retoma)"))
    print("=" * 72)

    stop = {"flag": False}
    signal.signal(signal.SIGINT, lambda *_: stop.update(flag=True))
    signal.signal(signal.SIGTERM, lambda *_: stop.update(flag=True))

    hold_entry = None
    net_fails = 0
    ticks = 0
    while not stop["flag"]:
        source = "sim"
        prices = {}
        if not args.sim:
            try:
                prices, source = fetch_prices()
                net_fails = 0
            except Exception as e:
                net_fails += 1
                print(f"[red  ] sin precios ({e.__class__.__name__}); "
                      f"reintento {net_fails} en {interval}s")
                if net_fails >= 60:
                    print("[red  ] demasiados fallos seguidos; me detengo")
                    break
                time.sleep(interval)
                continue

        update_indicators(ind, args.sim, prices)
        if hold_entry is None and ind["BTC"]["primed"]:
            hold_entry = ind["BTC"]["px"]

        for pf in portfolios:
            maybe_open(pf, ind, fees_on)
            maybe_close(pf, ind, fees_on, log, quiet=args.compare)

        ticks += 1
        if ticks % 50 == 1:
            if args.compare:
                resumen = " · ".join(f"{p['name']} ${p['equity']:,.0f}" for p in portfolios)
                print(f"{time.strftime('%H:%M:%S')} [{source}] t={ticks}  {resumen}")
            else:
                pf = portfolios[0]
                pnl = pf["equity"] - START_CASH
                wr = pf["wins"] / pf["closed"] * 100 if pf["closed"] else 0
                print(f"{time.strftime('%H:%M:%S')} [{source}] equity ${pf['equity']:,.2f} "
                      f"({pnl:+,.2f}) · {pf['closed']} trades · WR {wr:.1f}% · "
                      f"abiertas {len(pf['positions'])}")
        if not args.compare and (ticks % 12 == 0 or portfolios[0]["positions"]):
            save_portfolio(portfolios[0], ind, args.sim)
        if args.max_ticks and ticks >= args.max_ticks:
            break
        time.sleep(interval)

    if not args.compare:
        save_portfolio(portfolios[0], ind, args.sim)

    hold_final = START_CASH
    if hold_entry:
        gross = START_CASH * ind["BTC"]["px"] / hold_entry
        hold_final = gross - (START_CASH + gross) * (FEE_SIDE + SLIPPAGE) if fees_on else gross

    print("-" * 72)
    print(compare_table(portfolios, hold_final))
    print("Recuerda: sobre un paseo aleatorio ninguna estrategia tiene ventaja, y con")
    print("costes, operar más = perder más. En mercados reales pasa parecido más veces")
    print("de las que cualquier vendedor de bots admite.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
