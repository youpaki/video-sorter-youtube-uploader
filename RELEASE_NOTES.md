# Release Notes

## Version 1.0.0

### Initial Release

Application complète pour le tri automatique de vidéos par analyse IA et upload YouTube.

### Fonctionnalités principales

- Analyse automatique de vidéos via modèle de vision
- Tri personnalisable selon critères définis par l'utilisateur
- Interface graphique multi-plateforme (Tkinter)
- Upload automatique sur YouTube sans API officielle (Selenium)
- Gestion de liste avec ajout/suppression manuelle

### Formats supportés

MP4, AVI, MOV, MKV, WMV, FLV, WEBM

### Configuration requise

- Python 3.8+
- Google Chrome
- Connexion internet pour l'API de vision
- Compte Google/YouTube pour l'upload

### Compilation

Exécutables compilés disponibles pour:
- macOS (Intel/Apple Silicon)
- Windows (via PyInstaller)

### Build depuis les sources

```bash
pip install -r requirements.txt
pyinstaller build.spec
```

### Limitations connues

- Une frame analysée par vidéo (1 seconde)
- Requiert authentification manuelle pour 2FA Google
- L'API de vision doit être accessible à http://trenas.fr:1234

### Dépendances principales

- selenium 4.15.2
- opencv-python 4.8.1.78
- requests 2.31.0
- pillow 10.1.0
- webdriver-manager 4.0.1
