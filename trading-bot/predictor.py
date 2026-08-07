#!/usr/bin/env python3
"""
Experimento: ¿se puede predecir si BTC sube o baja en los próximos 5 minutos?

Método honesto, el mismo que usaría (en versión sencilla) un quant de verdad:

  1. Descarga velas reales de 5 minutos de BTC/USDT (Binance, API pública).
  2. Construye features con lo conocido HASTA cada vela (nunca del futuro).
  3. Entrena una regresión logística SOLO con el primer 70% (pasado).
  4. Evalúa en el 30% final (futuro no visto): precisión y, sobre todo,
     si el acierto extra bastaría para pagar comisiones y spread.
  5. Compara contra dos referencias: "siempre sube" y "repite la última vela".

Uso:
  python3 predictor.py                  velas reales (necesita internet)
  python3 predictor.py --days 30        más historia (por defecto 14 días)
  python3 predictor.py --sim            velas sintéticas (paseo aleatorio)

Sin dependencias: solo Python 3 estándar. Educativo: no ejecuta ni una orden.
"""

import argparse
import json
import math
import random
import sys
import time
import urllib.request

FEE_SIDE = 0.0010          # 0.10% por lado
SLIPPAGE = 0.0002          # 0.02% por lado
ROUND_TRIP = 2 * (FEE_SIDE + SLIPPAGE)   # coste total ida y vuelta (~0.24%)


# ---------------------------------------------------------------- datos

def fetch_klines(days):
    """Velas 5m de BTCUSDT desde Binance, en bloques de 1000."""
    need = days * 24 * 12
    closes = []
    end = int(time.time() * 1000)
    while len(closes) < need:
        n = min(1000, need - len(closes))
        url = ("https://api.binance.com/api/v3/klines"
               f"?symbol=BTCUSDT&interval=5m&limit={n}&endTime={end}")
        with urllib.request.urlopen(url, timeout=15) as r:
            rows = json.load(r)
        if not rows:
            break
        closes = [float(row[4]) for row in rows] + closes
        end = rows[0][0] - 1
        print(f"[datos] {len(closes)}/{need} velas descargadas…")
    return closes


def sim_klines(days):
    """Velas sintéticas: paseo aleatorio con la volatilidad típica de BTC 5m."""
    n = days * 24 * 12
    px, out = 77_800.0, []
    for _ in range(n):
        px *= math.exp(0.0012 * random.gauss(0, 1))
        out.append(px)
    return out


# ---------------------------------------------------------------- features

def build_dataset(closes):
    """X, y: features en la vela t → ¿la vela t+1 cierra arriba?"""
    rets = [0.0] + [math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes))]
    X, y = [], []
    for t in range(40, len(closes) - 1):
        window = rets[t - 19:t + 1]
        mu = sum(window) / len(window)
        vol = math.sqrt(sum((r - mu) ** 2 for r in window) / len(window)) or 1e-9
        # RSI(14)
        gains = [max(r, 0) for r in rets[t - 13:t + 1]]
        losses = [max(-r, 0) for r in rets[t - 13:t + 1]]
        gl = sum(losses)
        rsi = 100.0 if gl == 0 else 100 - 100 / (1 + sum(gains) / gl)
        # posición dentro del rango de 40 velas
        w40 = closes[t - 39:t + 1]
        hi, lo = max(w40), min(w40)
        pos = (closes[t] - lo) / (hi - lo) if hi > lo else 0.5
        X.append([
            rets[t] / vol,                       # último retorno (normalizado)
            rets[t - 1] / vol,
            rets[t - 2] / vol,
            sum(rets[t - 4:t + 1]) / vol,        # momentum 25 min
            sum(rets[t - 11:t + 1]) / vol,       # momentum 1 h
            (rsi - 50) / 25,
            pos * 2 - 1,
            vol * 1000,
        ])
        y.append(1 if closes[t + 1] > closes[t] else 0)
    return X, y, rets


# ---------------------------------------------------------------- modelo

def train_logistic(X, y, epochs=400, lr=0.05, l2=1e-3):
    nfeat = len(X[0])
    w = [0.0] * nfeat
    b = 0.0
    n = len(X)
    for _ in range(epochs):
        gw = [0.0] * nfeat
        gb = 0.0
        for xi, yi in zip(X, y):
            z = b + sum(wj * xj for wj, xj in zip(w, xi))
            p = 1 / (1 + math.exp(-max(-30, min(30, z))))
            err = p - yi
            for j in range(nfeat):
                gw[j] += err * xi[j]
            gb += err
        for j in range(nfeat):
            w[j] -= lr * (gw[j] / n + l2 * w[j])
        b -= lr * gb / n
    return w, b


def predict(w, b, xi):
    z = b + sum(wj * xj for wj, xj in zip(w, xi))
    return 1 / (1 + math.exp(-max(-30, min(30, z))))


# ---------------------------------------------------------------- evaluación

def accuracy(preds, y):
    return sum(1 for p, yi in zip(preds, y) if (p >= 0.5) == (yi == 1)) / len(y)


def ci95(p, n):
    return 1.96 * math.sqrt(p * (1 - p) / n)


def economic_sim(probs, y, moves, thr):
    """Opera solo cuando |prob-0.5| supera el umbral. Devuelve pnl con y sin costes."""
    pnl_bruto = pnl_neto = 0.0
    trades = hits = 0
    for p, yi, mv in zip(probs, y, moves):
        if abs(p - 0.5) < thr:
            continue
        side = 1 if p >= 0.5 else -1
        realized = side * mv                     # retorno de la vela siguiente
        pnl_bruto += realized
        pnl_neto += realized - ROUND_TRIP
        trades += 1
        hits += 1 if (p >= 0.5) == (yi == 1) else 0
    return trades, (hits / trades if trades else 0.0), pnl_bruto, pnl_neto


def main():
    ap = argparse.ArgumentParser(description="¿Se puede predecir BTC a 5 minutos?")
    ap.add_argument("--days", type=int, default=14, help="días de historia (def: 14)")
    ap.add_argument("--sim", action="store_true", help="velas sintéticas (sin internet)")
    args = ap.parse_args()

    print("=" * 70)
    print("EXPERIMENTO: predicción de dirección de BTC a 5 minutos (educativo)")
    print("=" * 70)

    if args.sim:
        closes = sim_klines(args.days)
        print(f"[datos] {len(closes)} velas SINTÉTICAS (paseo aleatorio, sin ventaja posible)")
    else:
        try:
            closes = fetch_klines(args.days)
        except Exception as e:
            print(f"[datos] no se pudo descargar ({e.__class__.__name__}). "
                  "Prueba --sim o revisa tu conexión.")
            return 1
        print(f"[datos] {len(closes)} velas reales de BTCUSDT 5m")

    X, y, _ = build_dataset(closes)
    cut = int(len(X) * 0.7)
    Xtr, ytr = X[:cut], y[:cut]
    Xte, yte = X[cut:], y[cut:]
    print(f"[setup] train {len(Xtr)} velas (pasado) · test {len(Xte)} velas (futuro no visto)")

    print("[model] entrenando regresión logística…")
    w, b = train_logistic(Xtr, ytr)
    probs_te = [predict(w, b, xi) for xi in Xte]

    acc_te = accuracy(probs_te, yte)
    base_up = max(sum(yte), len(yte) - sum(yte)) / len(yte)
    # referencia "repite la última vela": feature 0 es el último retorno normalizado
    persist = [1.0 if xi[0] > 0 else 0.0 for xi in Xte]
    acc_persist = accuracy(persist, yte)
    e = ci95(0.5, len(yte))

    # economía: movimiento absoluto medio vs coste
    moves_te = []
    offset = 40 + cut
    for t in range(offset, offset + len(Xte)):
        moves_te.append(abs(closes[t + 1] / closes[t] - 1))
    avg_move = sum(moves_te) / len(moves_te)
    breakeven = 0.5 * (1 + ROUND_TRIP / avg_move) if avg_move else 1.0

    print()
    print(f"  precisión del modelo (test):      {acc_te*100:5.2f}%")
    print(f"  referencia mayoritaria:           {base_up*100:5.2f}%")
    print(f"  referencia 'repite última vela':  {acc_persist*100:5.2f}%")
    print(f"  zona de azar puro (n={len(yte)}):     50% ± {e*100:.2f}%  "
          f"(entre {50-e*100:.1f}% y {50+e*100:.1f}%)")
    print()
    print(f"  movimiento medio |5m| de la vela: {avg_move*100:.3f}%")
    print(f"  coste ida y vuelta:               {ROUND_TRIP*100:.3f}%")
    print(f"  → precisión mínima para no perder: {min(breakeven,1)*100:.1f}%"
          + ("  (¡imposible!)" if breakeven > 0.99 else ""))
    print()

    # simulación económica sobre el test con distintos umbrales de confianza
    signed_moves = []
    for t in range(offset, offset + len(Xte)):
        signed_moves.append(closes[t + 1] / closes[t] - 1)
    print("  si hubiéramos operado cada predicción del test:")
    print("  umbral conf.   trades   acierto   pnl bruto   pnl con costes")
    for thr in (0.0, 0.02, 0.05):
        n, hit, bruto, neto = economic_sim(probs_te, yte, signed_moves, thr)
        print(f"      {0.5+thr:.2f}      {n:6}   {hit*100:6.1f}%   {bruto*100:+8.2f}%   "
              f"{neto*100:+8.2f}%")
    print()
    print("Lectura: aunque la precisión supere el 50% por poco, el 'pnl con costes'")
    print("manda. A 5 minutos el movimiento medio es menor que la comisión: incluso")
    print("acertando mucho, el peaje se lo come todo. Un 'edge conf 96.5%' es ficción.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
