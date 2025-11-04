# Video Sorter & YouTube Uploader

Application Python pour trier automatiquement des vidéos selon des critères personnalisés via un modèle de vision AI, puis les uploader sur YouTube sans configuration API.

Repository: https://github.com/youpaki/video-sorter-youtube-uploader

## Fonctionnalités

- Scan récursif de dossiers contenant des vidéos
- Analyse automatique via modèle de vision AI (compatible OpenAI-like API)
- Critères de tri entièrement personnalisables
- Interface graphique intuitive avec gestion de liste
- Upload automatique sur YouTube via Selenium (pas d'API Google requise)
- Configuration de visibilité et catégorie par upload

## Installation

### Prérequis

- Python 3.8 ou supérieur
- Google Chrome installé
- Compte Google/YouTube

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Configuration

L'application se connecte par défaut à `http://trenas.fr:1234` pour l'API de vision. Modifiez `modules/vision_api.py` si nécessaire.

## Utilisation

### Lancement

```bash
python main.py
```

Sur Windows, vous pouvez utiliser le script batch fourni:
```cmd
run.bat
```

### Workflow

1. **Scan et tri**
   - Ajoutez un ou plusieurs dossiers contenant vos vidéos
   - Définissez vos critères de tri (texte libre)
   - Lancez l'analyse (extraits une frame par vidéo à 1s)
   - Les vidéos sont automatiquement triées par score (0-100)

2. **Gestion de la liste**
   - Visualisez les résultats dans le tableau
   - Ajoutez ou retirez des vidéos manuellement
   - Vérifiez les scores et analyses

3. **Upload YouTube**
   - Connectez-vous avec vos identifiants Google
   - Configurez la visibilité (private/unlisted/public)
   - Choisissez la catégorie YouTube
   - Lancez l'upload automatique

## Architecture

```
.
├── main.py                     # Point d'entrée
├── requirements.txt            # Dépendances Python
├── run.bat                     # Script de lancement Windows
│
├── modules/
│   ├── vision_api.py          # Client API de vision
│   ├── video_sorter.py        # Logique de tri
│   └── youtube_uploader.py    # Automatisation YouTube (Selenium)
│
└── ui/
    └── app.py                 # Interface Tkinter
```

## Technologies

| Composant | Technologie | Usage |
|-----------|-------------|-------|
| Interface | Tkinter | UI native multi-plateforme |
| Vision AI | Requests | Communication HTTP avec API |
| Vidéo | OpenCV | Extraction de frames |
| Upload | Selenium + ChromeDriver | Automatisation navigateur |
| Images | Pillow | Encodage base64 |

## Formats supportés

MP4, AVI, MOV, MKV, WMV, FLV, WEBM

## Limitations

- L'analyse extrait une seule frame par vidéo (1 seconde)
- L'API de vision doit être accessible et compatible OpenAI format
- L'upload YouTube nécessite une interaction manuelle pour 2FA si activé
- Temps d'analyse: environ 30 secondes par vidéo

## Dépannage

### Erreur de connexion API
Vérifiez que l'API est accessible: `curl http://trenas.fr:1234/v1/models`

### Échec upload YouTube
- Vérifiez vos identifiants
- Si 2FA activé, complétez la vérification dans le navigateur
- Utilisez un mot de passe d'application Google si nécessaire

### Module non trouvé
Réinstallez les dépendances: `pip install -r requirements.txt`

## Licence

MIT License - Voir fichier LICENSE
