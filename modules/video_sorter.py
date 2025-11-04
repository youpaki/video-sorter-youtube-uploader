"""
Video Sorter Module
Gère le tri des vidéos selon les critères définis
"""

import os
from typing import List, Dict, Any
from pathlib import Path


class VideoSorter:
    SUPPORTED_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
    
    def __init__(self):
        """Initialise le trieur de vidéos"""
        self.videos = []
        self.analyzed_videos = []
        
    def scan_folders(self, folder_paths: List[str]) -> List[str]:
        """
        Scanne les dossiers pour trouver toutes les vidéos
        
        Args:
            folder_paths: Liste des chemins de dossiers à scanner
            
        Returns:
            Liste des chemins de vidéos trouvées
        """
        video_files = []
        
        for folder_path in folder_paths:
            if not os.path.exists(folder_path):
                print(f"Dossier inexistant: {folder_path}")
                continue
                
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    ext = os.path.splitext(file)[1].lower()
                    
                    if ext in self.SUPPORTED_EXTENSIONS:
                        video_files.append(file_path)
        
        self.videos = video_files
        return video_files
    
    def sort_videos_by_score(self, analyzed_videos: List[Dict[str, Any]], 
                            ascending: bool = False) -> List[Dict[str, Any]]:
        """
        Trie les vidéos analysées par score
        
        Args:
            analyzed_videos: Liste des vidéos avec leurs analyses
            ascending: Si True, trie par ordre croissant, sinon décroissant
            
        Returns:
            Liste triée des vidéos
        """
        return sorted(analyzed_videos, 
                     key=lambda x: x.get('score', 0), 
                     reverse=not ascending)
    
    def filter_videos_by_score(self, analyzed_videos: List[Dict[str, Any]], 
                               min_score: int = 0, 
                               max_score: int = 100) -> List[Dict[str, Any]]:
        """
        Filtre les vidéos par score
        
        Args:
            analyzed_videos: Liste des vidéos avec leurs analyses
            min_score: Score minimum
            max_score: Score maximum
            
        Returns:
            Liste filtrée des vidéos
        """
        return [v for v in analyzed_videos 
                if min_score <= v.get('score', 0) <= max_score]
    
    def get_video_info(self, video_path: str) -> Dict[str, Any]:
        """
        Récupère les informations d'une vidéo
        
        Args:
            video_path: Chemin vers la vidéo
            
        Returns:
            Dictionnaire avec les informations de la vidéo
        """
        try:
            stat = os.stat(video_path)
            return {
                'path': video_path,
                'filename': os.path.basename(video_path),
                'size': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'exists': True
            }
        except Exception as e:
            return {
                'path': video_path,
                'filename': os.path.basename(video_path),
                'error': str(e),
                'exists': False
            }
    
    def get_video_count(self) -> int:
        """
        Retourne le nombre de vidéos trouvées
        
        Returns:
            Nombre de vidéos
        """
        return len(self.videos)
    
    def remove_video(self, video_path: str) -> bool:
        """
        Retire une vidéo de la liste
        
        Args:
            video_path: Chemin de la vidéo à retirer
            
        Returns:
            True si la vidéo a été retirée, False sinon
        """
        if video_path in self.videos:
            self.videos.remove(video_path)
            return True
        return False
    
    def add_video(self, video_path: str) -> bool:
        """
        Ajoute une vidéo à la liste
        
        Args:
            video_path: Chemin de la vidéo à ajouter
            
        Returns:
            True si la vidéo a été ajoutée, False sinon
        """
        if os.path.exists(video_path) and video_path not in self.videos:
            ext = os.path.splitext(video_path)[1].lower()
            if ext in self.SUPPORTED_EXTENSIONS:
                self.videos.append(video_path)
                return True
        return False
