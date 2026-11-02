"""
El catálogo: cada producto, de qué está hecho y cómo se presenta.
Para añadir un producto nuevo se añade aquí una entrada.
"""

import comun
from productos import decodables, lectura, multiplicacion

PRODUCTOS = {
    "multiplicacion-g3": {
        "tipo": "matematicas",
        "html": multiplicacion.html,
        "problemas": multiplicacion.problemas,
        "colores": multiplicacion.COLORES,
        "muestras": [0, 2, 15, 18],          # índices de página (empieza en 0)
        "ficha": {
            "titulo": "Multiplication Fact Fluency Drills Grade 3 | Timed Tests Facts 0-10 | Answer Keys",
            "grados": ["3rd"], "materias": ["Math"], "estandares": ["3.OA.C.7"],
            "precio_usd": 4.00,
            "portada": {"grado": "GRADE 3", "linea1": "Multiplication", "linea2": "Fluency Drills",
                        "detalle": "Facts 0–10 · 14 practice pages · Answer keys"},
            "insignias": ["Print & Go", "Answer Keys", "Certificate"],
        },
    },
    "thanksgiving-lectura-g3": {
        "tipo": "lectura",
        "contenido": "thanksgiving-g3.json",
        "html": lambda: lectura.html(comun.leer_json(comun.CONTENIDO / "thanksgiving-g3.json")),
        "colores": lectura.COLORES,
        "muestras": [0, 2, 3, 10],
        "ficha": {
            "titulo": "Thanksgiving Reading Comprehension Passages 3rd Grade | Fiction & Nonfiction | Answer Key",
            "grados": ["3rd"], "materias": ["Reading", "Thanksgiving"], "estandares": ["RL.3.1", "RI.3.1", "L.3.4"],
            "precio_usd": 3.50,
            "portada": {"grado": "GRADE 3", "linea1": "Thanksgiving", "linea2": "Reading Passages",
                        "detalle": "4 passages · Questions · Vocabulary · Answer key"},
            "insignias": ["Fiction & Nonfiction", "Print & Go", "Answer Key"],
        },
    },
    "silent-e-decodables-g1": {
        "tipo": "decodables",
        "contenido": "silent-e-g1.json",
        "html": lambda: decodables.html(comun.leer_json(comun.CONTENIDO / "silent-e-g1.json")),
        "colores": decodables.COLORES,
        "muestras": [0, 2, 3, 6],
        "ficha": {
            "titulo": "Silent e Decodable Passages 1st Grade | CVCe Reading Fluency | Science of Reading",
            "grados": ["1st"], "materias": ["Phonics", "Reading"], "estandares": ["RF.1.3c", "RF.1.4"],
            "precio_usd": 3.00,
            "portada": {"grado": "GRADE 1", "linea1": "Silent e", "linea2": "Decodable Passages",
                        "detalle": "5 stories · a_e i_e o_e u_e · Answer key"},
            "insignias": ["Science of Reading", "100% Decodable", "Answer Key"],
        },
    },
}
