"""Sube el video a YouTube usando la API de datos v3 con un refresh token OAuth."""

import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

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


def subir(ruta_mp4: str, titulo: str, descripcion: str, tags: list[str], config: dict) -> str:
    """Sube el video y devuelve la URL pública."""
    youtube = _cliente()
    body = {
        "snippet": {
            "title": titulo[:100],
            "description": descripcion + "\n\n#Shorts",
            "tags": (tags + config["canal"]["tags_base"])[:30],
            "categoryId": config["canal"]["categoria_youtube"],
            "defaultLanguage": config["idioma"],
            "defaultAudioLanguage": config["idioma"],
        },
        "status": {
            "privacyStatus": config["canal"]["privacidad"],
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(ruta_mp4, mimetype="video/mp4", resumable=True, chunksize=8 * 1024 * 1024)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Subiendo... {int(status.progress() * 100)}%")

    video_id = response["id"]
    url = f"https://www.youtube.com/shorts/{video_id}"
    print(f"Publicado: {url}")
    return url
