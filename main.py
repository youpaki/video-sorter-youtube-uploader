"""
Point d'entrée principal de l'application
Video Sorter & YouTube Uploader
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app import main

if __name__ == "__main__":
    main()
