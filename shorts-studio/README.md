# 🎬 Shorts Studio

Idea nueva: un mini-proyecto para crear **YouTube Shorts con IA** — sin mostrar
tu cara y sin usar tu voz.

## ¿Qué hay aquí?

| Archivo | Qué es |
|---|---|
| `PLAYBOOK.md` | La guía completa de 12 pasos (+ bonus) con todos los prompts explicados |
| `shorts_studio.py` | Script que genera todos los prompts ya rellenados con tu tema |

## Cómo usarlo

```bash
cd shorts-studio
python shorts_studio.py
```

El script te pregunta tu tema, audiencia, nicho, suscriptores y más, y crea un
archivo `mi-short-<tema>.md` con los 12 prompts (+ bonus) listos para pegar en
Claude o ChatGPT:

1. **Nicho** — elegir el nicho con mejor CPM
2. **Guion** — guion de 45 segundos con gancho y llamado a la acción
3. **Ganchos** — 20 primeras líneas para no perder al espectador
4. **Títulos** — 15 títulos con análisis de potencial viral
5. **Voz IA** — guion adaptado para ElevenLabs (pausas, acentos, emociones)
6. **Retención** — versión optimizada segundo a segundo
7. **SEO** — descripción con palabra clave, ganchos y 15 hashtags
8. **Ideas** — 30 ideas de Shorts para 30 días
9. **Reciclaje** — convertir 1 video largo en 10 Shorts
10. **Monetización** — 7 formas de monetizar más allá de AdSense
11. **Competencia** — analizar 5 canales que ya funcionan
12. **Calendario** — plan de publicación de 30 días
13. **BONUS** — el prompt maestro: plan completo de 90 días

No necesita instalar nada: solo Python (sin librerías externas).
