"""Lee los videos ya subidos al canal y guarda sus títulos en
content/canal_existente.json, para que el generador nunca repita un caso
que ya está publicado en YouTube."""

import json
import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

CANAL_PATH = "content/canal_existente.json"
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]


def _cliente():
    creds = Credentials(
        token=None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        scopes=SCOPES,
    )
    return build("youtube", "v3", credentials=creds)


def sincronizar() -> list[str]:
    """Devuelve los títulos de todos los videos del canal y los guarda en disco.
    Si falla (p. ej. el token no tiene permiso de lectura), devuelve lo último guardado."""
    try:
        youtube = _cliente()
        canal = youtube.channels().list(part="contentDetails", mine=True).execute()
        uploads = canal["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        titulos = []
        page_token = None
        while True:
            resp = youtube.playlistItems().list(
                part="snippet", playlistId=uploads, maxResults=50, pageToken=page_token
            ).execute()
            titulos += [item["snippet"]["title"] for item in resp.get("items", [])]
            page_token = resp.get("nextPageToken")
            if not page_token:
                break

        with open(CANAL_PATH, "w", encoding="utf-8") as f:
            json.dump({"titulos": titulos}, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Canal sincronizado: {len(titulos)} videos ya publicados")
        return titulos
    except Exception as e:
        print(f"Aviso: no se pudo leer el canal ({e}). Se usa la última copia local.")
        return titulos_guardados()


def titulos_guardados() -> list[str]:
    if os.path.exists(CANAL_PATH):
        with open(CANAL_PATH, encoding="utf-8") as f:
            return json.load(f).get("titulos", [])
    return []
