#!/usr/bin/env python3
"""
PAPER·QUANT bot — paper trading continuo (24/7), solo con dinero ficticio.

La misma estrategia del dashboard (cruce EMA 8/21 con riesgo del 1% por
operación), pero como proceso independiente: corre sin navegador, guarda su
estado en state.json (si lo detienes y lo relanzas, retoma donde iba) y
registra cada operación cerrada en trades.csv.

Modos:
  python3 paper_bot.py            precios reales (Binance REST, Coinbase de respaldo)
  python3 paper_bot.py --sim      precios simulados (paseo aleatorio), sin internet

Ninguna orden es real. Nunca se envía dinero a ningún sitio.
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
STATE_FILE = os.path.join(HERE, "state.json")
TRADES_FILE = os.path.join(HERE, "trades.csv")

START_CASH = 10_000.0
RISK_PCT = 0.01          # 1% del capital en juego por operación
STOP_SIGMAS = 6          # el stop se coloca a 6 sigmas del precio de entrada
TP_R = 1.5               # take profit a +1.5R (el stop es -1R)
MAX_HOLD = 120           # muestras máximas con una posición abierta
MAX_POSITIONS = 3

SIM_VOL = {"BTC": 0.0009, "ETH": 0.0012, "SOL": 0.0016}
SIM_PX = {"BTC": 77_800.0, "ETH": 3_410.0, "SOL": 178.4}
BINANCE_SYMBOLS = {"BTCUSDT": "BTC", "ETHUSDT": "ETH", "SOLUSDT": "SOL"}
COINBASE_PAIRS = {"BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD"}


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
    """Binance primero, Coinbase de respaldo. Lanza excepción si ambos fallan."""
    try:
        return fetch_binance(), "binance"
    except Exception:
        return fetch_coinbase(), "coinbase"


# ---------------------------------------------------------------- estado

def fresh_state(sim):
    return {
        "equity": START_CASH,
        "closed": 0,
        "wins": 0,
        "gross_win": 0.0,
        "gross_loss": 0.0,
        "positions": [],
        "assets": {
            k: {"px": SIM_PX[k], "prev": SIM_PX[k],
                "ema8": SIM_PX[k], "ema21": SIM_PX[k],
                "vol": SIM_VOL[k], "primed": sim}
            for k in SIM_PX
        },
        "sim": sim,
        "started": time.time(),
    }


def load_state(sim):
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                st = json.load(f)
            if st.get("sim") == sim:
                print(f"[estado] retomando sesión: equity ${st['equity']:,.2f}, "
                      f"{st['closed']} trades cerrados")
                return st
            print("[estado] el estado guardado es de otro modo (sim/real); empiezo de cero")
        except Exception as e:
            print(f"[estado] no se pudo leer state.json ({e}); empiezo de cero")
    return fresh_state(sim)


def save_state(st):
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(st, f, indent=1)
    os.replace(tmp, STATE_FILE)


def log_trade(row):
    new = not os.path.exists(TRADES_FILE)
    with open(TRADES_FILE, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["utc", "mercado", "lado", "entrada", "salida", "tamaño",
                        "pnl", "ret_pct", "motivo", "equity"])
        w.writerow(row)


# ---------------------------------------------------------------- estrategia

def update_prices(st, prices):
    for k, a in st["assets"].items():
        if st["sim"]:
            a["px"] *= math.exp(SIM_VOL[k] * random.gauss(0, 1))
        elif k in prices:
            a["px"] = prices[k]
            a["primed"] = True
        if not a["primed"]:
            continue
        r = math.log(a["px"] / a["prev"]) if a["prev"] else 0.0
        if not st["sim"]:
            a["vol"] = max(0.0002, math.sqrt(0.94 * a["vol"] ** 2 + 0.06 * r ** 2))
        a["prev"] = a["px"]
        a["ema8"] += (a["px"] - a["ema8"]) * 2 / 9
        a["ema21"] += (a["px"] - a["ema21"]) * 2 / 22


def maybe_open(st):
    if len(st["positions"]) >= MAX_POSITIONS:
        return
    held = {p["asset"] for p in st["positions"]}
    for k, a in st["assets"].items():
        if k in held or not a["primed"]:
            continue
        spread = (a["ema8"] - a["ema21"]) / a["ema21"]
        thr = 0.0006 if st["sim"] else max(0.0002, a["vol"] * 1.5)
        conf = min(0.99, 0.48 + 0.12 * abs(spread) / thr + random.random() * 0.2)
        if abs(spread) > thr and conf > 0.55 and random.random() < 0.35:
            side = "LONG" if spread > 0 else "SHORT"
            risk_cash = st["equity"] * RISK_PCT
            stop_dist = STOP_SIGMAS * a["vol"] * a["px"]
            size = risk_cash / stop_dist
            st["positions"].append({
                "asset": k, "side": side, "entry": a["px"], "size": size,
                "stop_dist": stop_dist, "held": 0, "opened": time.time(),
            })
            print(f"[abre ] {side} {k}USD @ {a['px']:,.2f}  "
                  f"tamaño {size:.4f}  conf {conf * 100:.0f}%  (papel)")


def maybe_close(st):
    for p in list(st["positions"]):
        a = st["assets"][p["asset"]]
        p["held"] += 1
        sign = 1 if p["side"] == "LONG" else -1
        diff = (a["px"] - p["entry"]) * sign
        spread = (a["ema8"] - a["ema21"]) / a["ema21"]
        flipped = (spread < 0) if p["side"] == "LONG" else (spread > 0)

        reason = None
        if diff <= -p["stop_dist"]:
            reason = "stop -1R"
        elif diff >= TP_R * p["stop_dist"]:
            reason = f"take-profit +{TP_R}R"
        elif flipped and p["held"] > 3:
            reason = "señal invertida"
        elif p["held"] >= MAX_HOLD:
            reason = "tiempo máximo"
        if not reason:
            continue

        pnl = diff * p["size"]
        st["equity"] += pnl
        st["closed"] += 1
        if pnl > 0:
            st["wins"] += 1
            st["gross_win"] += pnl
        else:
            st["gross_loss"] += -pnl
        st["positions"].remove(p)
        ret = pnl / st["equity"] * 100
        log_trade([time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   p["asset"] + "USD", p["side"], f"{p['entry']:.2f}",
                   f"{a['px']:.2f}", f"{p['size']:.6f}", f"{pnl:.2f}",
                   f"{ret:.3f}", reason, f"{st['equity']:.2f}"])
        tag = "GANA " if pnl > 0 else "PIERDE"
        print(f"[{tag}] {p['side']} {p['asset']}USD  {pnl:+,.2f} $  ({reason})  "
              f"equity ${st['equity']:,.2f}")


def status_line(st, source):
    pnl = st["equity"] - START_CASH
    wr = st["wins"] / st["closed"] * 100 if st["closed"] else 0
    px = "  ".join(f"{k} {a['px']:,.0f}" if a["px"] >= 1000 else f"{k} {a['px']:,.2f}"
                   for k, a in st["assets"].items())
    return (f"{time.strftime('%H:%M:%S')} [{source}] equity ${st['equity']:,.2f} "
            f"({pnl:+,.2f}) · {st['closed']} trades · WR {wr:.1f}% · "
            f"abiertas {len(st['positions'])} · {px}")


# ---------------------------------------------------------------- bucle

def main():
    ap = argparse.ArgumentParser(description="Bot de paper trading continuo (educativo)")
    ap.add_argument("--sim", action="store_true",
                    help="precios simulados (sin internet)")
    ap.add_argument("--interval", type=float, default=None,
                    help="segundos entre muestras (real: 5, sim: 0.75)")
    ap.add_argument("--max-ticks", type=int, default=0,
                    help="detenerse tras N muestras (0 = sin límite)")
    args = ap.parse_args()

    interval = args.interval if args.interval is not None else (0.75 if args.sim else 5.0)
    st = load_state(args.sim)

    print("=" * 72)
    print("PAPER·QUANT bot — SIMULADOR EDUCATIVO, dinero 100% ficticio")
    print(f"modo: {'precios simulados' if args.sim else 'precios reales (órdenes de papel)'}"
          f" · muestra cada {interval}s · estado en {os.path.basename(STATE_FILE)}")
    print("Ctrl+C para detener (el estado queda guardado y se retoma al relanzar)")
    print("=" * 72)

    stop = {"flag": False}
    signal.signal(signal.SIGINT, lambda *_: stop.update(flag=True))
    signal.signal(signal.SIGTERM, lambda *_: stop.update(flag=True))

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
                    print("[red  ] demasiados fallos seguidos; me detengo con el estado a salvo")
                    break
                time.sleep(interval)
                continue

        update_prices(st, prices)
        maybe_open(st)
        maybe_close(st)
        ticks += 1
        if ticks % 12 == 1:
            print(status_line(st, source))
        if ticks % 12 == 0 or st["positions"]:
            save_state(st)
        if args.max_ticks and ticks >= args.max_ticks:
            break
        time.sleep(interval)

    save_state(st)
    pnl = st["equity"] - START_CASH
    pf = (st["gross_win"] / st["gross_loss"]) if st["gross_loss"] else float("inf")
    print("-" * 72)
    print(f"sesión guardada · equity ${st['equity']:,.2f} ({pnl:+,.2f}) · "
          f"{st['closed']} trades · factor de beneficio {pf:.2f}")
    print(f"historial: {TRADES_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
