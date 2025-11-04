# Exemples d'utilisation

## Scénarios d'utilisation

### Scénario 1: Trier des clips de jeux vidéo

**Critères de tri:**
```
Évalue les clips de jeux vidéo selon:
- La présence d'action intense ou de moments spectaculaires
- La qualité visuelle et la netteté de l'image
- Les effets visuels impressionnants (explosions, compétences spéciales)
- L'intérêt pour un montage gaming
Donne un score élevé aux moments les plus excitants.
```

**Résultat attendu:**
Les vidéos contenant des moments de jeu spectaculaires (kills, victoires, actions rapides) auront des scores plus élevés.

---

### Scénario 2: Trier des vlogs ou contenus lifestyle

**Critères de tri:**
```
Analyse les vidéos pour identifier:
- La présence de personnes dans le cadre
- L'esthétique générale et l'atmosphère (lumière, couleurs chaudes)
- Des environnements intéressants (paysages, intérieurs design)
- La qualité de composition de l'image
Privilégie les contenus visuellement attractifs et bien composés.
```

**Résultat attendu:**
Les vidéos avec de belles compositions, de bonnes conditions d'éclairage et des sujets intéressants seront mieux notées.

---

### Scénario 3: Trier des contenus éducatifs/tutoriels

**Critères de tri:**
```
Évalue selon:
- La présence de texte, diagrammes ou éléments pédagogiques
- La clarté visuelle et la lisibilité
- Une mise en page structurée
- L'absence de distractions visuelles
Score plus élevé pour les contenus qui semblent informatifs et bien organisés.
```

**Résultat attendu:**
Les vidéos montrant des présentations claires, des écrans de tutoriel ou des diagrammes auront des scores élevés.

---

### Scénario 4: Trier des clips nature/paysages

**Critères de tri:**
```
Recherche:
- Des paysages naturels spectaculaires
- De belles conditions météorologiques et lumineuses
- Des couleurs vives et saturées (ciels bleus, couchers de soleil, verdure)
- Une composition esthétique
- L'absence de présence humaine ou d'éléments artificiels
```

**Résultat attendu:**
Les vidéos de nature pure, avec de beaux paysages et de bonnes conditions lumineuses seront favorisées.

---

## Workflow complet exemple

### Préparation
1. Créer un dossier avec vos clips vidéo
   ```
   C:\Users\VotreNom\Videos\Clips\
   ```

2. Lancer l'application
   - Double-cliquer sur `run.bat` (Windows)
   - Ou: `python main.py`

### Étape 1: Configuration
1. Onglet "1. Scan & Tri"
2. Ajouter dossier: `C:\Users\VotreNom\Videos\Clips\`
3. Cliquer "Scanner" → Ex: 50 vidéos trouvées

### Étape 2: Définir les critères
```
Je veux trier mes clips de gaming pour créer un montage des meilleurs moments.
Évalue:
- L'intensité de l'action (combats, courses, moments dynamiques)
- La présence d'éléments visuels spectaculaires
- La qualité générale de l'image
Attribue les scores les plus élevés aux moments les plus excitants.
```

### Étape 3: Analyse
1. Sélectionner le modèle: `qwen2.5-vl`
2. Cliquer "Analyser les vidéos"
3. Attendre (environ 30 secondes par vidéo)
4. ✓ Analyse terminée

### Étape 4: Révision
1. Onglet "2. Vidéos"
2. Voir la liste triée par score (100 → 0)
3. Retirer les vidéos avec score < 60
4. Garder les 20 meilleures

### Étape 5: Upload YouTube
1. Onglet "3. Upload YouTube"
2. Email: `votre.email@gmail.com`
3. Mot de passe: `••••••••`
4. Cliquer "Se connecter"
5. Configurer:
   - Visibilité: `unlisted` (non répertorié)
   - Catégorie: `20` (Gaming)
6. Cliquer "Uploader les vidéos sur YouTube"
7. Confirmer
8. ✓ 20 vidéos uploadées avec succès!

---

## Configuration des paramètres YouTube

### Catégories YouTube
- `1` - Film & Animation
- `2` - Autos & Vehicles
- `10` - Music
- `15` - Pets & Animals
- `17` - Sports
- `18` - Short Movies
- `19` - Travel & Events
- `20` - Gaming
- `21` - Videoblogging
- `22` - People & Blogs (par défaut)
- `23` - Comedy
- `24` - Entertainment
- `25` - News & Politics
- `26` - Howto & Style
- `27` - Education
- `28` - Science & Technology
- `29` - Nonprofits & Activism

### Niveaux de visibilité
- **Private**: Seul vous pouvez voir la vidéo
- **Unlisted**: Visible uniquement avec le lien
- **Public**: Visible pour tout le monde

---

## Conseils et astuces

### Pour de meilleurs résultats d'analyse
1. **Soyez spécifique dans vos critères**: Plus vos critères sont détaillés, meilleurs seront les résultats
2. **Testez avec quelques vidéos d'abord**: Analysez 5-10 vidéos pour voir si les critères fonctionnent bien
3. **Ajustez si nécessaire**: Si les scores ne correspondent pas à vos attentes, reformulez les critères

### Pour l'upload YouTube
1. **Utilisez "unlisted" pour les tests**: Évitez de publier en public avant d'être sûr
2. **Préparez vos titres**: Le nom du fichier devient le titre, renommez vos fichiers avant l'analyse
3. **Vérifiez la connexion**: Assurez-vous d'avoir une bonne connexion internet stable
4. **Upload par lots**: Si vous avez beaucoup de vidéos, uploadez-les par groupes de 10-20

### Performances
- L'analyse prend environ 20-40 secondes par vidéo
- L'upload dépend de la taille des fichiers et de votre connexion
- Pour 100 vidéos: prévoyez 1-2 heures pour l'analyse
- Fermez les autres applications pour de meilleures performances

---

## Dépannage courant

### "API non accessible"
→ Vérifiez dans votre navigateur: http://trenas.fr:1234/v1/models
→ Si ça ne fonctionne pas, le serveur est peut-être hors ligne

### "Échec de connexion YouTube"
→ Vérifiez vos identifiants
→ Si vous avez 2FA: créez un mot de passe d'application
→ Complétez la vérification 2FA dans le navigateur qui s'ouvre

### "Module not found"
→ Réinstallez: `pip install -r requirements.txt`
→ Vérifiez que l'environnement virtuel est activé

### Scores tous identiques ou bizarres
→ Reformulez vos critères plus clairement
→ Vérifiez que l'API répond correctement
→ Essayez un autre modèle (llava, qwen2-vl)
