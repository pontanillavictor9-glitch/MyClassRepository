# Puente MetaTrader 5 → Trading Live Studio
#
# Lee tu cuenta de MT5 (real o demo, da igual) y empuja cada segundo el estado
# al servidor Node para que los overlays muestren TUS posiciones reales:
# operaciones abiertas con su P&L, flotante, cerrado hoy y beneficio del día.
#
# Requisitos (solo Windows, con el terminal MT5 instalado y abierto):
#   pip install MetaTrader5 requests
#
# Uso (desde la carpeta raíz del proyecto, con `npm start` ya corriendo):
#   python mt5/bridge.py
#
# El terminal de MetaTrader 5 debe estar ABIERTO y con sesión iniciada.
# No hace falta poner aquí tu contraseña: el puente se conecta al terminal
# que ya tienes abierto en el PC.

import json
import os
import sys
import time
from datetime import datetime, date, timedelta

try:
    import MetaTrader5 as mt5
except ImportError:
    print("Falta el paquete MetaTrader5. Instálalo con: pip install MetaTrader5")
    print("(Solo funciona en Windows, donde está instalado el terminal MT5)")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Falta el paquete requests. Instálalo con: pip install requests")
    sys.exit(1)


def cargar_config():
    """Busca config.json (o el ejemplo) en la carpeta actual o la superior."""
    for carpeta in (".", ".."):
        for nombre in ("config.json", "config.example.json"):
            ruta = os.path.join(carpeta, nombre)
            if os.path.exists(ruta):
                with open(ruta, encoding="utf-8") as f:
                    return json.load(f)
    return {}


config = cargar_config()
PUERTO = config.get("puerto", 3000)
TOKEN = os.environ.get("PANEL_TOKEN") or config.get("panelToken", "")
URL = f"http://localhost:{PUERTO}/api/mt5/state"
INTERVALO = 1  # segundos entre actualizaciones


def mapear_posicion(p):
    es_long = p.type == mt5.POSITION_TYPE_BUY
    direccion = 1 if es_long else -1
    pct = None
    if p.price_open:
        pct = (p.price_current - p.price_open) / p.price_open * 100 * direccion
    return {
        "id": p.ticket,
        "symbol": p.symbol,
        "side": "long" if es_long else "short",
        "qty": p.volume,
        "entryPrice": p.price_open,
        "lastPrice": p.price_current,
        "pnl": p.profit + p.swap,
        "pnlPct": pct,
        "openedAt": datetime.fromtimestamp(p.time).isoformat(),
    }


def realizado_hoy():
    """Suma el P&L de las operaciones CERRADAS hoy (sin contar depósitos/retiradas)."""
    desde = datetime.combine(date.today(), datetime.min.time())
    hasta = datetime.now() + timedelta(minutes=5)
    deals = mt5.history_deals_get(desde, hasta) or []
    total = 0.0
    for d in deals:
        if d.type in (mt5.DEAL_TYPE_BUY, mt5.DEAL_TYPE_SELL) and d.entry != mt5.DEAL_ENTRY_IN:
            total += d.profit + d.commission + d.swap
    return total


def historial_hoy():
    """Últimos cierres de hoy para la tabla de historial del panel."""
    desde = datetime.combine(date.today(), datetime.min.time())
    hasta = datetime.now() + timedelta(minutes=5)
    deals = mt5.history_deals_get(desde, hasta) or []
    cierres = []
    for d in deals:
        if d.type in (mt5.DEAL_TYPE_BUY, mt5.DEAL_TYPE_SELL) and d.entry != mt5.DEAL_ENTRY_IN:
            cierres.append({
                "id": d.ticket,
                "symbol": d.symbol,
                # El deal que cierra un long es una venta, y viceversa
                "side": "long" if d.type == mt5.DEAL_TYPE_SELL else "short",
                "qty": d.volume,
                "entryPrice": None,
                "exitPrice": d.price,
                "pnl": d.profit + d.commission + d.swap,
                "closedAt": datetime.fromtimestamp(d.time).isoformat(),
            })
    cierres.sort(key=lambda c: c["closedAt"], reverse=True)
    return cierres[:30]


def main():
    if not mt5.initialize():
        print("❌ No se pudo conectar con el terminal MT5:", mt5.last_error())
        print("   Asegúrate de que MetaTrader 5 está ABIERTO y con la sesión iniciada.")
        sys.exit(1)

    cuenta = mt5.account_info()
    if cuenta is None:
        print("❌ MT5 está abierto pero sin sesión iniciada en ninguna cuenta.")
        sys.exit(1)

    print(f"✅ Conectado a la cuenta MT5 #{cuenta.login} ({cuenta.server}) en {cuenta.currency}")
    print(f"   Empujando estado a {URL} cada {INTERVALO}s. Ctrl+C para salir.")

    errores_seguidos = 0
    while True:
        try:
            acc = mt5.account_info()
            posiciones = mt5.positions_get() or []
            realizado = realizado_hoy()
            flotante = acc.profit

            payload = {
                "moneda": acc.currency,
                "balance": acc.balance,
                "equity": acc.equity,
                "positions": [mapear_posicion(p) for p in posiciones],
                "history": historial_hoy(),
                "realizadoHoy": realizado,
                "flotante": flotante,
                "beneficioDia": realizado + flotante,
            }
            r = requests.post(
                URL,
                json=payload,
                headers={"x-panel-token": TOKEN},
                timeout=5,
            )
            if r.status_code == 401:
                print("❌ Token incorrecto: revisa panelToken en config.json")
                sys.exit(1)
            r.raise_for_status()
            errores_seguidos = 0
        except KeyboardInterrupt:
            break
        except Exception as e:
            errores_seguidos += 1
            if errores_seguidos in (1, 10) or errores_seguidos % 60 == 0:
                print(f"⚠️  Error enviando estado ({e}). ¿Está el servidor arrancado (npm start)?")
        time.sleep(INTERVALO)

    mt5.shutdown()
    print("Puente detenido.")


if __name__ == "__main__":
    main()
