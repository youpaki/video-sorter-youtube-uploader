"""
YouTube Uploader Module
Upload automatique des vidéos sur YouTube via Selenium (sans API officielle)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from typing import Dict, Any, Optional, Callable


class YouTubeUploader:
    def __init__(self):
        """Initialise l'uploader YouTube"""
        self.driver = None
        self.logged_in = False
        
    def setup_driver(self, headless: bool = False) -> webdriver.Chrome:
        """
        Configure et retourne un driver Chrome
        
        Args:
            headless: Si True, lance Chrome en mode headless
            
        Returns:
            Instance du driver Chrome
        """
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Désactiver la détection de webdriver
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Masquer le fait que c'est un webdriver
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.driver = driver
        return driver
    
    def login_to_youtube(self, email: str, password: str, 
                        callback: Optional[Callable[[str], None]] = None) -> bool:
        """
        Se connecte à YouTube/Google
        
        Args:
            email: Email du compte Google
            password: Mot de passe du compte
            callback: Fonction de callback pour les messages de statut
            
        Returns:
            True si connexion réussie, False sinon
        """
        try:
            if callback:
                callback("Ouverture de la page de connexion...")
            
            self.driver.get("https://accounts.google.com/signin")
            time.sleep(2)
            
            if callback:
                callback("Saisie de l'email...")
            
            # Saisir l'email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
            )
            email_field.send_keys(email)
            
            # Cliquer sur suivant
            next_button = self.driver.find_element(By.ID, "identifierNext")
            next_button.click()
            time.sleep(3)
            
            if callback:
                callback("Saisie du mot de passe...")
            
            # Saisir le mot de passe
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
            password_field.send_keys(password)
            
            # Cliquer sur suivant
            next_button = self.driver.find_element(By.ID, "passwordNext")
            next_button.click()
            time.sleep(5)
            
            # Vérifier si la connexion a réussi
            if "myaccount.google.com" in self.driver.current_url or "youtube.com" in self.driver.current_url:
                self.logged_in = True
                if callback:
                    callback("Connexion réussie!")
                return True
            else:
                if callback:
                    callback("Échec de la connexion. Vérifiez vos identifiants.")
                return False
                
        except Exception as e:
            if callback:
                callback(f"Erreur lors de la connexion: {str(e)}")
            return False
    
    def upload_video(self, video_path: str, title: str, description: str = "",
                    visibility: str = "private", category: str = "22",
                    callback: Optional[Callable[[str], None]] = None) -> Dict[str, Any]:
        """
        Upload une vidéo sur YouTube
        
        Args:
            video_path: Chemin vers la vidéo
            title: Titre de la vidéo
            description: Description de la vidéo
            visibility: "public", "private" ou "unlisted"
            category: ID de la catégorie (22 = People & Blogs par défaut)
            callback: Fonction de callback pour les messages de statut
            
        Returns:
            Dictionnaire avec le statut de l'upload
        """
        try:
            if not self.logged_in:
                return {
                    "success": False,
                    "error": "Non connecté. Veuillez vous connecter d'abord."
                }
            
            if not os.path.exists(video_path):
                return {
                    "success": False,
                    "error": f"Fichier introuvable: {video_path}"
                }
            
            if callback:
                callback(f"Début de l'upload: {os.path.basename(video_path)}...")
            
            # Aller sur la page d'upload YouTube
            self.driver.get("https://www.youtube.com/upload")
            time.sleep(3)
            
            if callback:
                callback("Sélection du fichier...")
            
            # Trouver et cliquer sur le bouton de sélection de fichier
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            
            # Envoyer le chemin du fichier
            file_input.send_keys(os.path.abspath(video_path))
            time.sleep(5)
            
            if callback:
                callback("Configuration des détails de la vidéo...")
            
            # Attendre que le titre soit modifiable
            title_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#textbox"))
            )
            
            # Effacer et saisir le titre
            title_field.clear()
            time.sleep(1)
            title_field.send_keys(title)
            
            # Saisir la description si le champ existe
            try:
                description_fields = self.driver.find_elements(By.CSS_SELECTOR, "#textbox")
                if len(description_fields) > 1:
                    description_fields[1].send_keys(description)
            except:
                pass
            
            time.sleep(2)
            
            if callback:
                callback("Passage à l'étape suivante...")
            
            # Cliquer sur "Suivant" plusieurs fois
            for _ in range(3):
                try:
                    next_button = self.driver.find_element(By.ID, "next-button")
                    next_button.click()
                    time.sleep(2)
                except:
                    pass
            
            if callback:
                callback(f"Configuration de la visibilité: {visibility}...")
            
            # Sélectionner la visibilité
            try:
                visibility_map = {
                    "private": "PRIVATE",
                    "unlisted": "UNLISTED",
                    "public": "PUBLIC"
                }
                
                visibility_value = visibility_map.get(visibility.lower(), "PRIVATE")
                
                radio_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR, 
                        f"tp-yt-paper-radio-button[name='{visibility_value}']"
                    ))
                )
                radio_button.click()
                time.sleep(2)
            except:
                if callback:
                    callback("Impossible de définir la visibilité, utilisation de la valeur par défaut")
            
            if callback:
                callback("Finalisation de l'upload...")
            
            # Cliquer sur "Publier" ou "Enregistrer"
            try:
                done_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "done-button"))
                )
                done_button.click()
                time.sleep(5)
                
                if callback:
                    callback("✓ Upload terminé avec succès!")
                
                return {
                    "success": True,
                    "video_path": video_path,
                    "title": title
                }
            except:
                if callback:
                    callback("Erreur lors de la finalisation")
                return {
                    "success": False,
                    "error": "Impossible de finaliser l'upload"
                }
                
        except Exception as e:
            if callback:
                callback(f"Erreur: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "video_path": video_path
            }
    
    def upload_multiple_videos(self, videos: list, 
                              visibility: str = "private",
                              category: str = "22",
                              callback: Optional[Callable[[str], None]] = None) -> list:
        """
        Upload plusieurs vidéos
        
        Args:
            videos: Liste de dictionnaires avec 'path', 'title', 'description'
            visibility: Visibilité par défaut
            category: Catégorie par défaut
            callback: Fonction de callback pour les messages
            
        Returns:
            Liste des résultats d'upload
        """
        results = []
        
        for i, video in enumerate(videos):
            if callback:
                callback(f"\n=== Upload {i+1}/{len(videos)} ===")
            
            result = self.upload_video(
                video_path=video.get('path'),
                title=video.get('title', os.path.basename(video.get('path'))),
                description=video.get('description', ''),
                visibility=visibility,
                category=category,
                callback=callback
            )
            
            results.append(result)
            
            if result.get('success'):
                if callback:
                    callback(f"✓ Vidéo {i+1} uploadée avec succès\n")
            else:
                if callback:
                    callback(f"✗ Échec de l'upload de la vidéo {i+1}\n")
            
            time.sleep(3)
        
        return results
    
    def close(self):
        """Ferme le driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.logged_in = False
