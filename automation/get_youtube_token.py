"""Se ejecuta UNA sola vez en tu computadora para obtener el YT_REFRESH_TOKEN.

Pasos previos (ver SETUP.md):
  1. Crea un proyecto en Google Cloud Console y activa "YouTube Data API v3".
  2. Crea credenciales OAuth 2.0 de tipo "Aplicación de escritorio".
  3. Ejecuta:  YT_CLIENT_ID=... YT_CLIENT_SECRET=... python automation/get_youtube_token.py
  4. Autoriza en el navegador con la cuenta de tu canal de YouTube.
  5. Copia el refresh token que se imprime y guárdalo como secreto YT_REFRESH_TOKEN en GitHub.
"""

import os

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": os.environ["YT_CLIENT_ID"],
            "client_secret": os.environ["YT_CLIENT_SECRET"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    },
    SCOPES,
)
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")

print("\n=== GUARDA ESTE VALOR COMO SECRETO 'YT_REFRESH_TOKEN' EN GITHUB ===")
print(creds.refresh_token)
