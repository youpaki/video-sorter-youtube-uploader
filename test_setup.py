"""
Script de test pour vérifier l'installation et la configuration
"""

import sys
import importlib

def test_imports():
    """Teste l'import de tous les modules nécessaires"""
    print("=== Test des imports ===\n")
    
    modules = [
        ('tkinter', 'Interface graphique'),
        ('requests', 'Requêtes HTTP'),
        ('selenium', 'Automatisation navigateur'),
        ('cv2', 'OpenCV (traitement vidéo)'),
        ('PIL', 'Pillow (traitement d\'images)'),
        ('webdriver_manager', 'Gestion des drivers')
    ]
    
    all_ok = True
    for module_name, description in modules:
        try:
            importlib.import_module(module_name)
            print(f"✓ {module_name:20} - {description}")
        except ImportError as e:
            print(f"✗ {module_name:20} - MANQUANT ({description})")
            all_ok = False
    
    print()
    return all_ok

def test_api_connection():
    """Teste la connexion à l'API de vision"""
    print("=== Test de connexion à l'API ===\n")
    
    try:
        import requests
        response = requests.get("http://trenas.fr:1234/v1/models", timeout=5)
        if response.status_code == 200:
            print("✓ Connexion à l'API de vision réussie")
            print(f"  URL: http://trenas.fr:1234")
            try:
                data = response.json()
                if 'data' in data:
                    print(f"  Modèles disponibles: {len(data['data'])}")
            except:
                pass
            return True
        else:
            print(f"✗ API accessible mais erreur: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Impossible de se connecter à l'API")
        print("  Vérifiez que http://trenas.fr:1234 est accessible")
        return False
    except Exception as e:
        print(f"✗ Erreur lors du test: {str(e)}")
        return False
    finally:
        print()

def test_modules():
    """Teste l'import des modules du projet"""
    print("=== Test des modules du projet ===\n")
    
    try:
        from modules.vision_api import VisionAPI
        print("✓ Module vision_api importé")
    except Exception as e:
        print(f"✗ Erreur module vision_api: {e}")
        return False
    
    try:
        from modules.video_sorter import VideoSorter
        print("✓ Module video_sorter importé")
    except Exception as e:
        print(f"✗ Erreur module video_sorter: {e}")
        return False
    
    try:
        from modules.youtube_uploader import YouTubeUploader
        print("✓ Module youtube_uploader importé")
    except Exception as e:
        print(f"✗ Erreur module youtube_uploader: {e}")
        return False
    
    try:
        from ui.app import VideoSorterApp
        print("✓ Module UI importé")
    except Exception as e:
        print(f"✗ Erreur module UI: {e}")
        return False
    
    print()
    return True

def test_chrome():
    """Teste la disponibilité de Chrome"""
    print("=== Test de Chrome/ChromeDriver ===\n")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        print("Téléchargement/vérification du ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        print("✓ ChromeDriver disponible")
        print()
        return True
    except Exception as e:
        print(f"✗ Erreur ChromeDriver: {e}")
        print()
        return False

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("  TEST DE CONFIGURATION - Video Sorter & YouTube Uploader")
    print("="*60 + "\n")
    
    results = []
    
    # Test des imports
    results.append(("Imports des dépendances", test_imports()))
    
    # Test de l'API
    results.append(("Connexion API vision", test_api_connection()))
    
    # Test des modules
    results.append(("Modules du projet", test_modules()))
    
    # Test de Chrome
    results.append(("Chrome/ChromeDriver", test_chrome()))
    
    # Résumé
    print("="*60)
    print("  RÉSUMÉ")
    print("="*60 + "\n")
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSÉ" if passed else "✗ ÉCHEC"
        print(f"{status:10} - {test_name}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("✓ Tous les tests sont passés!")
        print("  Vous pouvez lancer l'application avec: python main.py")
    else:
        print("✗ Certains tests ont échoué.")
        print("  Installez les dépendances manquantes avec: pip install -r requirements.txt")
    
    print()
    input("Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
