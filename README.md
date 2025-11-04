# Video Sorter & YouTube Uploader

🎬 **Repository GitHub**: https://github.com/youpaki/video-sorter-youtube-uploader

Un programme Python avec interface graphique pour trier des vidéos en utilisant un modèle de vision AI et les uploader automatiquement sur YouTube.

## Fonctionnalités

- 🎬 Sélection de dossiers contenant des vidéos
- 🤖 Tri automatique des vidéos via un modèle de vision AI (API à http://trenas.fr:1234)
- ✏️ Critères de tri personnalisables par l'utilisateur
- 📝 Liste modifiable des vidéos (ajout/suppression)
- 📤 Upload automatique sur YouTube avec paramètres personnalisables
- 🔒 Support de différents niveaux de visibilité (Public/Privé/Non répertorié)

## Prérequis

- Python 3.8+
- Chrome/Chromium installé
- Compte YouTube/Google

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python main.py
```

1. Ajoutez des dossiers contenant vos vidéos
2. Définissez vos critères de tri
3. Lancez l'analyse des vidéos
4. Modifiez la liste si nécessaire
5. Configurez les paramètres YouTube
6. Lancez l'upload

## Structure du projet

```
.
├── main.py                 # Point d'entrée principal
├── ui/
│   └── app.py             # Interface graphique
├── modules/
│   ├── vision_api.py      # Communication avec le modèle de vision
│   ├── video_sorter.py    # Logique de tri des vidéos
│   └── youtube_uploader.py # Upload automatique sur YouTube
├── requirements.txt        # Dépendances
└── README.md              # Documentation
```

## Technologies utilisées

- **Tkinter**: Interface graphique
- **Requests**: Communication avec l'API de vision
- **Selenium**: Automatisation de l'upload YouTube
- **OpenCV**: Extraction de frames vidéo
- **Pillow**: Manipulation d'images

## Note

Ce programme utilise l'automatisation du navigateur (Selenium) pour uploader sur YouTube, ce qui ne nécessite pas d'API key ou de configuration Google Cloud Console.
