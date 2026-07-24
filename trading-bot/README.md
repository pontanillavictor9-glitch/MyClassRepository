# PAPER·QUANT bot — laboratorio de estrategias de paper trading

Bot educativo que opera **continuamente** sin navegador, guarda su estado y
retoma la sesión si se reinicia. Incluye varias estrategias clásicas, costes
realistas (comisión 0,10% + slippage por lado) y un modo torneo para
compararlas con datos, no con fe.

**Todo el dinero es ficticio.** En modo real solo se *leen* precios de mercado;
ninguna orden se envía a ningún exchange. **No existe el bot que "gana dinero
garantizado"** — este proyecto sirve para entender por qué.

## Uso

```bash
python3 paper_bot.py                     # estrategia ema, precios reales
python3 paper_bot.py --sim               # precios simulados (sin internet)
python3 paper_bot.py --strategy rsi      # elegir: ema / rsi / breakout / random
python3 paper_bot.py --compare --sim     # torneo: todas a la vez + buy&hold
python3 paper_bot.py --no-fees           # sin costes (para ver su efecto)
```

Solo necesita Python 3 estándar. `Ctrl+C` detiene guardando el estado
(`state_<estrategia>.json`); al relanzar, la sesión continúa. Cada operación
cerrada queda en `trades.csv` con sus costes y motivo de salida.

## Las estrategias

| Nombre     | Idea | Tipo |
|------------|------|------|
| `ema`      | cruce de medias EMA 8/21 | seguimiento de tendencia |
| `rsi`      | RSI(14) <30 compra, >70 vende | reversión a la media |
| `breakout` | ruptura del canal de 40 muestras (Donchian) | momentum |
| `random`   | moneda al aire | **grupo de control** |

Todas comparten la misma gestión de riesgo: 1% del capital por operación (1R),
stop a -1R, take-profit a +1.5R, salida por señal contraria o tiempo máximo.

## Lo que enseña el torneo (resultados reales de este repo)

Sobre precios simulados (paseo aleatorio, donde por construcción **no existe
ventaja posible**), 5.000 muestras:

**Con costes realistas** — todas las estrategias se hunden; la que más opera,
más pierde. Las comisiones se comieron $5.000–$9.000 de un capital de $10.000:

```
estrategia      trades   WR%     PF   costes($)   equity final
buy&hold BTC        1    0.0    ·           0   $ 9,226  (-774)
ema               255   28.6   0.45      6,247   $ 4,464  (-5,536)
random            219   28.8   0.26      5,200   $ 4,144  (-5,856)
rsi               253   36.0   0.15      5,324   $ 3,532  (-6,468)
breakout          414   26.1   0.51      9,075   $ 3,200  (-6,800)
```

**Sin costes** — todo queda alrededor del empate… y en esta tirada la que ganó
fue la **moneda al aire**. Un "ganador" puede ser pura suerte:

```
random            230   52.2   1.11          0   $10,688  (+688)
buy&hold BTC        1    0.0    ·           0   $10,424  (+424)
ema               232   37.5   1.05          0   $10,393  (+393)
rsi               232   59.5   0.89          0   $ 9,188  (-812)
breakout          443   29.6   0.83          0   $ 7,762  (-2,238)
```

Moralejas: (1) operar mucho multiplica los costes, no las ganancias;
(2) sin una ventaja real y medible, un bot es una máquina de pagar comisiones;
(3) cualquier racha ganadora corta puede ser azar — exige miles de operaciones
y validación fuera de muestra antes de creerte nada.

## Cómo dejarlo corriendo solo

```bash
nohup python3 paper_bot.py >> bot.log 2>&1 &
tail -f bot.log
```

Corre mientras el ordenador esté encendido. Para 24/7 real: una Raspberry Pi
o un VPS. El estado persistente hace que un reinicio no pierda nada.
