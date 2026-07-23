"""Contenido de los 30 videos del mes 1 (nicho: finanzas personales para jóvenes).

Cada video es una lista de segmentos: (duración, icono, líneas).
Cada línea: (texto, tamaño, color, retardo de aparición en segundos).
Los videos 4-30 usan el formato compacto con estilos; V() los expande.
"""

BLANCO = (236, 237, 239)
GRIS = (154, 160, 173)
ROJO = (255, 92, 92)
AMBAR = (255, 197, 61)
VERDE = (110, 200, 140)

# Estilos compactos: código -> (tamaño, color)
_E = {
    "g": (96, BLANCO),   # grande
    "n": (76, BLANCO),   # normal
    "n2": (68, BLANCO),  # normal chico
    "R": (112, ROJO),    # rojo gigante
    "r": (84, ROJO),     # rojo
    "A": (100, AMBAR),   # ámbar gigante
    "a": (84, AMBAR),    # ámbar
    "V": (100, VERDE),   # verde gigante
    "v": (84, VERDE),    # verde
    "d": (56, GRIS),     # dim
    "sp": (30, BLANCO),  # espaciador
}


def V(*segs):
    """Expande segmentos compactos: (dur, icono, [(texto, estilo, delay), ...])."""
    out = []
    for dur, icono, lineas in segs:
        exp = []
        for linea in lineas:
            if linea == "sp":
                exp.append(("", 30, BLANCO, 0))
            else:
                texto, estilo, delay = linea
                tam, color = _E[estilo]
                exp.append((texto, tam, color, delay))
        out.append((dur, icono, exp))
    return out


VIDEO_01 = [
    (4.0, "tv", [
        ("Tu NETFLIX", 92, BLANCO, 0.0),
        ("no cuesta $15.", 92, BLANCO, 0.2),
        ("", 30, BLANCO, 0),
        ("CUESTA", 96, AMBAR, 1.3),
        ("$30.000", 180, ROJO, 1.6),
    ]),
    (4.0, "monedas", [
        ("$15 al mes", 94, BLANCO, 0.0),
        ("= $180 al año", 94, BLANCO, 0.4),
        ("", 30, BLANCO, 0),
        ("«Poco», piensas.", 70, GRIS, 1.5),
        ("ERROR.", 124, ROJO, 2.3),
    ]),
    (4.5, "etiqueta", [
        ("Cada peso que gastas", 74, BLANCO, 0.0),
        ("tiene un precio", 74, BLANCO, 0.25),
        ("OCULTO:", 118, AMBAR, 1.0),
        ("", 30, BLANCO, 0),
        ("lo que pudo generar", 66, GRIS, 1.9),
        ("INVERTIDO", 96, BLANCO, 2.4),
    ]),
    (5.5, "curva", [
        ("$15 al mes al 10% anual", 68, BLANCO, 0.0),
        ("en 30 años son...", 64, GRIS, 0.8),
        ("COUNTER", 170, ROJO, 1.6),
        ("(promedio histórico de la bolsa)", 40, GRIS, 4.2),
    ]),
    (4.0, "carro", [
        ("Una suscripción", 82, BLANCO, 0.0),
        ("«barata»", 82, GRIS, 0.35),
        ("", 30, BLANCO, 0),
        ("VALE UN CARRO", 106, AMBAR, 1.3),
    ]),
    (5.0, "lista", [
        ("NO canceles Netflix.", 82, BLANCO, 0.0),
        ("Ese no es el punto.", 58, GRIS, 0.9),
        ("", 30, BLANCO, 0),
        ("Elimina la que", 78, BLANCO, 1.9),
        ("NO USASTE", 106, ROJO, 2.4),
        ("este mes", 78, BLANCO, 2.7),
    ]),
    (4.5, "invertir", [
        ("E invierte lo que", 82, BLANCO, 0.0),
        ("te cobraba.", 82, BLANCO, 0.35),
        ("", 30, BLANCO, 0),
        ("Cada mes.", 90, AMBAR, 1.5),
        ("Sin excusas.", 90, ROJO, 2.1),
    ]),
    (5.0, "burbuja", [
        ("¿Cuál suscripción", 80, BLANCO, 0.0),
        ("pagas SIN usar?", 80, BLANCO, 0.35),
        ("", 30, BLANCO, 0),
        ("CONFIÉSALO EN", 88, AMBAR, 1.6),
        ("LOS COMENTARIOS", 88, AMBAR, 1.9),
        ("▼", 84, ROJO, 2.5),
    ]),
]

VIDEO_02 = [
    (4.0, "carrito", [
        ("Tu CEREBRO te", 88, BLANCO, 0.0),
        ("SABOTEA", 128, ROJO, 0.4),
        ("cada vez que compras", 72, BLANCO, 1.0),
        ("", 30, BLANCO, 0),
        ("(y tiene arreglo)", 56, GRIS, 2.2),
    ]),
    (4.5, "chispa", [
        ("Ves algo que te gusta", 70, BLANCO, 0.0),
        ("y BUM:", 82, BLANCO, 0.6),
        ("DOPAMINA", 126, AMBAR, 1.1),
        ("", 30, BLANCO, 0),
        ("Tu cerebro grita:", 62, GRIS, 2.2),
        ("«¡CÓMPRALO YA!»", 94, ROJO, 2.7),
    ]),
    (4.5, "etiqueta", [
        ("Por eso existen las", 72, BLANCO, 0.0),
        ("ofertas «SOLO HOY»", 84, AMBAR, 0.5),
        ("", 30, BLANCO, 0),
        ("Quieren que decidas", 68, BLANCO, 1.6),
        ("SIN PENSAR", 110, ROJO, 2.1),
        ("Pero hay un truco...", 54, GRIS, 3.2),
    ]),
    (3.5, "reloj", [
        ("LA REGLA DE LAS", 82, BLANCO, 0.0),
        ("72 HORAS", 165, AMBAR, 0.5),
    ]),
    (4.5, "calendario", [
        ("¿Quieres comprarlo?", 80, BLANCO, 0.0),
        ("Perfecto.", 68, GRIS, 0.8),
        ("", 30, BLANCO, 0),
        ("ESPERA", 118, ROJO, 1.5),
        ("3 DÍAS", 118, AMBAR, 1.9),
    ]),
    (4.5, "check", [
        ("Si a las 72 horas", 76, BLANCO, 0.0),
        ("lo sigues queriendo:", 74, BLANCO, 0.4),
        ("", 30, BLANCO, 0),
        ("CÓMPRALO", 118, VERDE, 1.4),
        ("Sin culpa.", 68, GRIS, 2.2),
    ]),
    (5.0, "monedas", [
        ("Spoiler:", 80, AMBAR, 0.0),
        ("el 80% de las veces", 74, BLANCO, 0.5),
        ("SE TE OLVIDA", 116, ROJO, 1.4),
        ("", 30, BLANCO, 0),
        ("No era deseo.", 64, GRIS, 2.6),
        ("Era dopamina.", 64, GRIS, 3.1),
    ]),
    (5.0, "burbuja", [
        ("¿De qué compra", 80, BLANCO, 0.0),
        ("te arrepientes?", 80, BLANCO, 0.35),
        ("", 30, BLANCO, 0),
        ("CUÉNTALO EN", 88, AMBAR, 1.5),
        ("LOS COMENTARIOS", 88, AMBAR, 1.8),
        ("▼", 84, ROJO, 2.4),
    ]),
]

VIDEO_03 = [
    (4.0, "banco", [
        ("Ser POBRE", 100, BLANCO, 0.0),
        ("es CARÍSIMO", 110, ROJO, 0.5),
        ("", 30, BLANCO, 0),
        ("Te lo demuestro en 30 seg", 56, GRIS, 1.8),
    ]),
    (4.5, "banco", [
        ("¿Poco saldo en el banco?", 62, BLANCO, 0.0),
        ("COMISIÓN.", 106, ROJO, 0.6),
        ("¿Cajero de otro banco?", 62, BLANCO, 1.5),
        ("COMISIÓN.", 106, ROJO, 2.1),
        ("", 30, BLANCO, 0),
        ("Ser pobre tiene tarifa.", 56, GRIS, 3.2),
    ]),
    (4.5, "etiqueta", [
        ("¿No te alcanza?", 72, BLANCO, 0.0),
        ("Pagas en CUOTAS...", 84, AMBAR, 0.5),
        ("con INTERESES.", 84, ROJO, 1.2),
        ("", 30, BLANCO, 0),
        ("Todo te cuesta MÁS.", 68, BLANCO, 2.2),
        ("Y hay algo peor...", 54, GRIS, 3.3),
    ]),
    (5.0, "bota", [
        ("La teoría de las botas:", 64, BLANCO, 0.0),
        ("", 30, BLANCO, 0),
        ("Botas buenas: $50", 76, BLANCO, 0.8),
        ("duran 10 años", 64, VERDE, 1.3),
        ("Botas baratas: $10", 76, BLANCO, 2.2),
        ("duran 1 año", 64, ROJO, 2.7),
    ]),
    (4.5, "monedas", [
        ("El rico paga $50", 76, BLANCO, 0.0),
        ("UNA vez.", 84, VERDE, 0.6),
        ("", 30, BLANCO, 0),
        ("El pobre paga $10...", 76, BLANCO, 1.5),
        ("DIEZ VECES", 114, ROJO, 2.2),
        ("= $100 por las mismas botas", 54, GRIS, 3.1),
    ]),
    (4.5, "check", [
        ("Y no, no es tu culpa.", 70, BLANCO, 0.0),
        ("El sistema cobra", 70, BLANCO, 0.7),
        ("por NO tener.", 84, AMBAR, 1.2),
        ("", 30, BLANCO, 0),
        ("Pero conocer la trampa", 58, GRIS, 2.3),
        ("es empezar a escapar.", 58, GRIS, 2.8),
    ]),
    (4.5, "invertir", [
        ("Tu primera meta", 72, BLANCO, 0.0),
        ("NO es ser rico.", 72, BLANCO, 0.4),
        ("", 30, BLANCO, 0),
        ("Es un COLCHÓN", 96, AMBAR, 1.3),
        ("que te libre de comisiones,", 54, GRIS, 2.2),
        ("cuotas e intereses.", 54, GRIS, 2.7),
    ]),
    (5.0, "burbuja", [
        ("¿Qué cobro te parece", 76, BLANCO, 0.0),
        ("un ROBO?", 100, ROJO, 0.5),
        ("", 30, BLANCO, 0),
        ("DILO EN", 88, AMBAR, 1.6),
        ("LOS COMENTARIOS", 88, AMBAR, 1.9),
        ("▼", 84, ROJO, 2.5),
    ]),
]

VIDEO_04 = V(
    (4.0, "chispa", [("El truco del 1%", "A", 0.0), ("que arregla tu cuenta", "n", 0.5), "sp", ("(sin sufrir)", "d", 1.6)]),
    (4.5, "grafica", [("¿Ahorrar 30% de golpe?", "n", 0.0), ("IMPOSIBLE.", "R", 0.7), "sp", ("Por eso abandonas", "d", 1.9), ("a la segunda semana.", "d", 2.3)]),
    (4.5, "curva", [("Pero ¿mejorar 1%", "n", 0.0), ("cada mes?", "n", 0.4), "sp", ("Ni lo sientes.", "v", 1.4), ("Y se acumula.", "a", 2.2)]),
    (4.5, "monedas", [("Mes 1: guardas $10", "n", 0.0), ("Mes 6: guardas $60", "n", 0.8), ("Mes 12:", "n", 1.6), ("$120 al mes", "A", 2.1), ("sin dolor", "d", 2.9)]),
    (4.5, "check", [("La constancia le gana", "n", 0.0), ("al talento.", "n", 0.4), "sp", ("También con dinero.", "a", 1.5)]),
    (5.0, "burbuja", [("¿Te sumas al reto", "n", 0.0), ("del 1%?", "A", 0.4), "sp", ("Di «YO» EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_05 = V(
    (4.0, "etiqueta", [("El sueldo mínimo es", "n", 0.0), ("una TRAMPA", "R", 0.5), ("mental", "R", 0.9), "sp", ("y te explico por qué", "d", 1.9)]),
    (4.5, "banco", [("Te acostumbras a", "n", 0.0), ("cobrar lo mínimo...", "n", 0.4), "sp", ("y terminas pidiendo", "n2", 1.5), ("LO MÍNIMO", "R", 2.1)]),
    (4.5, "chispa", [("Se llama ANCLAJE:", "a", 0.0), "sp", ("tu mente fija ese número", "n2", 0.8), ("como «lo normal»", "n2", 1.3), ("Y ahí te quedas.", "d", 2.4)]),
    (4.5, "grafica", [("Quien negocia su sueldo", "n2", 0.0), ("gana hasta", "n", 0.7), ("20% MÁS", "A", 1.2), ("en 5 años", "n", 1.7)]),
    (4.5, "check", [("Tu sueldo NO es", "n", 0.0), ("tu valor.", "n", 0.4), "sp", ("Es tu punto", "a", 1.4), ("de partida.", "a", 1.8)]),
    (5.0, "burbuja", [("¿Alguna vez pediste", "n", 0.0), ("un aumento?", "n", 0.4), "sp", ("CUÉNTAME EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_06 = V(
    (4.0, "banco", [("Tu banco tiene una", "n", 0.0), ("cuenta que NO", "n", 0.4), ("te ofrece", "n", 0.7), "sp", ("Y es mejor que la tuya.", "d", 1.8)]),
    (4.5, "monedas", [("Tu cuenta normal paga", "n2", 0.0), ("0% de interés", "n", 0.6), "sp", ("CERO.", "R", 1.6), ("Tu plata duerme gratis.", "d", 2.5)]),
    (4.5, "banco", [("Las cuentas de", "n", 0.0), ("ALTO RENDIMIENTO", "A", 0.5), "sp", ("pagan intereses", "n", 1.5), ("todos los meses", "n", 1.9)]),
    (4.5, "telefono", [("Y se abren desde", "n", 0.0), ("el celular", "n", 0.4), "sp", ("en 10 minutos", "a", 1.4), ("Gratis.", "v", 2.2)]),
    (4.5, "check", [("Mismo dinero.", "n", 0.0), ("Mismo esfuerzo: cero.", "n", 0.5), "sp", ("Más intereses", "a", 1.6), ("para ti.", "a", 2.0)]),
    (5.0, "burbuja", [("¿Sabías que existían?", "n", 0.0), ("Sé sincero.", "d", 0.6), "sp", ("TE LEO EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_07 = V(
    (4.0, "carrito", [("Pierdes $100 al mes", "g", 0.0), ("sin darte cuenta", "n", 0.5), "sp", ("Estos son los 3 huecos:", "d", 1.6)]),
    (4.5, "etiqueta", [("1. El delivery", "A", 0.0), "sp", ("Pagas hasta 30% extra", "n2", 0.8), ("por no caminar", "n2", 1.3), ("dos cuadras", "d", 2.0)]),
    (4.5, "monedas", [("2. Cafés y snacks", "A", 0.0), "sp", ("$3 al día parecen nada", "n2", 0.8), ("= $90 AL MES", "R", 1.6)]),
    (4.5, "telefono", [("3. Suscripciones", "A", 0.0), ("fantasma", "A", 0.4), "sp", ("Las que pagas", "n2", 1.3), ("y ni recuerdas", "n2", 1.7)]),
    (4.5, "check", [("No es dejar de vivir.", "n", 0.0), "sp", ("Es ELEGIR a dónde", "a", 1.0), ("va tu plata.", "a", 1.4)]),
    (5.0, "burbuja", [("¿Cuál es tu", "n", 0.0), ("gasto hormiga?", "A", 0.4), "sp", ("CONFIÉSALO EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_08 = V(
    (4.0, "chispa", [("Tu cerebro ODIA", "g", 0.0), ("ahorrar", "R", 0.5), "sp", ("Es ciencia, no excusa.", "d", 1.6)]),
    (4.5, "reloj", [("Prefiere $10 hoy", "n", 0.0), ("que $100 en un año", "n", 0.5), "sp", ("Se llama descuento", "d", 1.6), ("hiperbólico", "a", 2.1)]),
    (4.5, "chispa", [("Para tu cerebro,", "n", 0.0), ("tu «yo futuro»...", "n", 0.5), "sp", ("es un DESCONOCIDO", "R", 1.5), ("¿Por qué darle tu plata?", "d", 2.5)]),
    (4.5, "check", [("El truco:", "n", 0.0), ("AUTOMATIZA", "A", 0.5), "sp", ("Que el ahorro salga solo", "n2", 1.5), ("el día de pago", "n2", 2.0)]),
    (4.5, "foco", [("No luches contra", "n", 0.0), ("tu cerebro.", "n", 0.4), "sp", ("PROGRÁMALO.", "A", 1.4)]),
    (5.0, "burbuja", [("¿Ahorras manual", "n", 0.0), ("o automático?", "n", 0.4), "sp", ("DIME EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_09 = V(
    (4.0, "foco", [("Este experimento", "n", 0.0), ("predice tu futuro", "n", 0.4), ("FINANCIERO", "A", 0.9), "sp", ("(con niños y dulces)", "d", 1.9)]),
    (4.5, "reloj", [("Le dan 1 dulce a un niño:", "n2", 0.0), "sp", ("«Si esperas 15 minutos,", "n2", 0.9), ("te doy DOS»", "a", 1.5)]),
    (4.5, "grafica", [("Años después,", "n", 0.0), ("los que esperaron", "n", 0.4), "sp", ("tenían mejores finanzas,", "n2", 1.4), ("trabajos y salud", "n2", 1.9)]),
    (4.5, "monedas", [("Tu sueldo es el dulce:", "n", 0.0), "sp", ("¿Te lo comes TODO", "n", 1.0), ("el mismo día?", "R", 1.6)]),
    (4.5, "check", [("Esperar no es aburrido.", "n2", 0.0), "sp", ("Es la habilidad", "a", 1.0), ("mejor pagada del mundo.", "a", 1.5)]),
    (5.0, "burbuja", [("¿Tú esperas o", "n", 0.0), ("te lo comes?", "n", 0.4), "sp", ("SÉ HONESTO EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_10 = V(
    (4.0, "carro", [("Los millonarios REALES", "n", 0.0), ("no se ven ricos", "g", 0.5), "sp", ("Y hay una razón.", "d", 1.6)]),
    (4.5, "carro", [("El del carro nuevo", "n", 0.0), ("del año...", "n", 0.4), "sp", ("suele deber", "n", 1.4), ("HASTA LA CAMISA", "R", 1.9)]),
    (4.5, "monedas", [("El millonario promedio", "n2", 0.0), "sp", ("usa carro usado", "n", 0.9), ("y reloj normal", "n", 1.4), ("Riqueza silenciosa.", "d", 2.4)]),
    (4.5, "chispa", [("Aparentar riqueza", "n", 0.0), "sp", ("es el hobby", "n", 0.9), ("MÁS CARO", "R", 1.4), ("del mundo", "n", 1.9)]),
    (4.5, "check", [("Rico no es el que", "n", 0.0), ("más muestra.", "n", 0.4), "sp", ("Es el que", "a", 1.4), ("menos debe.", "a", 1.8)]),
    (5.0, "burbuja", [("¿Conoces a alguien así?", "n2", 0.0), ("(no des nombres 😅)", "d", 0.6), "sp", ("CUENTA EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_11 = V(
    (4.0, "etiqueta", [("En crisis compras", "n", 0.0), ("MÁS tonterías", "R", 0.5), "sp", ("Es matemático.", "d", 1.6)]),
    (4.5, "chispa", [("Se llama", "n", 0.0), ("efecto lipstick:", "A", 0.4), "sp", ("lujos pequeños cuando", "n2", 1.4), ("no alcanza para grandes", "n2", 1.9)]),
    (4.5, "carrito", [("No puedes comprar casa...", "n2", 0.0), "sp", ("pero sí ese antojo", "n", 1.0), ("de $20", "A", 1.6), ("Y se siente bien.", "d", 2.5)]),
    (4.5, "monedas", [("El problema:", "n", 0.0), "sp", ("20 antojos de $20", "n", 0.9), ("= $400", "R", 1.5), ("que ni recuerdas", "d", 2.3)]),
    (4.5, "check", [("Date gustos.", "n", 0.0), "sp", ("Pero ELÍGELOS,", "a", 1.0), ("no los sufras.", "a", 1.4)]),
    (5.0, "burbuja", [("¿Cuál es tu", "n", 0.0), ("lujo pequeño?", "A", 0.4), "sp", ("DILO EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_12 = V(
    (4.0, "telefono", [("Ese lujo que muestras", "n", 0.0), ("en redes es", "n", 0.4), ("DEUDA", "R", 0.9), "sp", ("Y todos lo sabemos.", "d", 1.9)]),
    (4.5, "telefono", [("Celular de $1.000", "n", 0.0), ("en 24 cuotas", "n", 0.5), "sp", ("no es riqueza", "R", 1.5)]),
    (4.5, "etiqueta", [("Es pagar INTERESES", "n", 0.0), "sp", ("para impresionar a gente", "n2", 0.9), ("que ni te mira", "n2", 1.4)]),
    (4.5, "monedas", [("La riqueza real", "n", 0.0), ("es silenciosa:", "n", 0.4), "sp", ("es SALDO,", "a", 1.4), ("no fotos.", "a", 1.8)]),
    (4.5, "check", [("Presume en 10 años.", "n", 0.0), "sp", ("Con libertad,", "a", 1.0), ("no con logos.", "a", 1.4)]),
    (5.0, "burbuja", [("¿Compras para ti", "n", 0.0), ("o para mostrar?", "n", 0.4), "sp", ("HONESTIDAD EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_13 = V(
    (4.0, "grafica", [("La regla 50/30/20", "g", 0.0), ("NO funciona", "R", 0.5), ("si ganas poco", "n", 1.0)]),
    (4.5, "grafica", [("50% necesidades", "n2", 0.0), ("30% gustos", "n2", 0.5), ("20% ahorro...", "n2", 1.0), "sp", ("¿CON QUÉ SUELDO?", "R", 2.0)]),
    (4.5, "banco", [("Si el arriendo se come", "n2", 0.0), ("el 60%,", "A", 0.6), "sp", ("la regla solo sirve", "n2", 1.6), ("para frustrarte", "r", 2.1)]),
    (4.5, "check", [("Alternativa real:", "n", 0.0), "sp", ("empieza ahorrando 1%", "n2", 0.9), ("y sube 1% cada mes", "v", 1.5)]),
    (4.5, "foco", [("La mejor regla", "n", 0.0), "sp", ("es la que SÍ", "a", 1.0), ("puedes cumplir.", "a", 1.4)]),
    (5.0, "burbuja", [("¿Cuánto logras ahorrar?", "n2", 0.0), ("Sin juzgar.", "d", 0.6), "sp", ("DILO EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_14 = V(
    (4.0, "telefono", [("Las apps de compras", "n", 0.0), ("te MANIPULAN", "R", 0.5), "sp", ("Así lo hacen:", "d", 1.6)]),
    (4.5, "reloj", [("Ofertas con", "n", 0.0), ("cuenta regresiva", "a", 0.4), "sp", ("= pánico artificial", "n2", 1.4), ("para que no pienses", "d", 2.2)]),
    (4.5, "carrito", [("«Envío gratis si", "n2", 0.0), ("agregas un poco más»", "n2", 0.5), "sp", ("= terminas gastando", "n2", 1.5), ("MÁS", "R", 2.1)]),
    (4.5, "chispa", [("Comprar en 1 clic", "n", 0.0), "sp", ("= CERO segundos", "r", 1.0), ("para arrepentirte", "n2", 1.6)]),
    (4.5, "check", [("El antídoto: BORRA la app", "n2", 0.0), "sp", ("¿La necesitas? Navegador.", "n2", 1.0), ("Fricción = ahorro.", "a", 1.8)]),
    (5.0, "burbuja", [("¿Cuál app te hace", "n", 0.0), ("gastar más?", "A", 0.4), "sp", ("DILO EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_15 = V(
    (4.0, "invertir", [("Invertir tu primer $100", "n", 0.0), ("toma 10 MINUTOS", "A", 0.6), "sp", ("Paso a paso:", "d", 1.7)]),
    (4.5, "banco", [("1. Abre cuenta en un", "n2", 0.0), ("broker REGULADO", "a", 0.6), "sp", ("Desde el celular.", "n2", 1.6), ("Muchos sin mínimo.", "d", 2.3)]),
    (4.5, "curva", [("2. Compra un", "n", 0.0), ("FONDO INDEXADO", "A", 0.5), "sp", ("Todo el mercado", "n2", 1.5), ("en una sola compra", "n2", 2.0)]),
    (4.5, "reloj", [("3. NO lo toques", "g", 0.0), "sp", ("En serio.", "d", 1.0), ("Ni lo mires a diario.", "d", 1.5), ("Déjalo crecer.", "v", 2.3)]),
    (4.5, "check", [("No es para ser rico", "n2", 0.0), ("mañana.", "n2", 0.4), "sp", ("Es para EMPEZAR", "a", 1.4), ("la bola de nieve.", "a", 1.9)]),
    (5.0, "burbuja", [("¿Qué te frena", "n", 0.0), ("para empezar?", "n", 0.4), "sp", ("TE LEO EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_16 = V(
    (4.0, "curva", [("Ojalá me hubieran", "n", 0.0), ("mostrado esto", "n", 0.4), ("a los 18", "A", 0.9)]),
    (4.5, "monedas", [("$100 al mes", "g", 0.0), ("desde los 18...", "n", 0.6)]),
    (5.0, "curva", [("...a los 48 tienes", "n", 0.0), "sp", ("MÁS DE $200.000", "R", 1.0), ("(al 10% anual promedio)", "d", 2.2)]),
    (4.5, "reloj", [("¿Y si empiezas", "n", 0.0), ("a los 28?", "n", 0.4), "sp", ("Menos de la MITAD", "R", 1.4), ("10 años = doble.", "d", 2.4)]),
    (4.5, "foco", [("El mejor momento", "n", 0.0), ("fue a los 18.", "n", 0.4), "sp", ("El segundo mejor", "a", 1.4), ("es HOY.", "A", 1.9)]),
    (5.0, "burbuja", [("¿A qué edad", "n", 0.0), ("empiezas tú?", "n", 0.4), "sp", ("DILO EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_17 = V(
    (4.0, "telefono", [("Estas apps ahorran", "n", 0.0), ("aunque tú no quieras", "g", 0.5)]),
    (4.5, "monedas", [("1. Las que REDONDEAN", "a", 0.0), "sp", ("Pagas $2,70", "n2", 0.9), ("y guardan $0,30 solas", "n2", 1.4), ("Ni lo notas.", "d", 2.3)]),
    (4.5, "banco", [("2. Las de METAS", "a", 0.0), "sp", ("Separan tu plata", "n2", 0.9), ("el mismo día de pago", "n2", 1.4), ("Antes de que la veas.", "d", 2.3)]),
    (4.5, "grafica", [("3. Las que ANALIZAN", "a", 0.0), "sp", ("Te muestran a dónde", "n2", 0.9), ("se va todo", "n2", 1.4), ("(prepárate para llorar)", "d", 2.3)]),
    (4.5, "check", [("La fuerza de voluntad", "n2", 0.0), ("FALLA.", "R", 0.6), "sp", ("La automatización no.", "a", 1.6)]),
    (5.0, "burbuja", [("¿Usas alguna?", "n", 0.0), "sp", ("RECOMIENDA EN", "a", 1.2), ("LOS COMENTARIOS", "a", 1.5), ("▼", "r", 2.1)]),
)

VIDEO_18 = V(
    (4.0, "burbuja", [("Pide tu aumento con", "n", 0.0), ("estas palabras exactas", "g", 0.5)]),
    (4.5, "libro", [("1. Lista tus logros", "a", 0.0), ("CON NÚMEROS", "A", 0.5), "sp", ("«Este año logré X, Y, Z»", "n2", 1.5), ("Datos, no sentimientos.", "d", 2.4)]),
    (4.5, "grafica", [("2. Muestra crecimiento", "a", 0.0), "sp", ("«Mi rol creció:", "n2", 0.9), ("estos son los resultados»", "n2", 1.4)]),
    (4.5, "monedas", [("3. Cierra abierto:", "a", 0.0), "sp", ("«Busco un ajuste acorde.", "n2", 0.9), ("¿Qué necesitas", "n2", 1.5), ("ver de mí?»", "n2", 1.9)]),
    (4.5, "check", [("No pidas por necesidad.", "n2", 0.0), "sp", ("Muestra tu VALOR.", "a", 1.0), ("Los números negocian solos.", "d", 1.9)]),
    (5.0, "burbuja", [("¿Te da miedo pedirlo?", "n2", 0.0), "sp", ("CONFIESA EN", "a", 1.2), ("LOS COMENTARIOS", "a", 1.5), ("▼", "r", 2.1)]),
)

VIDEO_19 = V(
    (4.0, "sobre", [("Tu abuela manejaba", "n", 0.0), ("el dinero MEJOR", "A", 0.5), ("que tú", "n", 0.9)]),
    (4.5, "sobre", [("Su truco: SOBRES", "a", 0.0), "sp", ("Uno para comida,", "n2", 0.9), ("uno para renta,", "n2", 1.3), ("uno para gustos", "n2", 1.7)]),
    (4.5, "telefono", [("Versión 2026:", "n", 0.0), "sp", ("SUBCUENTAS digitales", "a", 0.9), ("con nombre y apellido", "n2", 1.5)]),
    (4.5, "calendario", [("El día de pago", "n", 0.0), ("reparte TODO", "A", 0.5), "sp", ("Cada peso", "n2", 1.5), ("con su misión", "n2", 1.9)]),
    (4.5, "foco", [("Lo que no tiene nombre...", "n2", 0.0), "sp", ("se gasta SOLO.", "R", 1.2)]),
    (5.0, "burbuja", [("¿Le pones nombre", "n", 0.0), ("a tu plata?", "n", 0.4), "sp", ("DIME EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_20 = V(
    (4.0, "escudo", [("NO necesitas 6 meses", "n", 0.0), ("de sueldo ahorrado", "n", 0.5), "sp", ("Eso te paraliza.", "d", 1.6)]),
    (4.5, "escudo", [("Eso dicen los gurús.", "n", 0.0), "sp", ("Y tú, al ver la cifra,", "n2", 1.0), ("NI EMPIEZAS", "R", 1.6)]),
    (4.5, "monedas", [("Meta 1: $500", "A", 0.0), "sp", ("Cubre la mayoría de", "n2", 0.9), ("emergencias reales:", "n2", 1.4), ("llanta, muela, celular", "d", 2.2)]),
    (4.5, "grafica", [("Después: 1 mes de gastos", "n2", 0.0), ("Luego 3. Luego 6.", "n2", 0.6), "sp", ("POR NIVELES,", "a", 1.6), ("como un videojuego", "n2", 2.1)]),
    (4.5, "check", [("Un fondo pequeño HOY", "n2", 0.0), "sp", ("vale más que uno", "a", 1.0), ("perfecto NUNCA.", "a", 1.5)]),
    (5.0, "burbuja", [("¿Nivel 0, 1, 2 o 3?", "n", 0.0), "sp", ("DI EL TUYO EN", "a", 1.2), ("LOS COMENTARIOS", "a", 1.5), ("▼", "r", 2.1)]),
)

VIDEO_21 = V(
    (4.0, "check", [("Hay deudas que", "n", 0.0), ("te hacen RICO", "V", 0.5), "sp", ("(y nadie te lo explica)", "d", 1.6)]),
    (4.5, "etiqueta", [("Deuda MALA:", "r", 0.0), "sp", ("compra cosas que", "n2", 0.9), ("PIERDEN valor", "R", 1.4), ("ropa, antojos, apariencias", "d", 2.3)]),
    (4.5, "curva", [("Deuda BUENA:", "v", 0.0), "sp", ("compra cosas que", "n2", 0.9), ("GENERAN valor", "V", 1.4)]),
    (4.5, "libro", [("Educación que sube", "n2", 0.0), ("tu sueldo,", "n2", 0.4), ("herramientas de trabajo,", "n2", 0.9), ("un negocio que factura", "n2", 1.4)]),
    (4.5, "escudo", [("La pregunta no es", "n2", 0.0), ("«¿me endeudo?»", "n", 0.5), "sp", ("Es: «¿esto me paga", "a", 1.5), ("de vuelta?»", "a", 2.0)]),
    (5.0, "burbuja", [("¿Tu deuda actual es", "n", 0.0), ("buena o mala?", "A", 0.4), "sp", ("ANALÍZALA EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_22 = V(
    (4.0, "tv", [("Un canal de 10K subs", "n", 0.0), ("gana ESTO:", "A", 0.5), "sp", ("(números reales)", "d", 1.6)]),
    (4.5, "monedas", [("De AdSense en Shorts:", "n2", 0.0), "sp", ("$50-150 al mes", "n", 0.9), ("Sí. POCO.", "R", 1.7), ("Pero espera...", "d", 2.6)]),
    (4.5, "grafica", [("AdSense es solo", "n", 0.0), "sp", ("la PUNTA", "a", 0.9), ("del iceberg", "n", 1.4)]),
    (4.5, "invertir", [("Afiliados, productos", "n2", 0.0), ("y marcas", "n2", 0.4), "sp", ("pagan 5-10x MÁS", "A", 1.4), ("con la misma audiencia", "d", 2.3)]),
    (4.5, "check", [("10K subs no es", "n", 0.0), ("un sueldo.", "n", 0.4), "sp", ("Es una PALANCA.", "A", 1.4)]),
    (5.0, "burbuja", [("¿Quieres la parte 2", "n", 0.0), ("con el desglose?", "n", 0.4), "sp", ("DI «PARTE 2» EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_23 = V(
    (4.0, "grafica", [("¿Eres clase media?", "g", 0.0), "sp", ("Los números dicen", "n", 1.0), ("otra cosa", "R", 1.5)]),
    (4.5, "banco", [("Clase media era:", "n", 0.0), "sp", ("casa + carro", "n2", 0.9), ("+ vacaciones", "n2", 1.3), ("con UN sueldo", "a", 2.0)]),
    (4.5, "etiqueta", [("Hoy ese estándar", "n", 0.0), "sp", ("cuesta DOS sueldos", "R", 1.0), ("(y a veces ni así)", "d", 2.0)]),
    (4.5, "monedas", [("No es que gastes mal.", "n2", 0.0), "sp", ("Es que TODO subió", "n2", 1.0), ("más que tu sueldo", "r", 1.6)]),
    (4.5, "check", [("No te compares", "n", 0.0), ("con tus papás.", "n", 0.4), "sp", ("Compárate con", "a", 1.4), ("TU plan.", "a", 1.8)]),
    (5.0, "burbuja", [("¿Cuánto se necesita", "n", 0.0), ("en tu país?", "n", 0.4), "sp", ("DEBATE EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_24 = V(
    (4.0, "monedas", [("Llevas años", "n", 0.0), ("ahorrando MAL", "R", 0.5), "sp", ("Y te explico por qué.", "d", 1.6)]),
    (4.5, "monedas", [("El dinero quieto", "n", 0.0), ("PIERDE:", "R", 0.5), "sp", ("la inflación se lo come", "n2", 1.5), ("un poco cada año", "d", 2.3)]),
    (4.5, "curva", [("Bajo el colchón,", "n", 0.0), "sp", ("$1.000 de hoy", "n", 0.9), ("valdrán mucho menos", "r", 1.5), ("en 5 años", "n2", 2.1)]),
    (4.5, "invertir", [("Ahorrar es DEFENSA.", "n", 0.0), "sp", ("Invertir es", "n", 1.0), ("ATAQUE.", "A", 1.5)]),
    (4.5, "check", [("Primero: colchón", "n", 0.0), ("de emergencia.", "n", 0.4), "sp", ("Después: todo lo demás", "a", 1.4), ("A TRABAJAR.", "A", 2.0)]),
    (5.0, "burbuja", [("¿Tu plata trabaja", "n", 0.0), ("o duerme?", "A", 0.4), "sp", ("RESPONDE EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_25 = V(
    (4.0, "escudo", [("Así funciona la estafa", "n", 0.0), ("que ves en Instagram", "n", 0.5), "sp", ("Apréndetela.", "d", 1.6)]),
    (4.5, "chispa", [("Paso 1: foto con", "n2", 0.0), ("carro RENTADO", "a", 0.5), "sp", ("«Mira mis resultados,", "d", 1.5), ("tú también puedes»", "d", 2.0)]),
    (4.5, "etiqueta", [("Paso 2: te venden", "n2", 0.0), ("un curso para", "n2", 0.4), ("hacerte rico RÁPIDO", "R", 1.0)]),
    (4.5, "monedas", [("La verdad:", "n", 0.0), "sp", ("su negocio no es invertir.", "n2", 0.9), ("Es VENDERTE", "R", 1.6), ("el curso.", "n", 2.1)]),
    (4.5, "escudo", [("Regla de oro:", "n", 0.0), "sp", ("si te APURAN a decidir,", "a", 1.0), ("es trampa.", "r", 1.7)]),
    (5.0, "burbuja", [("¿Te han intentado", "n", 0.0), ("reclutar?", "A", 0.4), "sp", ("CUENTA LA HISTORIA", "a", 1.5), ("EN COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_26 = V(
    (4.0, "invertir", [("3 ingresos extra que", "n", 0.0), ("empiezan con $0", "A", 0.5), "sp", ("Sin humo. Verificables.", "d", 1.6)]),
    (4.5, "telefono", [("1. Vende lo que", "a", 0.0), ("ya no usas", "a", 0.4), "sp", ("Todos tenemos $200", "n2", 1.4), ("durmiendo en cajones", "n2", 1.9)]),
    (4.5, "libro", [("2. Ofrece lo que", "a", 0.0), ("ya sabes", "a", 0.4), "sp", ("Clases, diseño, textos,", "n2", 1.4), ("planillas, traducciones", "n2", 1.9)]),
    (4.5, "tv", [("3. Documenta lo", "a", 0.0), ("que aprendes", "a", 0.4), "sp", ("Contenido de nicho", "n2", 1.4), ("(como este canal 😉)", "d", 2.2)]),
    (4.5, "check", [("No necesitas capital.", "n2", 0.0), "sp", ("Necesitas empezar", "a", 1.0), ("AUNQUE SALGA FEO.", "A", 1.6)]),
    (5.0, "burbuja", [("¿Cuál probarías:", "n", 0.0), ("1, 2 o 3?", "A", 0.4), "sp", ("VOTA EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_27 = V(
    (4.0, "libro", [("Lo que te enseñaron", "n", 0.0), ("del dinero", "n", 0.4), ("YA NO APLICA", "R", 0.9)]),
    (4.5, "libro", [("«Estudia, empleo fijo,", "n2", 0.0), ("y jubílate»", "n2", 0.5), "sp", ("era el plan de", "n2", 1.5), ("OTRO MUNDO", "R", 2.0)]),
    (4.5, "banco", [("Antes: un sueldo", "n", 0.0), ("compraba una casa", "n", 0.5), "sp", ("Hoy: apenas paga", "n2", 1.5), ("el arriendo", "r", 2.0)]),
    (4.5, "foco", [("Y no es culpa", "n", 0.0), ("de tus papás:", "n", 0.4), "sp", ("su consejo era perfecto...", "d", 1.4), ("para su época.", "a", 2.0)]),
    (4.5, "check", [("Honra su esfuerzo:", "n", 0.0), "sp", ("aprende lo que ellos", "a", 1.0), ("no pudieron.", "a", 1.5)]),
    (5.0, "burbuja", [("¿Qué consejo de dinero", "n2", 0.0), ("te dieron en casa?", "n2", 0.4), "sp", ("CUÉNTALO EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_28 = V(
    (4.0, "carro", [("Tu carro te cuesta", "n", 0.0), ("el DOBLE", "R", 0.5), ("de lo que crees", "n", 0.9)]),
    (4.5, "carro", [("El precio de compra", "n", 0.0), "sp", ("es solo la ENTRADA", "a", 1.0), ("al club", "n", 1.5)]),
    (4.5, "etiqueta", [("Seguro + gasolina", "n2", 0.0), ("+ mantenimiento", "n2", 0.5), ("+ parqueo + multas", "n2", 1.0), "sp", ("Suma TODO eso.", "r", 2.0)]),
    (4.5, "curva", [("Y encima pierde", "n", 0.0), "sp", ("20% de su valor", "R", 1.0), ("el PRIMER año", "n", 1.6)]),
    (4.5, "check", [("¿Lo necesitas? Cómpralo.", "n2", 0.0), "sp", ("¿Es para presumir?", "n2", 1.0), ("Recuerda este video.", "a", 1.6)]),
    (5.0, "burbuja", [("¿Cuánto te cuesta el tuyo", "n2", 0.0), ("al mes? De verdad.", "n2", 0.4), "sp", ("CALCULA EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_29 = V(
    (4.0, "monedas", [("Un dólar al día", "g", 0.0), "sp", ("puede volverse", "n", 1.0), ("SEIS CIFRAS", "A", 1.5)]),
    (4.5, "monedas", [("$1 diario", "g", 0.0), ("= $365 al año", "n", 0.5), "sp", ("«Eso no es nada»,", "d", 1.5), ("dices.", "d", 2.0)]),
    (5.0, "curva", [("Invertido al 10% anual", "n2", 0.0), ("durante 40 años...", "n2", 0.5), "sp", ("casi $200.000", "R", 1.6)]),
    (4.5, "foco", [("No es magia.", "n", 0.0), "sp", ("Es tiempo + constancia:", "n2", 1.0), ("la fórmula ABURRIDA", "a", 1.6), ("que sí funciona", "n2", 2.2)]),
    (4.5, "check", [("Un dólar. Cada día.", "n", 0.0), "sp", ("Tu yo del futuro", "a", 1.0), ("hará una fiesta.", "a", 1.5)]),
    (5.0, "burbuja", [("¿Puedes apartar", "n", 0.0), ("$1 al día?", "A", 0.4), "sp", ("SÉ HONESTO EN", "a", 1.5), ("LOS COMENTARIOS", "a", 1.8), ("▼", "r", 2.4)]),
)

VIDEO_30 = V(
    (4.0, "sobre", [("Tu yo de 40 años", "g", 0.0), ("te RUEGA", "R", 0.5), ("que veas esto", "n", 0.9)]),
    (4.5, "reloj", [("Él ya sabe si", "n", 0.0), ("empezaste hoy...", "n", 0.4), "sp", ("o si lo dejaste", "n2", 1.4), ("«para luego»", "r", 1.9)]),
    (4.5, "monedas", [("Cada peso que", "n", 0.0), ("guardas hoy", "n", 0.4), "sp", ("es un REGALO", "a", 1.4), ("que le mandas", "n", 1.9)]),
    (4.5, "curva", [("Y el tiempo lo multiplica:", "n2", 0.0), "sp", ("tú pones $1...", "n", 1.0), ("él recibe $10", "V", 1.6)]),
    (4.5, "check", [("No ahorras para tu jefe", "n2", 0.0), ("ni para presumir.", "n2", 0.5), "sp", ("Ahorras para ÉL.", "A", 1.5)]),
    (5.0, "burbuja", [("Escríbele algo a", "n", 0.0), ("tu yo de 40", "A", 0.4), "sp", ("AQUÍ ABAJO ✍️", "a", 1.5), ("▼", "r", 2.1)]),
)

VIDEOS = {
    "1": ("video-01-netflix.mp4", VIDEO_01),
    "2": ("video-02-72horas.mp4", VIDEO_02),
    "3": ("video-03-pobre-caro.mp4", VIDEO_03),
    "4": ("video-04-truco-1pct.mp4", VIDEO_04),
    "5": ("video-05-sueldo-minimo.mp4", VIDEO_05),
    "6": ("video-06-cuenta-banco.mp4", VIDEO_06),
    "7": ("video-07-gastos-hormiga.mp4", VIDEO_07),
    "8": ("video-08-cerebro-ahorro.mp4", VIDEO_08),
    "9": ("video-09-malvavisco.mp4", VIDEO_09),
    "10": ("video-10-ricos-tacanos.mp4", VIDEO_10),
    "11": ("video-11-efecto-lipstick.mp4", VIDEO_11),
    "12": ("video-12-presumir-pobreza.mp4", VIDEO_12),
    "13": ("video-13-regla-503020.mp4", VIDEO_13),
    "14": ("video-14-apps-dopamina.mp4", VIDEO_14),
    "15": ("video-15-primeros-100.mp4", VIDEO_15),
    "16": ("video-16-interes-compuesto.mp4", VIDEO_16),
    "17": ("video-17-apps-ahorro.mp4", VIDEO_17),
    "18": ("video-18-pedir-aumento.mp4", VIDEO_18),
    "19": ("video-19-metodo-sobres.mp4", VIDEO_19),
    "20": ("video-20-fondo-emergencia.mp4", VIDEO_20),
    "21": ("video-21-deuda-buena.mp4", VIDEO_21),
    "22": ("video-22-youtuber-10k.mp4", VIDEO_22),
    "23": ("video-23-clase-media.mp4", VIDEO_23),
    "24": ("video-24-ahorrar-no-basta.mp4", VIDEO_24),
    "25": ("video-25-estafa-rapida.mp4", VIDEO_25),
    "26": ("video-26-ingresos-extra.mp4", VIDEO_26),
    "27": ("video-27-consejos-papas.mp4", VIDEO_27),
    "28": ("video-28-costo-carro.mp4", VIDEO_28),
    "29": ("video-29-dolar-diario.mp4", VIDEO_29),
    "30": ("video-30-carta-yo-40.mp4", VIDEO_30),
}
