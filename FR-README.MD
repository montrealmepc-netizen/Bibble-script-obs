# OBS Bible Presenter 3.0

Un script Python complet pour afficher des versets bibliques dans OBS Studio, doté d'une interface moderne, d'une mise en forme automatique du texte et d'une intégration directe avec les sources de texte OBS. Inspiré par et développé pour MEPC Montréal.

[Image de l'interface OBS Bible Presenter]

## Fonctionnalités ✨

* **Interface Moderne :** Navigation intuitive utilisant CustomTkinter.
* **Gestion des Versions :** Chargez plusieurs versions de la Bible à partir de fichiers XML (format OSIS recommandé).
* **Navigation :** Parcourez facilement les Livres, Chapitres et Versets.
* **Recherche :**
    * Recherche par référence (ex: "Jean 3:16", "1 Cor 13:4").
    * Recherche par mot-clé dans la version active de la Bible.
    * Reconnaissance des noms de livres en plusieurs langues (Français, Anglais, Kirundi inclus).
    * Historique des recherches.
* **Favoris :** Enregistrez et accédez rapidement à vos versets préférés.
* **Intégration OBS :**
    * Met à jour directement les Sources de Texte (GDI+ ou Freetype 2) désignées dans OBS.
    * Contrôle la visibilité simultanée du texte principal ET de la référence.
* **Mise en Forme Automatique du Texte :**
    * Retour à la ligne automatique basé sur un nombre maximum de **mots par ligne**.
    * Division automatique des longs versets en blocs gérables basé sur un nombre maximum de **lignes par bloc**.
    * Limites configurables via l'onglet Paramètres.
* **Éditeur Live :** Modifiez directement le verset actuel ; les changements sont reflétés instantanément dans OBS.
* **Aperçu du Verset Suivant :** Visualisez et modifiez le verset à venir.
* **Paramètres Personnalisables :**
    * Sélection du thème : Clair/Sombre/Système.
    * Modèle d'affichage de la référence personnalisable.
    * Limites de mise en forme du texte ajustables.
* **Raccourcis Claviers :** Contrôlez la navigation bloc/verset directement depuis les raccourcis OBS.

---

## Prérequis 📝

1.  **OBS Studio :** Assurez-vous d'avoir installé OBS Studio (testé avec les versions récentes).
2.  **Python :** OBS Studio inclut généralement un environnement Python compatible. Cependant, si vous rencontrez des problèmes, l'installation d'une version autonome de Python (ex: 3.9, 3.10) peut être nécessaire pour installer des bibliothèques. Assurez-vous qu'OBS est configuré pour utiliser la bonne installation Python si vous en avez plusieurs.
3.  **Bibliothèque Python :** Vous avez besoin de `customtkinter`.

---

## Guide d'Installation 🛠️

1.  **Télécharger le Script :** Téléchargez le fichier `obs_bible_presenter_3.0.py` depuis ce dépôt.
2.  **Installer la Bibliothèque :** Ouvrez l'Invite de Commandes (cmd) ou le Terminal de votre système et exécutez :
    ```bash
    pip install customtkinter
    ```
    * *Note :* Si vous avez plusieurs versions de Python, assurez-vous d'utiliser le `pip` associé à l'environnement Python utilisé par OBS (ex: `python -m pip install customtkinter` ou `pip3 install customtkinter`).
3.  **Ajouter le Script à OBS :**
    * Ouvrez OBS Studio.
    * Allez dans `Outils` > `Scripts`.
    * Cliquez sur le bouton `+` en bas à gauche.
    * Naviguez jusqu'au fichier `obs_bible_presenter_3.0.py` téléchargé et sélectionnez-le.
4.  **Configurer les Paramètres du Script dans OBS :**
    * **Dossier des Bibles (.xml) :** Cliquez sur `Parcourir` et sélectionnez le dossier contenant vos fichiers XML de Bibles (format OSIS préféré).
    * **Source Texte Principal :** Sélectionnez la Source de Texte OBS (GDI+ ou Freetype 2) où le texte principal du verset doit apparaître.
    * **Source Texte Référence :** Sélectionnez la Source de Texte OBS où la référence (ex: "Jean 3:16") doit apparaître.
    * Fermez la fenêtre des Scripts.

---

## Guide d'Utilisation 📖

1.  **Ouvrir le Navigateur :** Retournez dans `Outils` > `Scripts`. Sélectionnez le script "OBS Bible Presenter 3.0" et cliquez sur le bouton `Ouvrir le Navigateur 3.0`.
2.  **Sélectionner la Bible :** Choisissez la version de la Bible souhaitée dans la liste déroulante en haut à gauche.
3.  **Naviguer :**
    * Cliquez sur un nom de Livre dans la barre latérale gauche.
    * Sélectionnez le Chapitre et le Verset dans les listes déroulantes au-dessus de la liste des livres.
    * Le verset sélectionné apparaîtra dans l'onglet "Éditeur" et mettra à jour les sources de texte OBS.
4.  **Afficher les Blocs :** Si un verset est divisé en plusieurs blocs (à cause des paramètres de formatage), utilisez les boutons `<< Préc.` et `Suiv. >>` ou les raccourcis configurés pour naviguer entre eux.
5.  **Onglet Recherche:**
    * Entrez une référence (ex: `Gen 1:1`) ou des mots-clés (ex: `amour jamais échoue`).
    * Appuyez sur Entrée ou cliquez sur `Rechercher`.
    * Double-cliquez sur un résultat pour l'afficher.
6.  **Onglet Favoris (⭐ Favoris):**
    * Pendant l'affichage d'un verset dans l'onglet Éditeur, cliquez sur le bouton `⭐ Favoris` pour l'enregistrer.
    * Allez dans l'onglet "⭐ Favoris" pour voir les favoris enregistrés.
    * Double-cliquez sur un favori pour le charger.
    * Sélectionnez un favori et cliquez sur `Retirer le favori sélectionné` pour le supprimer.
7.  **Onglet Éditeur :**
    * **Éditeur Principal :** Affiche le verset/bloc actuel, formaté automatiquement. Vous pouvez modifier manuellement le texte ici pour des ajustements temporaires ; ces modifications apparaîtront immédiatement dans OBS. **Note :** Quitter et revenir au verset réappliquera le formatage automatique, sauf si la modification a été faite dans l'aperçu pour le verset *suivant*.
    * **Aperçu Verset Suivant :** Affiche le verset *suivant* dans le chapitre, également formaté automatiquement. Vous pouvez modifier ce texte *avant* d'y naviguer. Ces modifications **persisteront** lorsque vous naviguerez vers ce verset.
    * **Vider :** Efface les sources de texte dans OBS.
8.  **Bascule "Show Text / Ref" :** Utilisez l'interrupteur en haut à droite de la fenêtre du Navigateur pour afficher ou masquer simultanément les sources de texte principal et de référence dans OBS.

---

## Configuration (Onglet Paramètres) ⚙️

* **Thème de l'application :** Choisissez Clair, Sombre, ou le défaut Système.
* **Modèle de référence :** Personnalisez l'affichage de la référence en utilisant `{livre}`, `{chapitre}` et `{verset}`.
* **Mots Max par Ligne :** Définissez le nombre maximum de mots avant un retour à la ligne automatique (0 pour désactiver).
* **Lignes Max par Bloc :** Définissez le nombre maximum de lignes avant une division automatique en un nouveau bloc d'affichage (0 pour désactiver).
* Cliquez sur `Enregistrer les paramètres` pour appliquer les changements. Modifier les paramètres de formatage reformatera automatiquement le verset actuellement affiché.

---

## Raccourcis Claviers ⌨️

Configurez-les dans OBS via `Fichier` > `Paramètres` > `Raccourcis clavier`. Cherchez "Bible":

* **Bible: Bloc Suivant :** Affiche le bloc suivant du verset actuel.
* **Bible: Bloc Précédent :** Affiche le bloc précédent du verset actuel.
* **Bible: Verset Suivant :** Charge le verset suivant dans le chapitre.
* **Bible: Verset Précédent :** Charge le verset précédent dans le chapitre.

---

## Dépannage 🤔

* **Bibliothèque Non Trouvée :** Assurez-vous que `customtkinter` est correctement installé dans l'environnement Python utilisé par OBS. Exécutez `pip show customtkinter` dans votre terminal pour vérifier.
* **Erreur de Script au Chargement :** Vérifiez les fichiers journaux d'OBS (`Aide` > `Fichiers journaux` > `Afficher les fichiers journaux`) pour des erreurs Python. Souvent lié à des bibliothèques manquantes ou des erreurs de syntaxe dans les modifications.
* **Aucune Source de Texte Listée :** Assurez-vous d'avoir créé des sources Texte (GDI+ / Freetype 2) dans votre scène OBS *avant* de configurer le script.
* **Texte Non Mis à Jour :** Vérifiez que les bonnes sources de texte sont sélectionnées dans les paramètres du script. Vérifiez si les sources sont visibles dans votre scène OBS.
* **Formatage Ne Fonctionne Pas :** Assurez-vous que les paramètres "Mots Max" et "Lignes Max" sont supérieurs à 0. Enregistrez les paramètres après modification.
