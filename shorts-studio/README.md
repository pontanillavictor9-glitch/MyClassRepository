# 🎬 Shorts Studio

Idea nueva: un mini-proyecto para crear **YouTube Shorts con IA** — sin mostrar
tu cara y sin usar tu voz.

## ¿Qué hay aquí?

| Archivo | Qué es |
|---|---|
| `PLAYBOOK.md` | La guía completa de 7 pasos con todos los prompts explicados |
| `shorts_studio.py` | Script que genera los 7 prompts ya rellenados con tu tema |

## Cómo usarlo

```bash
cd shorts-studio
python shorts_studio.py
```

El script te pregunta tu tema, audiencia, edad e intereses, y crea un archivo
`mi-short-<tema>.md` con los 7 prompts listos para pegar en Claude o ChatGPT:

1. **Nicho** — elegir el nicho con mejor CPM
2. **Guion** — guion de 45 segundos con gancho y llamado a la acción
3. **Ganchos** — 20 primeras líneas para no perder al espectador
4. **Títulos** — 15 títulos con análisis de potencial viral
5. **Voz IA** — guion adaptado para ElevenLabs (pausas, acentos, emociones)
6. **Retención** — versión optimizada segundo a segundo
7. **SEO** — descripción de YouTube con palabras clave y hashtags

No necesita instalar nada: solo Python (sin librerías externas).
