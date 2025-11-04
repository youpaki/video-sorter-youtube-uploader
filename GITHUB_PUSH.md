# Instructions pour pousser vers GitHub

## Étape 1: Créer un repository GitHub

1. Allez sur https://github.com/new
2. Nommez votre repository (ex: "video-sorter-youtube-uploader")
3. Laissez-le PUBLIC ou PRIVATE selon votre choix
4. **NE PAS** initialiser avec README, .gitignore ou LICENSE (nous les avons déjà)
5. Cliquez sur "Create repository"

## Étape 2: Pousser le code

Une fois le repository créé, GitHub vous donnera des commandes. Utilisez celles pour un repository existant:

```bash
cd "/Users/seoo/Desktop/prgms/script video upload"
git remote add origin https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
git branch -M main
git push -u origin main
```

**OU avec SSH (si configuré):**

```bash
cd "/Users/seoo/Desktop/prgms/script video upload"
git remote add origin git@github.com:VOTRE_USERNAME/VOTRE_REPO.git
git branch -M main
git push -u origin main
```

## Alternative: Créer le repository en ligne de commande (avec GitHub CLI)

Si vous avez installé GitHub CLI (`gh`):

```bash
cd "/Users/seoo/Desktop/prgms/script video upload"
gh repo create video-sorter-youtube-uploader --public --source=. --remote=origin --push
```

## Commits actuels

Voici ce qui a été commité:

1. **Commit initial** (930dafe):
   - Interface graphique avec Tkinter
   - Module de vision AI pour analyser les vidéos
   - Système de tri personnalisable
   - Upload automatique sur YouTube via Selenium
   - Compatible Windows

2. **Documentation et outils** (dcc582c):
   - Script run.bat pour Windows
   - Documentation WINDOWS_SETUP.md
   - Script de test test_setup.py
   - Licence MIT

## Structure finale du projet

```
.
├── .env.example          # Exemple de configuration
├── .gitignore           # Fichiers à ignorer
├── LICENSE              # Licence MIT
├── README.md            # Documentation principale
├── WINDOWS_SETUP.md     # Instructions Windows
├── main.py              # Point d'entrée
├── requirements.txt     # Dépendances Python
├── run.bat             # Script de lancement Windows
├── test_setup.py       # Script de test
├── modules/
│   ├── __init__.py
│   ├── video_sorter.py     # Tri des vidéos
│   ├── vision_api.py       # API de vision
│   └── youtube_uploader.py # Upload YouTube
└── ui/
    ├── __init__.py
    └── app.py              # Interface graphique
```

## Note importante

⚠️ **Avant de pousser**, assurez-vous que votre `.gitignore` est correct pour ne pas inclure:
- Les identifiants dans `.env`
- Les fichiers `__pycache__`
- L'environnement virtuel `venv/`

Ces éléments sont déjà dans le `.gitignore` fourni.
