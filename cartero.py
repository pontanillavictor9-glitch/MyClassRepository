"""
Agente 3 — CARTERO

Manda el primer email (con las respuestas ya escritas dentro) y, si no hay
contestación en unos días, UN seguimiento. Nunca más de eso.

Por defecto NO manda nada: deja los emails en datos/buzon_salida/ para revisarlos
(.eml, se abren con doble clic). Para mandar de verdad:

    python cartero.py --enviar

Variables: SMTP_HOST, SMTP_PORT (587), SMTP_USUARIO, SMTP_CLAVE, EMAIL_REMITENTE,
REMITENTE_NOMBRE, MARCA, DIRECCION_POSTAL (obligatoria por ley), LIMITE_DIARIO (30),
DIAS_SEGUIMIENTO (4).

Ley de EE. UU. (CAN-SPAM) que se cumple aquí: remitente y asunto veraces,
dirección postal física, forma clara de darse de baja que se respeta para
siempre (lista de supresión), y nada de engañar.
"""

import argparse
import json
import os
import random
import smtplib
import ssl
import time
from datetime import datetime, timedelta
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

import comun

LIMITE_DIARIO = int(os.environ.get("LIMITE_DIARIO", "30"))
DIAS_SEGUIMIENTO = int(os.environ.get("DIAS_SEGUIMIENTO", "4"))


def pie():
    return (f"\n\n{comun.REMITENTE_NOMBRE}\n{comun.MARCA}\n\n--\n"
            f"{comun.MARCA} · {comun.DIRECCION_POSTAL}\n"
            "Not interested? Just reply \"no thanks\" and you won't hear from us again.")


def bloque_respuestas(p):
    trozos = []
    for r in p["borrador"]["respuestas"]:
        trozos.append(f"— Reply to {r['autor'] or 'a recent review'}:\n{r['respuesta'].strip()}")
    return "\n\n".join(trozos)


def componer(p, tipo):
    b = p["borrador"]
    msg = EmailMessage()
    msg["From"] = f"{comun.REMITENTE_NOMBRE} at {comun.MARCA} <{comun.EMAIL_REMITENTE}>"
    msg["To"] = p["email"]
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=comun.EMAIL_REMITENTE.split("@")[-1])
    msg["List-Unsubscribe"] = f"<mailto:{comun.EMAIL_REMITENTE}?subject=unsubscribe>"
    if tipo == "primero":
        msg["Subject"] = b["asunto"]
        texto = b["cuerpo"].replace("{{RESPUESTAS}}", bloque_respuestas(p))
    else:
        msg["Subject"] = "Re: " + b["asunto"]
        msg["In-Reply-To"] = p.get("message_id", "")
        msg["References"] = p.get("message_id", "")
        texto = b["seguimiento"]
    msg.set_content(texto.strip() + pie())
    return msg


def enviados_hoy():
    if not comun.REGISTRO.exists():
        return 0
    return sum(1 for l in comun.REGISTRO.read_text(encoding="utf-8").splitlines()
               if l.startswith('{"fecha": "' + comun.hoy()))


def _smtp():
    s = smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", "587")), timeout=60)
    s.starttls(context=ssl.create_default_context())
    s.login(os.environ["SMTP_USUARIO"], os.environ["SMTP_CLAVE"])
    return s


def pendientes(prospectos, ahora=None):
    """Lista de (prospecto, tipo) que toca mandar hoy, por orden."""
    ahora = ahora or datetime.now()
    cola = []
    for p in prospectos.values():
        if comun.esta_suprimido(p.get("email")):
            continue
        if p["estado"] == "enviado" and p.get("enviado"):
            if ahora - datetime.fromisoformat(p["enviado"]) >= timedelta(days=DIAS_SEGUIMIENTO):
                cola.append((p, "seguimiento"))
    for p in prospectos.values():
        if p["estado"] == "listo" and not comun.esta_suprimido(p.get("email")):
            cola.append((p, "primero"))
    return cola


def repartir(de_verdad=False):
    if de_verdad and "[" in comun.DIRECCION_POSTAL:
        raise SystemExit("Falta DIRECCION_POSTAL: la ley de EE. UU. obliga a poner una dirección postal real.")
    prospectos = comun.cargar_prospectos()
    cupo = max(LIMITE_DIARIO - (enviados_hoy() if de_verdad else 0), 0)
    cola = pendientes(prospectos)[:cupo]
    conexion = _smtp() if de_verdad and cola else None
    hechos = []
    try:
        for i, (p, tipo) in enumerate(cola):
            msg = componer(p, tipo)
            if not de_verdad:
                carpeta = comun.BUZON_SALIDA / comun.hoy()
                carpeta.mkdir(parents=True, exist_ok=True)
                (carpeta / f"{comun.slug(p['nombre'])[:40]}-{tipo}.eml").write_bytes(bytes(msg))
                hechos.append((p["nombre"], tipo))
                continue
            conexion.send_message(msg)
            if tipo == "primero":
                p["estado"], p["enviado"], p["message_id"] = "enviado", comun.ahora(), msg["Message-ID"]
            else:
                p["estado"], p["seguimiento"] = "seguimiento", comun.ahora()
            comun.guardar_prospectos(prospectos)
            with comun.REGISTRO.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"fecha": comun.ahora(), "email": p["email"], "tipo": tipo,
                                    "negocio": p["nombre"]}, ensure_ascii=False) + "\n")
            hechos.append((p["nombre"], tipo))
            if i < len(cola) - 1:
                time.sleep(random.uniform(40, 120))   # espaciados, como una persona
    finally:
        if conexion:
            conexion.quit()
    return hechos


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--enviar", action="store_true", help="mandar de verdad")
    x = a.parse_args()
    hechos = repartir(x.enviar)
    for nombre, tipo in hechos:
        print(f"  {tipo:11} {nombre}")
    print(f"{len(hechos)} emails {'enviados' if x.enviar else 'preparados en ' + str(comun.BUZON_SALIDA)}.")


if __name__ == "__main__":
    main()
