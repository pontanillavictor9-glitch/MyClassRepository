"""
Agente 4 — CARTERO

Monta y manda el email de cada cliente con las licitaciones que le preparó el
Emparejador.

Por defecto NO manda nada: deja cada email en datos/buzon_salida/AAAA-MM-DD/
para revisarlo (se abre con doble clic, es un .eml). Para mandar de verdad:

    python cartero.py --enviar

y antes hay que poner estas variables de entorno (las da tu proveedor de correo):
    SMTP_HOST, SMTP_PORT (normalmente 587), SMTP_USUARIO, SMTP_CLAVE, EMAIL_REMITENTE

Cada email lleva, por ley (LSSI), quién lo manda y un enlace de baja de un clic.
"""

import argparse
import json
import os
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from html import escape

import comun


def enviar_email(destino, asunto, texto, html=None, baja_url=None, de_verdad=False, carpeta=None):
    """Manda un email (de_verdad=True) o lo guarda como .eml para revisarlo."""
    msg = EmailMessage()
    msg["From"] = f"{comun.NOMBRE_SERVICIO} <{comun.EMAIL_REMITENTE}>"
    msg["To"] = destino
    msg["Subject"] = asunto
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()
    if baja_url:
        msg["List-Unsubscribe"] = f"<{baja_url}>"
        msg["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"
    msg.set_content(texto)
    if html:
        msg.add_alternative(html, subtype="html")

    if not de_verdad:
        carpeta = carpeta or comun.BUZON_SALIDA / comun.hoy()
        carpeta.mkdir(parents=True, exist_ok=True)
        f = carpeta / f"{comun.slug(destino)}-{comun.slug(asunto)[:40]}.eml"
        f.write_bytes(bytes(msg))
        return f

    host = os.environ["SMTP_HOST"]
    puerto = int(os.environ.get("SMTP_PORT", "587"))
    with smtplib.SMTP(host, puerto, timeout=60) as s:
        s.starttls(context=ssl.create_default_context())
        s.login(os.environ["SMTP_USUARIO"], os.environ["SMTP_CLAVE"])
        s.send_message(msg)
    return None


def _fecha_bonita(t):
    """2026-11-20T14:00:00 -> 20/11/2026 a las 14:00"""
    if not t:
        return "no indicado"
    fecha, _, hora = t.partition("T")
    a, m, d = (fecha.split("-") + ["", ""])[:3]
    return f"{d}/{m}/{a}" + (f" a las {hora[:5]}" if hora else "")


def _bloque(lic):
    an = comun.analisis_de(lic) or {}
    return {
        "titulo": lic.get("objeto") or lic.get("titulo") or "Licitación",
        "organo": lic.get("organo") or "",
        "importe": comun.euros(lic.get("importe_sin_iva")),
        "provincia": lic.get("provincia") or "España",
        "plazo": _fecha_bonita(lic.get("fin_plazo")),
        "resumen": an.get("resumen", ""),
        "requisitos": an.get("requisitos", []),
        "dificultad": an.get("dificultad"),
        "enlace": lic.get("enlace") or "",
    }


def componer(cli, lics):
    gratis = cli.get("plan") != "pago"
    baja = f"{comun.URL_WEB}/baja?t={cli['token']}"
    n = len(lics)
    asunto = (f"{n} licitación{'es' if n != 1 else ''} para ti"
              + (" esta semana" if gratis else " hoy"))
    bloques = [_bloque(l) for l in lics]

    # --- texto plano ---
    lineas = [f"Hola{(' ' + cli['nombre']) if cli.get('nombre') else ''},", "",
              f"Estas son las licitaciones abiertas que encajan con tu empresa:", ""]
    for i, b in enumerate(bloques, 1):
        lineas += [f"{i}. {b['titulo']}",
                   f"   {b['organo']} · {b['provincia']} · {b['importe']} · plazo: {b['plazo']}"]
        if b["resumen"]:
            lineas.append(f"   {b['resumen']}")
        if b["enlace"]:
            lineas.append(f"   {b['enlace']}")
        lineas.append("")
    if gratis:
        lineas += ["Estás en el plan gratis: 3 licitaciones a la semana.",
                   "Con el plan completo las recibes todas, cada mañana, con requisitos y dificultad.",
                   comun.ENLACE_PAGO or f"{comun.URL_WEB}/#precios", ""]
    lineas += ["--", f"{comun.NOMBRE_SERVICIO} · {comun.TITULAR}",
               f"Recibes esto porque te suscribiste. Darte de baja: {baja}"]
    texto = "\n".join(lineas)

    # --- HTML ---
    tarjetas = []
    for b in bloques:
        req = "".join(f"<li>{escape(r)}</li>" for r in b["requisitos"][:4])
        tarjetas.append(f"""
<div style="border:1px solid #e3e6ea;border-radius:10px;padding:16px;margin:0 0 14px">
 <div style="font-size:16px;font-weight:700;color:#14213d">{escape(b['titulo'])}</div>
 <div style="color:#5b6573;font-size:13px;margin:4px 0 10px">{escape(b['organo'])} · {escape(b['provincia'])}</div>
 <div style="font-size:14px"><b>{escape(b['importe'])}</b> sin IVA · plazo: <b>{escape(b['plazo'])}</b>
 {f" · dificultad {escape(b['dificultad'])}" if b['dificultad'] and not gratis else ""}</div>
 {f'<p style="font-size:14px;line-height:1.5;margin:10px 0">{escape(b["resumen"])}</p>' if b['resumen'] else ''}
 {f'<ul style="font-size:13px;color:#333;margin:0 0 8px">{req}</ul>' if req and not gratis else ''}
 {f'<a href="{escape(b["enlace"])}" style="color:#1d4ed8;font-size:14px">Ver la licitación oficial →</a>' if b['enlace'] else ''}
</div>""")
    promo = ""
    if gratis:
        promo = f"""<div style="background:#fff7e6;border-radius:10px;padding:16px;margin:8px 0 18px;font-size:14px">
 Estás en el <b>plan gratis</b> (3 a la semana). Con el plan completo recibes <b>todas</b>, cada mañana,
 con requisitos y dificultad. <a href="{escape(comun.ENLACE_PAGO or comun.URL_WEB + '/#precios')}">Pasarme al plan completo</a></div>"""
    html = f"""<!doctype html><html><body style="margin:0;background:#f5f6f8;font-family:Arial,Helvetica,sans-serif;color:#1f2933">
<div style="max-width:620px;margin:0 auto;padding:24px 16px">
 <div style="font-size:20px;font-weight:700;color:#14213d;margin-bottom:6px">{escape(comun.NOMBRE_SERVICIO)}</div>
 <p style="font-size:15px">Hola{escape(' ' + cli['nombre']) if cli.get('nombre') else ''}, estas son las licitaciones abiertas que encajan contigo:</p>
 {''.join(tarjetas)}
 {promo}
 <p style="font-size:12px;color:#7b8794;line-height:1.5">{escape(comun.NOMBRE_SERVICIO)} · {escape(comun.TITULAR)}<br>
 Recibes este email porque te suscribiste. <a href="{escape(baja)}" style="color:#7b8794">Darme de baja</a></p>
</div></body></html>"""
    return asunto, texto, html, baja


def repartir(fecha=None, de_verdad=False):
    fecha = fecha or comun.hoy()
    carpeta = comun.ENVIOS / fecha
    clientes = {c["id"]: c for c in comun.cargar_clientes()}
    hechos = []
    for f in sorted(carpeta.glob("*.json")):
        envio = json.loads(f.read_text(encoding="utf-8"))
        cli = clientes.get(envio["cliente"])
        if not cli or cli.get("estado") != "activo" or not envio["licitaciones"]:
            continue
        if envio.get("enviado") and de_verdad:
            continue                       # ya se mandó hoy: no repetir
        asunto, texto, html, baja = componer(cli, envio["licitaciones"])
        destino = enviar_email(cli["email"], asunto, texto, html, baja, de_verdad,
                               comun.BUZON_SALIDA / fecha)
        if de_verdad:
            cli.setdefault("enviados", []).extend(l["id"] for l in envio["licitaciones"])
            cli["enviados"] = cli["enviados"][-5000:]
            envio["enviado"] = True
            f.write_text(json.dumps(envio, ensure_ascii=False, indent=1), encoding="utf-8")
        hechos.append((cli["email"], len(envio["licitaciones"]), destino))
    if de_verdad and hechos:
        comun.guardar_clientes(list(clientes.values()))
    return hechos


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--enviar", action="store_true", help="mandar de verdad (si no, solo se guardan para revisar)")
    a = p.parse_args()
    for email, n, destino in repartir(de_verdad=a.enviar):
        print(f"  {email}: {n} licitaciones" + (f" → {destino}" if destino else " (enviado)"))


if __name__ == "__main__":
    main()
