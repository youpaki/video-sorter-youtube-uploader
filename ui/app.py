"""
Interface graphique principale de l'application
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.vision_api import VisionAPI
from modules.video_sorter import VideoSorter
from modules.youtube_uploader import YouTubeUploader


class VideoSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Sorter & YouTube Uploader")
        self.root.geometry("1200x800")
        
        # Initialiser les modules
        self.vision_api = VisionAPI()
        self.video_sorter = VideoSorter()
        self.youtube_uploader = None
        
        # Variables
        self.folders = []
        self.analyzed_videos = []
        self.selected_videos = []
        
        self.create_widgets()
        
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        
        # Notebook (onglets)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Onglet 1: Scan et tri
        self.tab_scan = ttk.Frame(notebook)
        notebook.add(self.tab_scan, text="1. Scan & Tri")
        self.create_scan_tab()
        
        # Onglet 2: Liste des vidéos
        self.tab_videos = ttk.Frame(notebook)
        notebook.add(self.tab_videos, text="2. Vidéos")
        self.create_videos_tab()
        
        # Onglet 3: Upload YouTube
        self.tab_upload = ttk.Frame(notebook)
        notebook.add(self.tab_upload, text="3. Upload YouTube")
        self.create_upload_tab()
        
    def create_scan_tab(self):
        """Crée l'onglet de scan et tri"""
        
        # Frame pour les dossiers
        folders_frame = ttk.LabelFrame(self.tab_scan, text="Dossiers à scanner", padding=10)
        folders_frame.pack(fill='both', expand=False, padx=10, pady=10)
        
        # Liste des dossiers
        self.folders_listbox = tk.Listbox(folders_frame, height=5)
        self.folders_listbox.pack(side='left', fill='both', expand=True)
        
        folders_scrollbar = ttk.Scrollbar(folders_frame, orient='vertical', 
                                         command=self.folders_listbox.yview)
        folders_scrollbar.pack(side='right', fill='y')
        self.folders_listbox.config(yscrollcommand=folders_scrollbar.set)
        
        # Boutons pour gérer les dossiers
        folders_buttons = ttk.Frame(folders_frame)
        folders_buttons.pack(fill='x', pady=5)
        
        ttk.Button(folders_buttons, text="Ajouter dossier", 
                  command=self.add_folder).pack(side='left', padx=5)
        ttk.Button(folders_buttons, text="Retirer dossier", 
                  command=self.remove_folder).pack(side='left', padx=5)
        ttk.Button(folders_buttons, text="Scanner", 
                  command=self.scan_folders).pack(side='left', padx=5)
        
        # Frame pour les critères
        criteria_frame = ttk.LabelFrame(self.tab_scan, text="Critères de tri", padding=10)
        criteria_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(criteria_frame, text="Décrivez vos critères de tri pour les vidéos:").pack(anchor='w')
        
        self.criteria_text = scrolledtext.ScrolledText(criteria_frame, height=8, wrap='word')
        self.criteria_text.pack(fill='both', expand=True, pady=5)
        self.criteria_text.insert('1.0', "Exemple: Évaluer la qualité visuelle, "
                                        "la présence de personnes, l'esthétique des couleurs, "
                                        "et l'intérêt général du contenu.")
        
        # Options de tri
        options_frame = ttk.Frame(criteria_frame)
        options_frame.pack(fill='x', pady=5)
        
        ttk.Label(options_frame, text="Modèle:").pack(side='left', padx=5)
        self.model_var = tk.StringVar(value="qwen2.5-vl")
        model_combo = ttk.Combobox(options_frame, textvariable=self.model_var, 
                                   values=["qwen2.5-vl", "qwen2-vl", "llava"], 
                                   width=15, state='readonly')
        model_combo.pack(side='left', padx=5)
        
        # Bouton pour analyser
        ttk.Button(criteria_frame, text="Analyser les vidéos", 
                  command=self.analyze_videos, 
                  style='Accent.TButton').pack(pady=10)
        
        # Barre de progression
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(criteria_frame, variable=self.progress_var, 
                                           maximum=100)
        self.progress_bar.pack(fill='x', pady=5)
        
        # Label de statut
        self.status_label = ttk.Label(criteria_frame, text="", foreground='blue')
        self.status_label.pack()
        
    def create_videos_tab(self):
        """Crée l'onglet de liste des vidéos"""
        
        # Frame pour les contrôles
        controls_frame = ttk.Frame(self.tab_videos)
        controls_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(controls_frame, text="Vidéos triées par score:").pack(side='left', padx=5)
        
        ttk.Button(controls_frame, text="Ajouter vidéo", 
                  command=self.add_video_manually).pack(side='right', padx=5)
        ttk.Button(controls_frame, text="Retirer sélectionnées", 
                  command=self.remove_selected_videos).pack(side='right', padx=5)
        ttk.Button(controls_frame, text="Rafraîchir", 
                  command=self.refresh_videos_list).pack(side='right', padx=5)
        
        # Treeview pour afficher les vidéos
        tree_frame = ttk.Frame(self.tab_videos)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('Nom', 'Chemin', 'Score', 'Analyse')
        self.videos_tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings')
        
        self.videos_tree.heading('#0', text='#')
        self.videos_tree.heading('Nom', text='Nom du fichier')
        self.videos_tree.heading('Chemin', text='Chemin')
        self.videos_tree.heading('Score', text='Score')
        self.videos_tree.heading('Analyse', text='Analyse')
        
        self.videos_tree.column('#0', width=50)
        self.videos_tree.column('Nom', width=200)
        self.videos_tree.column('Chemin', width=300)
        self.videos_tree.column('Score', width=80)
        self.videos_tree.column('Analyse', width=400)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient='vertical', command=self.videos_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.videos_tree.xview)
        self.videos_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.videos_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Info label
        self.videos_count_label = ttk.Label(self.tab_videos, 
                                           text="Aucune vidéo analysée")
        self.videos_count_label.pack(pady=5)
        
    def create_upload_tab(self):
        """Crée l'onglet d'upload YouTube"""
        
        # Frame pour la connexion
        login_frame = ttk.LabelFrame(self.tab_upload, text="Connexion YouTube", padding=10)
        login_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(login_frame, text="Email:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.email_entry = ttk.Entry(login_frame, width=40)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(login_frame, text="Mot de passe:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.password_entry = ttk.Entry(login_frame, width=40, show='*')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.login_button = ttk.Button(login_frame, text="Se connecter", 
                                      command=self.login_youtube)
        self.login_button.grid(row=2, column=1, sticky='e', padx=5, pady=5)
        
        # Frame pour les paramètres d'upload
        upload_frame = ttk.LabelFrame(self.tab_upload, text="Paramètres d'upload", padding=10)
        upload_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(upload_frame, text="Visibilité:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.visibility_var = tk.StringVar(value="private")
        visibility_combo = ttk.Combobox(upload_frame, textvariable=self.visibility_var,
                                       values=["private", "unlisted", "public"],
                                       width=15, state='readonly')
        visibility_combo.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(upload_frame, text="Catégorie:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.category_var = tk.StringVar(value="22")
        category_combo = ttk.Combobox(upload_frame, textvariable=self.category_var,
                                     values=["22", "20", "23", "24", "25", "26"],
                                     width=15, state='readonly')
        category_combo.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        ttk.Label(upload_frame, text="(22=People & Blogs, 20=Gaming, 23=Comedy...)").grid(
            row=1, column=2, sticky='w', padx=5, pady=5)
        
        # Bouton pour uploader
        self.upload_button = ttk.Button(upload_frame, text="Uploader les vidéos sur YouTube",
                                       command=self.start_upload,
                                       state='disabled',
                                       style='Accent.TButton')
        self.upload_button.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Console de log
        log_frame = ttk.LabelFrame(self.tab_upload, text="Console", padding=10)
        log_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap='word')
        self.log_text.pack(fill='both', expand=True)
        
    # Méthodes pour l'onglet Scan
    
    def add_folder(self):
        """Ajoute un dossier à scanner"""
        folder = filedialog.askdirectory(title="Sélectionner un dossier contenant des vidéos")
        if folder and folder not in self.folders:
            self.folders.append(folder)
            self.folders_listbox.insert(tk.END, folder)
            
    def remove_folder(self):
        """Retire un dossier de la liste"""
        selection = self.folders_listbox.curselection()
        if selection:
            index = selection[0]
            self.folders_listbox.delete(index)
            del self.folders[index]
            
    def scan_folders(self):
        """Scanne les dossiers pour trouver les vidéos"""
        if not self.folders:
            messagebox.showwarning("Aucun dossier", 
                                  "Veuillez ajouter au moins un dossier à scanner.")
            return
        
        self.status_label.config(text="Scan en cours...")
        self.root.update()
        
        videos = self.video_sorter.scan_folders(self.folders)
        
        self.status_label.config(text=f"{len(videos)} vidéo(s) trouvée(s)")
        messagebox.showinfo("Scan terminé", f"{len(videos)} vidéo(s) trouvée(s)")
        
    def analyze_videos(self):
        """Lance l'analyse des vidéos"""
        if not self.video_sorter.videos:
            messagebox.showwarning("Aucune vidéo", 
                                  "Veuillez d'abord scanner des dossiers.")
            return
        
        criteria = self.criteria_text.get('1.0', 'end-1c').strip()
        if not criteria:
            messagebox.showwarning("Critères manquants", 
                                  "Veuillez définir des critères de tri.")
            return
        
        # Tester la connexion à l'API
        if not self.vision_api.test_connection():
            messagebox.showerror("Erreur de connexion", 
                               "Impossible de se connecter à l'API de vision.\n"
                               "Vérifiez que http://trenas.fr:1234 est accessible.")
            return
        
        # Lancer l'analyse dans un thread séparé
        thread = threading.Thread(target=self._analyze_videos_thread, args=(criteria,))
        thread.daemon = True
        thread.start()
        
    def _analyze_videos_thread(self, criteria):
        """Thread pour analyser les vidéos"""
        videos = self.video_sorter.videos
        total = len(videos)
        self.analyzed_videos = []
        
        for i, video_path in enumerate(videos):
            self.status_label.config(text=f"Analyse: {i+1}/{total} - {os.path.basename(video_path)}")
            self.progress_var.set((i / total) * 100)
            self.root.update()
            
            result = self.vision_api.analyze_video(video_path, criteria, self.model_var.get())
            
            if result.get('success'):
                self.analyzed_videos.append(result)
        
        # Trier par score décroissant
        self.analyzed_videos = self.video_sorter.sort_videos_by_score(self.analyzed_videos)
        
        self.progress_var.set(100)
        self.status_label.config(text=f"Analyse terminée! {len(self.analyzed_videos)} vidéos analysées")
        
        # Rafraîchir la liste des vidéos
        self.root.after(100, self.refresh_videos_list)
        
        messagebox.showinfo("Analyse terminée", 
                          f"{len(self.analyzed_videos)} vidéos analysées avec succès!")
        
    # Méthodes pour l'onglet Vidéos
    
    def refresh_videos_list(self):
        """Rafraîchit la liste des vidéos"""
        # Effacer la liste
        for item in self.videos_tree.get_children():
            self.videos_tree.delete(item)
        
        # Remplir avec les vidéos analysées
        for i, video in enumerate(self.analyzed_videos):
            self.videos_tree.insert('', 'end', text=str(i+1), values=(
                os.path.basename(video.get('video_path', '')),
                video.get('video_path', ''),
                video.get('score', 0),
                video.get('analysis', '')[:100] + '...' if len(video.get('analysis', '')) > 100 else video.get('analysis', '')
            ))
        
        self.videos_count_label.config(text=f"{len(self.analyzed_videos)} vidéo(s)")
        
    def add_video_manually(self):
        """Ajoute une vidéo manuellement"""
        video_path = filedialog.askopenfilename(
            title="Sélectionner une vidéo",
            filetypes=[("Vidéos", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm")]
        )
        
        if video_path:
            # Ajouter avec un score par défaut
            self.analyzed_videos.append({
                'success': True,
                'video_path': video_path,
                'score': 50,
                'analysis': 'Ajoutée manuellement'
            })
            self.refresh_videos_list()
            
    def remove_selected_videos(self):
        """Retire les vidéos sélectionnées"""
        selection = self.videos_tree.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", 
                                  "Veuillez sélectionner des vidéos à retirer.")
            return
        
        # Récupérer les indices
        indices = [int(self.videos_tree.item(item)['text']) - 1 for item in selection]
        indices.sort(reverse=True)
        
        # Retirer les vidéos
        for index in indices:
            if 0 <= index < len(self.analyzed_videos):
                del self.analyzed_videos[index]
        
        self.refresh_videos_list()
        
    # Méthodes pour l'onglet Upload
    
    def login_youtube(self):
        """Se connecte à YouTube"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showwarning("Identifiants manquants", 
                                  "Veuillez saisir votre email et mot de passe.")
            return
        
        self.log("Initialisation du navigateur...")
        
        # Lancer dans un thread
        thread = threading.Thread(target=self._login_youtube_thread, args=(email, password))
        thread.daemon = True
        thread.start()
        
    def _login_youtube_thread(self, email, password):
        """Thread pour la connexion YouTube"""
        try:
            self.youtube_uploader = YouTubeUploader()
            self.youtube_uploader.setup_driver(headless=False)
            
            success = self.youtube_uploader.login_to_youtube(
                email, password, callback=self.log
            )
            
            if success:
                self.root.after(100, lambda: self.upload_button.config(state='normal'))
                self.root.after(100, lambda: self.login_button.config(state='disabled'))
            else:
                self.log("Échec de la connexion!")
                
        except Exception as e:
            self.log(f"Erreur: {str(e)}")
            
    def start_upload(self):
        """Lance l'upload des vidéos"""
        if not self.analyzed_videos:
            messagebox.showwarning("Aucune vidéo", 
                                  "Veuillez d'abord analyser des vidéos.")
            return
        
        if not self.youtube_uploader or not self.youtube_uploader.logged_in:
            messagebox.showwarning("Non connecté", 
                                  "Veuillez d'abord vous connecter à YouTube.")
            return
        
        # Demander confirmation
        response = messagebox.askyesno(
            "Confirmation",
            f"Êtes-vous sûr de vouloir uploader {len(self.analyzed_videos)} vidéo(s) sur YouTube?"
        )
        
        if not response:
            return
        
        # Préparer la liste des vidéos
        videos = [
            {
                'path': v.get('video_path'),
                'title': os.path.splitext(os.path.basename(v.get('video_path')))[0],
                'description': v.get('analysis', '')[:500]  # Limiter la description
            }
            for v in self.analyzed_videos
        ]
        
        # Lancer dans un thread
        thread = threading.Thread(
            target=self._upload_videos_thread,
            args=(videos, self.visibility_var.get(), self.category_var.get())
        )
        thread.daemon = True
        thread.start()
        
    def _upload_videos_thread(self, videos, visibility, category):
        """Thread pour uploader les vidéos"""
        try:
            results = self.youtube_uploader.upload_multiple_videos(
                videos, visibility, category, callback=self.log
            )
            
            success_count = sum(1 for r in results if r.get('success'))
            self.log(f"\n=== Résumé ===")
            self.log(f"✓ {success_count} vidéo(s) uploadée(s) avec succès")
            self.log(f"✗ {len(results) - success_count} échec(s)")
            
            messagebox.showinfo(
                "Upload terminé",
                f"{success_count}/{len(results)} vidéo(s) uploadée(s) avec succès!"
            )
            
        except Exception as e:
            self.log(f"Erreur globale: {str(e)}")
            
    def log(self, message):
        """Ajoute un message à la console de log"""
        def _log():
            self.log_text.insert('end', message + '\n')
            self.log_text.see('end')
            self.root.update()
        
        if threading.current_thread() != threading.main_thread():
            self.root.after(0, _log)
        else:
            _log()


def main():
    root = tk.Tk()
    app = VideoSorterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
