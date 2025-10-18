# OBS Bible Presenter 3.0

A comprehensive Python script for displaying Bible verses within OBS Studio, featuring a modern interface, automatic text formatting, and direct integration with OBS text sources. Inspired by and developed for MEPC Montreal.

[Image of OBS Bible Presenter Interface]

## Features ✨

* **Modern UI:** Intuitive navigation using CustomTkinter.
* **Bible Version Management:** Load multiple Bible versions from XML files (OSIS format recommended).
* **Navigation:** Easily browse Books, Chapters, and Verses.
* **Search:**
    * Reference search (e.g., "John 3:16", "1 Cor 13:4").
    * Keyword search within the active Bible version.
    * Multi-language book name recognition (French, English, Kirundi included).
    * Search history.
* **Favorites:** Save and quickly access your favorite verses.
* **OBS Integration:**
    * Directly updates designated GDI+ or Freetype 2 Text Sources in OBS.
    * Controls visibility for both the main text and reference sources simultaneously.
* **Automatic Text Formatting:**
    * Automatically wraps text based on a maximum number of **words per line**.
    * Automatically splits long verses into manageable blocks based on a maximum number of **lines per block**.
    * Configurable limits via the Settings tab.
* **Live Editor:** Edit the current verse directly; changes are reflected instantly in OBS.
* **Next Verse Preview:** See and edit the upcoming verse.
* **Customizable Settings:**
    * Light/Dark/System theme selection.
    * Customizable reference display template.
    * Adjustable text formatting limits.
* **Hotkeys:** Control block/verse navigation directly from OBS hotkeys.

---

## Prerequisites 📝

1.  **OBS Studio:** Ensure you have OBS Studio installed (tested with recent versions).
2.  **Python:** OBS Studio typically includes a compatible Python environment. However, if you encounter issues, installing a standalone Python version (e.g., 3.9, 3.10) might be necessary for installing libraries. Make sure OBS is configured to use the correct Python installation if you have multiple.
3.  **Python Library:** You need `customtkinter`.

---

## Installation Guide 🛠️

1.  **Download Script:** Download the `obs_bible_presenter_3.0.py` file from this repository.
2.  **Install Library:** Open your system's Command Prompt (cmd) or Terminal and run:
    ```bash
    pip install customtkinter
    ```
    * *Note:* If you have multiple Python versions, ensure you use the `pip` associated with the Python environment OBS uses (e.g., `python -m pip install customtkinter` or `pip3 install customtkinter`).
3.  **Add Script to OBS:**
    * Open OBS Studio.
    * Go to `Tools` > `Scripts`.
    * Click the `+` button in the bottom left.
    * Navigate to and select the downloaded `obs_bible_presenter_3.0.py` file.
4.  **Configure Script Settings in OBS:**
    * **Bible Folder (.xml):** Click `Browse` and select the folder containing your Bible XML files (OSIS format preferred).
    * **Main Text Source:** Select the OBS Text Source (GDI+ or Freetype 2) where the main verse text should appear.
    * **Reference Text Source:** Select the OBS Text Source where the reference (e.g., "John 3:16") should appear.
    * Close the Scripts window.

---

## Usage Guide 📖

1.  **Open Navigator:** Go back to `Tools` > `Scripts`. Select the "OBS Bible Presenter 3.0" script and click the `Open Navigator 3.0` button.
2.  **Select Bible:** Choose your desired Bible version from the top-left dropdown.
3.  **Navigate:**
    * Click a Book name in the left sidebar.
    * Select the Chapter and Verse from the dropdowns above the book list.
    * The selected verse will appear in the "Éditeur" (Editor) tab and update the OBS text sources.
4.  **Display Blocks:** If a verse is split into multiple blocks (due to formatting settings), use the `<< Préc.` (Prev) and `Suiv. >>` (Next) buttons or configured hotkeys to cycle through them.
5.  **Search Tab:**
    * Enter a reference (e.g., `Gen 1:1`) or keywords (e.g., `love never fails`).
    * Press Enter or click `Rechercher` (Search).
    * Double-click a result to display it.
6.  **Favorites Tab (⭐ Favoris):**
    * While viewing a verse in the Editor tab, click the `⭐ Favoris` button to save it.
    * Go to the "⭐ Favoris" tab to view saved favorites.
    * Double-click a favorite to load it.
    * Select a favorite and click `Retirer le favori sélectionné` (Remove selected favorite) to delete it.
7.  **Editor Tab (Éditeur):**
    * **Main Editor:** Shows the currently displayed verse/block, formatted automatically. You can manually edit the text here for temporary overrides; these edits will appear in OBS immediately. **Note:** Navigating away and back will reapply automatic formatting unless the edit was made in the preview pane for the *next* verse.
    * **Next Verse Preview:** Shows the *next* verse in the chapter, also automatically formatted. You can edit this text *before* navigating to it. These edits **will persist** when you navigate to that verse.
    * **Vider (Clear):** Clears the text sources in OBS.
8.  **Show Text / Ref Toggle:** Use the switch in the top-right corner of the Navigator window to simultaneously show or hide both the main text and reference sources in OBS.

---

## Configuration (Settings Tab) ⚙️

* **Thème de l'application (Theme):** Choose Light, Dark, or System default.
* **Modèle de référence (Reference Template):** Customize how the reference is displayed using `{livre}` (book), `{chapitre}` (chapter), and `{verset}` (verse).
* **Mots Max par Ligne (Max Words per Line):** Set the maximum words before automatically wrapping to a new line (0 to disable).
* **Lignes Max par Bloc (Max Lines per Block):** Set the maximum lines before automatically splitting into a new display block (0 to disable).
* Click `Enregistrer les paramètres` (Save Settings) to apply changes. Changing formatting settings will automatically reformat the currently displayed verse.

---

## Hotkeys ⌨️

Configure these in OBS under `File` > `Settings` > `Hotkeys`. Search for "Bible":

* **Bible: Next Block:** Displays the next block of the current verse.
* **Bible: Previous Block:** Displays the previous block of the current verse.
* **Bible: Next Verse:** Loads the next verse in the chapter.
* **Bible: Previous Verse:** Loads the previous verse in the chapter.

---

## Troubleshooting Tips 🤔

* **Library Not Found:** Ensure `customtkinter` is installed correctly in the Python environment OBS is using. Run `pip show customtkinter` in your terminal to check.
* **Script Error on Load:** Check the OBS log files (`Help` > `Log Files` > `Show Log Files`) for Python errors. Often related to missing libraries or syntax errors in modifications.
* **No Text Sources Listed:** Make sure you have created Text (GDI+ / Freetype 2) sources in your OBS scene *before* configuring the script.
* **Text Not Updating:** Verify the correct text sources are selected in the script settings. Check if the sources are visible in your OBS scene.
* **Formatting Not Working:** Ensure the "Max Words" and "Max Lines" settings are greater than 0. Save settings after changes.
