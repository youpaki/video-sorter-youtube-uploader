# Installation et utilisation sous Windows

## Prérequis

1. **Python 3.8 ou supérieur**
   - Télécharger depuis https://www.python.org/downloads/
   - ⚠️ Cocher "Add Python to PATH" lors de l'installation

2. **Google Chrome**
   - Télécharger depuis https://www.google.com/chrome/

## Installation rapide

1. Ouvrir PowerShell ou Command Prompt dans le dossier du projet

2. Créer un environnement virtuel (recommandé):
```cmd
python -m venv venv
venv\Scripts\activate
```

3. Installer les dépendances:
```cmd
pip install -r requirements.txt
```

## Lancement

### Méthode 1: Avec le script batch (plus simple)
Double-cliquer sur `run.bat`

### Méthode 2: En ligne de commande
```cmd
python main.py
```

## Utilisation

### Étape 1: Scanner et trier les vidéos

1. Dans l'onglet **"1. Scan & Tri"**:
   - Cliquez sur "Ajouter dossier" pour sélectionner vos dossiers contenant des vidéos
   - Cliquez sur "Scanner" pour détecter toutes les vidéos
   
2. Définissez vos **critères de tri**:
   - Exemple: "Évaluer la qualité visuelle, la présence de personnes, l'esthétique des couleurs"
   - Choisissez le modèle (qwen2.5-vl recommandé)
   
3. Cliquez sur **"Analyser les vidéos"**
   - L'analyse peut prendre plusieurs minutes selon le nombre de vidéos
   - Une barre de progression vous indique l'avancement

### Étape 2: Modifier la liste des vidéos

1. Dans l'onglet **"2. Vidéos"**:
   - Visualisez toutes les vidéos triées par score
   - Retirez les vidéos non désirées (sélection + "Retirer sélectionnées")
   - Ajoutez d'autres vidéos manuellement ("Ajouter vidéo")

### Étape 3: Uploader sur YouTube

1. Dans l'onglet **"3. Upload YouTube"**:
   - Entrez votre **email** et **mot de passe** YouTube/Google
   - Cliquez sur "Se connecter"
   - ⚠️ Un navigateur Chrome s'ouvrira pour la connexion
   
2. Configurez les paramètres:
   - **Visibilité**: Private (privé), Unlisted (non répertorié) ou Public
   - **Catégorie**: 22 (People & Blogs) par défaut
   
3. Cliquez sur **"Uploader les vidéos sur YouTube"**
   - Confirmez l'upload
   - Suivez la progression dans la console

## Résolution de problèmes

### Erreur "Impossible de se connecter à l'API de vision"
- Vérifiez que http://trenas.fr:1234 est accessible
- Testez dans votre navigateur: http://trenas.fr:1234/v1/models

### Erreur lors de l'upload YouTube
- Vérifiez vos identifiants Google
- Si vous avez l'authentification à 2 facteurs, utilisez un mot de passe d'application
- Le navigateur Chrome doit pouvoir s'ouvrir (désactiver le mode headless si nécessaire)

### "Module not found"
- Réinstallez les dépendances: `pip install -r requirements.txt`
- Vérifiez que l'environnement virtuel est activé

### ChromeDriver
- Le ChromeDriver se télécharge automatiquement via webdriver-manager
- En cas de problème, téléchargez-le manuellement: https://chromedriver.chromium.org/

## Notes importantes

- ⚠️ **Authentification Google**: Si vous avez l'authentification à 2 facteurs activée, vous devrez peut-être:
  1. Créer un mot de passe d'application dans votre compte Google
  2. Ou compléter manuellement la vérification 2FA dans le navigateur qui s'ouvre

- 📹 **Formats vidéo supportés**: MP4, AVI, MOV, MKV, WMV, FLV, WEBM

- 🚀 **Performance**: L'analyse des vidéos utilise une frame par vidéo (à 1 seconde)
  Pour des résultats plus précis, le code peut être modifié pour analyser plusieurs frames

- 🔒 **Sécurité**: Ne partagez jamais votre fichier `.env` s'il contient vos identifiants

## Support

En cas de problème, vérifiez:
1. Les logs dans la console de l'application
2. Que toutes les dépendances sont installées
3. Que l'API de vision est accessible
4. Que Chrome est installé et à jour
