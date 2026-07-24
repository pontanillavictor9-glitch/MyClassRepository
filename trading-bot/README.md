# PAPER·QUANT bot — paper trading continuo

Bot educativo que opera **continuamente** con la estrategia del dashboard
(cruce EMA 8/21, riesgo del 1% por operación), pero como proceso independiente:
no necesita navegador, guarda su estado y retoma la sesión si se reinicia.

**Todo el dinero es ficticio.** En modo real solo se *leen* precios de mercado;
ninguna orden se envía a ningún exchange.

## Uso

```bash
# precios reales (Binance REST, Coinbase de respaldo), muestra cada 5s
python3 paper_bot.py

# precios simulados (sin internet)
python3 paper_bot.py --sim
```

No necesita instalar nada: solo Python 3 estándar.

- `state.json` — estado vivo (equity, EMAs, posiciones). Se guarda solo;
  al relanzar el bot, la sesión continúa donde iba.
- `trades.csv` — historial de todas las operaciones cerradas, con motivo de
  salida (stop -1R, take-profit +1.5R, señal invertida o tiempo máximo).
- `Ctrl+C` — detiene el bot guardando el estado.

## Cómo dejarlo corriendo 24/7

En tu propio ordenador (mientras esté encendido):

```bash
nohup python3 paper_bot.py >> bot.log 2>&1 &
tail -f bot.log        # para mirar cómo va
```

Para que corra aunque tu ordenador esté apagado necesitarías una máquina
siempre encendida (una Raspberry Pi, un VPS…). Un cron de GitHub Actions también
puede ejecutarlo por ráfagas periódicas, pero no es un proceso continuo real.

## La estrategia, en corto

1. Cada muestra actualiza precio, volatilidad (EWMA) y las EMAs 8 y 21.
2. Si la EMA rápida se separa de la lenta más que un umbral (relativo a la
   volatilidad en modo real), abre una posición de papel LONG o SHORT.
3. El tamaño se calcula para que un movimiento de 6σ en contra ≈ 1% del capital (1R).
4. Sale por stop (-1R), take-profit (+1.5R), señal invertida o tiempo máximo.

Es una estrategia *de juguete* para aprender: espera verla perder muchas veces.
Eso es exactamente lo que pasa con las estrategias simples en mercados reales,
y es la lección que los posts viral-milagro no cuentan.
