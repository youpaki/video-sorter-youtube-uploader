"""
Vision API Module
Communique avec le modèle de vision à http://trenas.fr:1234
"""

import requests
import base64
import json
from typing import Dict, Any, Optional
import cv2
import os


class VisionAPI:
    def __init__(self, base_url: str = "http://trenas.fr:1234"):
        """
        Initialise le client API de vision
        
        Args:
            base_url: URL de base de l'API
        """
        self.base_url = base_url
        self.api_url = f"{base_url}/v1/chat/completions"
        
    def extract_frame(self, video_path: str, frame_time: float = 1.0) -> Optional[str]:
        """
        Extrait une frame d'une vidéo et la convertit en base64
        
        Args:
            video_path: Chemin vers la vidéo
            frame_time: Temps en secondes pour extraire la frame
            
        Returns:
            Image encodée en base64 ou None si erreur
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            # Positionner à la frame souhaitée
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_number = int(fps * frame_time)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                return None
            
            # Encoder l'image en JPEG puis en base64
            _, buffer = cv2.imencode('.jpg', frame)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return img_base64
        except Exception as e:
            print(f"Erreur lors de l'extraction de la frame: {e}")
            return None
    
    def analyze_video(self, video_path: str, criteria: str, model: str = "qwen2.5-vl") -> Dict[str, Any]:
        """
        Analyse une vidéo selon les critères donnés
        
        Args:
            video_path: Chemin vers la vidéo
            criteria: Critères d'analyse fournis par l'utilisateur
            model: Nom du modèle à utiliser
            
        Returns:
            Dictionnaire contenant l'analyse
        """
        try:
            # Extraire une frame de la vidéo
            frame_base64 = self.extract_frame(video_path)
            
            if not frame_base64:
                return {
                    "success": False,
                    "error": "Impossible d'extraire une frame de la vidéo",
                    "score": 0,
                    "analysis": ""
                }
            
            # Préparer le prompt
            prompt = f"""Analyse cette image extraite d'une vidéo selon les critères suivants:
{criteria}

Fournis une évaluation et un score de 0 à 100 pour ces critères.
Réponds au format JSON avec les champs: score (0-100), analysis (texte descriptif)."""

            # Préparer la requête
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{frame_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            # Envoyer la requête
            response = requests.post(
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # Essayer de parser le JSON de la réponse
                try:
                    # Chercher le JSON dans la réponse
                    if "{" in content and "}" in content:
                        json_start = content.index("{")
                        json_end = content.rindex("}") + 1
                        json_str = content[json_start:json_end]
                        parsed = json.loads(json_str)
                        
                        return {
                            "success": True,
                            "score": parsed.get("score", 50),
                            "analysis": parsed.get("analysis", content),
                            "video_path": video_path
                        }
                except:
                    pass
                
                # Si le parsing JSON échoue, extraire le score manuellement
                score = 50  # Score par défaut
                if "score" in content.lower():
                    import re
                    numbers = re.findall(r'\d+', content)
                    if numbers:
                        score = min(100, max(0, int(numbers[0])))
                
                return {
                    "success": True,
                    "score": score,
                    "analysis": content,
                    "video_path": video_path
                }
            else:
                return {
                    "success": False,
                    "error": f"Erreur API: {response.status_code}",
                    "score": 0,
                    "analysis": "",
                    "video_path": video_path
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "score": 0,
                "analysis": "",
                "video_path": video_path
            }
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à l'API
        
        Returns:
            True si la connexion fonctionne, False sinon
        """
        try:
            response = requests.get(f"{self.base_url}/v1/models", timeout=5)
            return response.status_code == 200
        except:
            return False
