# Présentateur Biblique pour OBS 2.0

Un script Python puissant pour OBS Studio, conçu pour afficher des versets bibliques et leurs références de manière fluide pendant des diffusions en direct ou des enregistrements. Cet outil envoie le texte du verset et la référence à deux sources de texte OBS distinctes, permettant une mise en page et un style indépendants. Il est doté d'une interface utilisateur moderne, de capacités de recherche robustes, de favoris, d'un historique et d'une prise en charge des raccourcis clavier pour une utilisation efficace.

Inspiré par et développé pour MEPC Montréal.

## ✨ Fonctionnalités

* **Sortie sur Deux Sources**: Envoie le texte du verset et sa référence (ex: "Jean 3:16") à deux sources de texte différentes dans OBS pour une flexibilité maximale de mise en page.
* **Interface Utilisateur Moderne**: Une fenêtre de navigation intuitive construite avec Tkinter et ttkthemes pour une gestion facile.
* **Recherche Avancée**: Trouvez rapidement des passages par référence (ex: "1 Cor 13:4") ou par recherche de mots-clés dans le texte.
* **Favoris et Historique**: Enregistrez les versets fréquemment utilisés dans vos favoris et accédez instantanément à vos recherches récentes.
* **Support des Raccourcis Clavier**: Naviguez entre les versets et les blocs de texte directement depuis OBS à l'aide de raccourcis configurables.
* **Éditeur de Versets en Direct**: Corrigez les fautes de frappe ou reformatez les versets à la volée. Les modifications sont automatiquement sauvegardées dans le fichier XML source.
* **Support Multi-Bibles**: Chargez plusieurs versions de la Bible (au format OSIS XML) et passez facilement de l'une à l'autre.

## ⚙️ Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

1.  **[OBS Studio](https://obsproject.com/)**: La dernière version est recommandée.
2.  **[Python](https://www.python.org/downloads/)**: Le script nécessite une version spécifique de Python qui correspond à votre installation d'OBS.
    * Pour trouver la version requise, ouvrez OBS et allez dans **Outils -> Scripts -> Paramètres Python**. La version exacte dont vous avez besoin y sera spécifiée.
    * **Crucial pour les utilisateurs de Windows** : Pendant l'installation de Python, assurez-vous de cocher la case **"Add Python to PATH"**.
3.  **Bibliothèque `ttkthemes`**: Un paquet Python pour le style de l'interface utilisateur.
4.  **Fichiers de la Bible**: Le script nécessite les textes bibliques au format **OSIS XML**.

## 🚀 Installation et Configuration

Suivez ces étapes pour faire fonctionner le script dans OBS.

### Étape 1 : Installer les Dépendances Python

Ouvrez un terminal (Invite de commandes sous Windows, Terminal sous macOS/Linux) et exécutez la commande suivante pour installer la bibliothèque requise :

```bash
pip install ttkthemes
```

### Étape 2 : Préparer les Fichiers de la Bible

1.  Téléchargez des versions de la Bible compatibles depuis le [dépôt de Bibles Compatibles](https://github.com/montrealmepc-netizen/Compatible-bibles).
2.  Créez un dossier sur votre ordinateur (par exemple, `C:\Bibles` ou `Documents/Bibles`).
3.  Extrayez et placez tous les fichiers `.xml` de la Bible directement dans ce dossier.

### Étape 3 : Configurer OBS Studio

1.  **Enregistrer le Script** : Enregistrez le code du script dans un fichier Python (par exemple, `bible_presenter.py`).
2.  **Créer les Sources de Texte** : Dans la scène OBS de votre choix, ajoutez deux sources de type **Texte (GDI+)** :
    * Une pour le texte du verset (nommez-la par exemple `Texte Verset`).
    * Une pour la référence (nommez-la par exemple `Référence Verset`).
3.  **Charger le Script** :
    * Dans OBS, allez dans **Outils -> Scripts**.
    * Cliquez sur le bouton `+` et ajoutez le fichier `bible_presenter.py`.
4.  **Définir les Propriétés du Script** :
    * Avec le script sélectionné, configurez les options à droite :
    * **Bible Folder** : Cliquez sur `Parcourir` et sélectionnez le dossier où vous avez enregistré vos fichiers `.xml`.
    * **Main Text Source (Verse)** : Sélectionnez votre source `Texte Verset` dans le menu déroulant.
    * **Reference Text Source (Optional)** : Sélectionnez votre source `Référence Verset`.
5.  **Lancer le Navigateur** : Cliquez sur le bouton **"Open Navigator"** dans les propriétés du script pour lancer la fenêtre de contrôle.

## 📖 Utilisation

La **Fenêtre de Navigation** est votre centre de contrôle principal.

* **Onglet Navigation** : Sélectionnez la version de la Bible, le livre, le chapitre et le verset à l'aide des menus déroulants.
* **Onglet Recherche** : Tapez une référence ou un mot-clé pour trouver des versets. Double-cliquez sur un résultat pour l'afficher.
* **Onglet Favoris** : Accédez à vos versets enregistrés. Double-cliquez pour en afficher un.
* **Éditeur de Versets en Direct** : Le verset actuellement affiché apparaît ici. Vous pouvez le modifier, et les changements seront visibles dans OBS et enregistrés dans le fichier XML après un court délai.
* **Boutons de Navigation** : Utilisez les boutons `<< Précédent`, `Suivant >>` et `Effacer` pour contrôler l'affichage.

### Raccourcis Clavier

Vous pouvez configurer les raccourcis suivants dans **OBS -> Paramètres -> Raccourcis clavier** :

* `Bible: Next Block` : Affiche le paragraphe/bloc suivant du verset actuel.
* `Bible: Previous Block` : Affiche le paragraphe/bloc précédent.
* `Bible: Next Verse` : Passe au verset suivant.
* `Bible: Previous Verse` : Passe au verset précédent.
