# CODE: BIBLE MEPC MONTREAL V1.0
# AUTEUR: Inspiré et développé pour MEPC Montreal
# DESCRIPTION: Un script complet pour afficher et gérer les versets de la Bible dans OBS.

import obspython as obs
import tkinter as tk
from tkinter import ttk, font, messagebox, scrolledtext
import xml.etree.ElementTree as ET
import os

# --- TABLE DE CORRESPONDANCE POUR LES NOMS DE LIVRES ---
OSIS_TO_FRENCH_BOOK_NAMES = {
    "Gen": "Genèse", "Exod": "Exode", "Lev": "Lévitique", "Num": "Nombres", "Deut": "Deutéronome",
    "Josh": "Josué", "Judg": "Juges", "Ruth": "Ruth", "1Sam": "1 Samuel", "2Sam": "2 Samuel",
    "1Kgs": "1 Rois", "2Kgs": "2 Rois", "1Chr": "1 Chroniques", "2Chr": "2 Chroniques", "Ezra": "Esdras",
    "Neh": "Néhémie", "Esth": "Esther", "Job": "Job", "Ps": "Psaumes", "Prov": "Proverbes",
    "Eccl": "Ecclésiaste", "Song": "Cantique des Cantiques", "Isa": "Ésaïe", "Jer": "Jérémie",
    "Lam": "Lamentations", "Ezek": "Ézéchiel", "Dan": "Daniel", "Hos": "Osée", "Joel": "Joël",
    "Amos": "Amos", "Obad": "Abdias", "Jonah": "Jonas", "Mic": "Michée", "Nah": "Nahum",
    "Hab": "Habacuc", "Zeph": "Sophonie", "Hag": "Aggée", "Zech": "Zacharie", "Mal": "Malachie",
    "Matt": "Matthieu", "Mark": "Marc", "Luke": "Luc", "John": "Jean", "Acts": "Actes",
    "Rom": "Romains", "1Cor": "1 Corinthiens", "2Cor": "2 Corinthiens", "Gal": "Galates",
    "Eph": "Éphésiens", "Phil": "Philippiens", "Col": "Colossiens", "1Thess": "1 Thessaloniciens",
    "2Thess": "2 Thessaloniciens", "1Tim": "1 Timothée", "2Tim": "2 Timothée", "Titus": "Tite",
    "Phlm": "Philémon", "Heb": "Hébreux", "Jas": "Jacques", "1Pet": "1 Pierre", "2Pet": "2 Pierre",
    "1John": "1 Jean", "2John": "2 Jean", "3John": "3 Jean", "Jude": "Jude", "Rev": "Apocalypse"
}

# --- Variable Globale (Gestionnaire) ---
bible_manager = None

# ----------------------------------------------------------------------
# --- CLASSE BibleManager ---
# ----------------------------------------------------------------------
class BibleManager:
    """Encapsule toutes les données et la logique de gestion de la Bible."""
    
    def __init__(self):
        self.bible_path = ""
        self.text_source_name = ""
        self.navigator_window = None
        self.bible_data = {}
        self.ordered_books = []
        self.lines_per_display = 5
        self.display_blocks = []
        self.current_block_index = -1
        self.current_book_id = "" 
        self.current_chapter = 0
        self.current_verse_index = -1
        self.next_verse_info_cache = {}
        self.modified_next_verse_text = None

    def load_bible_from_xml(self, filepath):
        self.bible_path = filepath
        self.bible_data.clear(); self.ordered_books.clear()
        self.reset_current_passage()
        if not filepath or not os.path.exists(filepath): return False
        try:
            ET.register_namespace("", "http://www.bibletechnologies.net/2003/OSIS/namespace")
            tree = ET.parse(filepath)
            root = tree.getroot()
            namespace = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
            for book_node in root.findall('.//osis:div[@type="book"]', namespace):
                book_id = book_node.get('osisID')
                if book_id:
                    book_name = OSIS_TO_FRENCH_BOOK_NAMES.get(book_id, book_id)
                    self.bible_data[book_id] = {'name': book_name, 'chapters': {}}
                    self.ordered_books.append(book_name)
                    for chapter_node in book_node.findall('osis:chapter', namespace):
                        chapter_osis_id = chapter_node.get('osisID')
                        try:
                            chapter_num = int(chapter_osis_id.split('.')[-1])
                            self.bible_data[book_id]['chapters'][chapter_num] = [""] 
                            for verse_node in chapter_node.findall('osis:verse', namespace):
                                self.bible_data[book_id]['chapters'][chapter_num].append(verse_node.text or "")
                        except (ValueError, IndexError): pass
            if self.navigator_window: self.navigator_window.update_book_list()
            return True
        except Exception as e:
            messagebox.showerror("Erreur de Chargement", f"Impossible de lire le fichier XML.\n\nErreur: {e}")
            return False

    def save_verse(self, book_id, chapter, verse_num, new_text):
        if not self.bible_path: return False, "Chemin du fichier non défini."
        try:
            ET.register_namespace("", "http://www.bibletechnologies.net/2003/OSIS/namespace")
            tree = ET.parse(self.bible_path)
            root = tree.getroot()
            namespace = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
            verse_osis_id = f"{book_id}.{chapter}.{verse_num}"
            verse_node = root.find(f".//osis:verse[@osisID='{verse_osis_id}']", namespace)
            if verse_node is not None:
                verse_node.text = new_text
                tree.write(self.bible_path, encoding='utf-8', xml_declaration=True)
                self.bible_data[book_id]['chapters'][chapter][verse_num] = new_text
                return True, "Sauvegarde réussie !"
            else: return False, f"Verset {verse_osis_id} non trouvé."
        except Exception as e: return False, f"Erreur de sauvegarde : {e}"

    def get_books(self): return self.ordered_books
    def get_book_id_by_name(self, name):
        for book_id, data in self.bible_data.items():
            if data['name'] == name: return book_id
        return None
    def get_chapters_for_book(self, book_name):
        book_id = self.get_book_id_by_name(book_name)
        if book_id in self.bible_data: return sorted(self.bible_data[book_id]['chapters'].keys())
        return []
    def get_verses_for_chapter(self, book_name, chapter_num):
        book_id = self.get_book_id_by_name(book_name)
        if book_id and chapter_num in self.bible_data[book_id]['chapters']:
            return self.bible_data[book_id]['chapters'][chapter_num]
        return []

    def set_passage(self, book, chapter, verse_num):
        self.current_book_id = self.get_book_id_by_name(book)
        self.current_chapter = int(chapter)
        self.current_verse_index = int(verse_num)
        verse_text_to_display = self.get_current_verse_text()
        if (self.modified_next_verse_text is not None and 
            self.next_verse_info_cache.get('book_id') == self.current_book_id and
            self.next_verse_info_cache.get('chapter') == self.current_chapter and
            self.next_verse_info_cache.get('verse_num') == self.current_verse_index):
            verse_text_to_display = self.modified_next_verse_text
            self.bible_data[self.current_book_id]['chapters'][self.current_chapter][self.current_verse_index] = verse_text_to_display
            self.modified_next_verse_text = None
        self.update_live_text(verse_text_to_display)
        self.current_block_index = 0 if self.display_blocks else -1
        update_obs_text()
        if self.navigator_window: self.navigator_window.update_display()

    def update_live_text(self, full_verse_text):
        self.display_blocks.clear()
        if full_verse_text:
            all_lines = full_verse_text.split('\n')
            for i in range(0, len(all_lines), self.lines_per_display):
                self.display_blocks.append("\n".join(all_lines[i : i + self.lines_per_display]))
        if self.current_block_index >= len(self.display_blocks):
            self.current_block_index = max(0, len(self.display_blocks) - 1)
        update_obs_text()
        if self.navigator_window: self.navigator_window.update_status_label()

    def navigate_block(self, direction):
        if not self.current_book_id or self.current_verse_index == -1: return
        new_block_index = self.current_block_index + direction
        if 0 <= new_block_index < len(self.display_blocks):
            self.current_block_index = new_block_index
            update_obs_text()
            if self.navigator_window: self.navigator_window.update_status_label()
        else: self.navigate_verse(direction)

    def navigate_verse(self, direction):
        if not self.current_book_id: return
        book_name = self.bible_data[self.current_book_id]['name']
        verses = self.get_verses_for_chapter(book_name, self.current_chapter)
        new_verse_index = self.current_verse_index + direction
        if 1 <= new_verse_index < len(verses):
            self.set_passage(book_name, self.current_chapter, new_verse_index)

    def reset_current_passage(self):
        self.current_book_id = ""; self.current_chapter = 0; self.current_verse_index = -1
        self.display_blocks.clear(); self.current_block_index = -1
        update_obs_text()
        if self.navigator_window: self.navigator_window.update_display()

    def get_current_block_text(self):
        if 0 <= self.current_block_index < len(self.display_blocks):
            return self.display_blocks[self.current_block_index]
        return ""
    def get_current_verse_text(self):
        if not self.current_book_id or self.current_verse_index <= 0: return ""
        try: return self.bible_data[self.current_book_id]['chapters'][self.current_chapter][self.current_verse_index]
        except (KeyError, IndexError): return ""

    def get_next_verse_info(self):
        self.modified_next_verse_text = None
        if not self.current_book_id or self.current_verse_index <= 0:
            self.next_verse_info_cache = {}
            return "...", ""
        book_name = self.bible_data[self.current_book_id]['name']
        verses_in_chapter = self.get_verses_for_chapter(book_name, self.current_chapter)
        if self.current_verse_index + 1 < len(verses_in_chapter):
            next_verse_num = self.current_verse_index + 1
            self.next_verse_info_cache = {
                'book_id': self.current_book_id, 'chapter': self.current_chapter,
                'verse_num': next_verse_num, 'ref': f"{book_name} {self.current_chapter}:{next_verse_num}"
            }
            return self.next_verse_info_cache['ref'], verses_in_chapter[next_verse_num]
        self.next_verse_info_cache = {}
        return "Fin du chapitre", ""

# --- Fonctions Globales et Standard OBS ---
def update_obs_text():
    global bible_manager; text_to_display = bible_manager.get_current_block_text() if bible_manager else ""
    source_name = bible_manager.text_source_name if bible_manager else ""
    if source_name:
        source = obs.obs_get_source_by_name(source_name)
        if source:
            settings = obs.obs_data_create(); obs.obs_data_set_string(settings, "text", text_to_display)
            obs.obs_source_update(source, settings)
            obs.obs_source_release(source); obs.obs_data_release(settings)
def on_hotkey_pressed(hotkey_id):
    if bible_manager:
        if hotkey_id == "bible_next": bible_manager.navigate_block(1)
        elif hotkey_id == "bible_prev": bible_manager.navigate_block(-1)
def setup_hotkeys():
    hotkeys = {"bible_next": "Bible: Suivant", "bible_prev": "Bible: Précédent"}
    for id, desc in hotkeys.items():
        obs.obs_hotkey_register_frontend(id, desc, lambda p, id=id: on_hotkey_pressed(id) if p else None)
def open_navigator_callback(props, prop):
    global bible_manager;
    if not bible_manager: return
    if not bible_manager.navigator_window or not bible_manager.navigator_window.winfo_exists():
        bible_manager.navigator_window = BibleNavigator(bible_manager)
        bible_manager.navigator_window.protocol("WM_DELETE_WINDOW", bible_manager.navigator_window.on_closing)
        bible_manager.navigator_window.mainloop()
    else: bible_manager.navigator_window.lift()

def script_description():
    return """
    <h2>Bible Mepc montreal V1.0</h2>
    <p>This script allows you to load a Bible from an OSIS-formatted XML file and display verses in a GDI+ text source.</p>
    <p><b>Download the Louis Segond 1910 XML Bible file here:</b> <a href='https://github.com/montrealmepc-netizen/biblefr'>https://github.com/montrealmepc-netizen/biblefr</a></p>
    <p><strong>Features:</strong></p>
    <ul>
        <li><strong>Live Editing:</strong> Text typed in the current verse editor updates the OBS text source in real-time.</li>
        <li><strong>Next Verse Preview & Edit:</strong> You can see and edit the upcoming verse. Edits are applied automatically when you navigate to it.</li>
        <li><strong>Block Display:</strong> Long verses are automatically split into pages (5 lines each) for better readability.</li>
        <li><strong>Easy Navigation:</strong> Use buttons or hotkeys to navigate through pages and verses.</li>
        <li><strong>Save on the Fly:</strong> Permanently save your edits to the XML file with the save buttons.</li>
    </ul>
    """
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_path(props, "bible_file", "Bible File (.xml)", obs.OBS_PATH_FILE, "XML Files (*.xml)", None)
    source_list = obs.obs_properties_add_list(props, "text_source", "Text Source (GDI+)", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id in ["text_gdiplus", "text_ft2_source"]:
                obs.obs_property_list_add_string(source_list, obs.obs_source_get_name(source), obs.obs_source_get_name(source))
        obs.source_list_release(sources)
    obs.obs_properties_add_button(props, "navigator_button", "Open Navigator", open_navigator_callback)
    return props
def script_load(settings):
    global bible_manager; bible_manager = BibleManager()
    bible_manager.text_source_name = obs.obs_data_get_string(settings, "text_source")
    bible_manager.load_bible_from_xml(obs.obs_data_get_string(settings, "bible_file"))
    setup_hotkeys()
def script_update(settings):
    global bible_manager;
    if not bible_manager: return
    bible_manager.text_source_name = obs.obs_data_get_string(settings, "text_source")
    if obs.obs_data_get_string(settings, "bible_file") != bible_manager.bible_path:
        bible_manager.load_bible_from_xml(obs.obs_data_get_string(settings, "bible_file"))
    update_obs_text()
def script_unload():
    if bible_manager and bible_manager.navigator_window: bible_manager.navigator_window.destroy()

# ----------------------------------------------------------------------
# --- CLASSE TKINTER ---
# ----------------------------------------------------------------------
class BibleNavigator(tk.Tk):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.title("Bible Mepc montreal V1.0")
        self.geometry("800x600")
        self.configure(padx=10, pady=10)
        self.font_main = font.Font(family="Segoe UI", size=10)
        self.create_widgets()
        self.update_book_list()

    def on_closing(self): self.manager.navigator_window = None; self.destroy()

    def create_widgets(self):
        main_frame = ttk.Frame(self); main_frame.pack(fill=tk.BOTH, expand=True)
        selection_frame = ttk.Frame(main_frame); selection_frame.pack(fill=tk.X, pady=(0, 10))
        selection_frame.columnconfigure(1, weight=1); selection_frame.columnconfigure(3, weight=1); selection_frame.columnconfigure(5, weight=1)
        ttk.Label(selection_frame, text="Livre:", font=self.font_main).grid(row=0, column=0, padx=(0, 5))
        self.book_var = tk.StringVar(); self.book_combo = ttk.Combobox(selection_frame, textvariable=self.book_var, state="readonly", font=self.font_main)
        self.book_combo.grid(row=0, column=1, sticky="ew"); self.book_combo.bind("<<ComboboxSelected>>", self.on_book_selected)
        ttk.Label(selection_frame, text="Chapitre:", font=self.font_main).grid(row=0, column=2, padx=(10, 5))
        self.chapter_var = tk.StringVar(); self.chapter_combo = ttk.Combobox(selection_frame, textvariable=self.chapter_var, state="readonly", width=5, font=self.font_main)
        self.chapter_combo.grid(row=0, column=3, sticky="ew"); self.chapter_combo.bind("<<ComboboxSelected>>", self.on_chapter_selected)
        ttk.Label(selection_frame, text="Verset:", font=self.font_main).grid(row=0, column=4, padx=(10, 5))
        self.verse_var = tk.StringVar(); self.verse_combo = ttk.Combobox(selection_frame, textvariable=self.verse_var, state="readonly", width=5, font=self.font_main)
        self.verse_combo.grid(row=0, column=5, sticky="ew"); self.verse_combo.bind("<<ComboboxSelected>>", self.on_verse_selected)

        editor_frame = ttk.LabelFrame(main_frame, text="Éditeur du verset actuel (mise à jour en direct)")
        editor_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.editor_text = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD, height=5, font=self.font_main)
        self.editor_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.editor_text.bind("<KeyRelease>", self.on_editor_key_release)
        
        control_frame = ttk.Frame(editor_frame); control_frame.pack(fill=tk.X, pady=(5,0))
        ttk.Button(control_frame, text="<< Précédent", command=lambda: self.manager.navigate_block(-1)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(control_frame, text="Suivant >>", command=lambda: self.manager.navigate_block(1)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(control_frame, text="Effacer l'affichage", command=self.manager.reset_current_passage).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        preview_frame = ttk.LabelFrame(main_frame, text="Éditeur du prochain verset (application automatique)")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.preview_ref_label = ttk.Label(preview_frame, text="...", font=self.font_main)
        self.preview_ref_label.pack(fill=tk.X, padx=5, pady=(5,0))
        self.preview_text = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, height=3, font=self.font_main)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.preview_text.bind("<KeyRelease>", self.on_preview_key_release)

        buttons_frame = ttk.Frame(main_frame); buttons_frame.pack(fill=tk.X, pady=(5, 10))
        buttons_frame.columnconfigure(0, weight=1); buttons_frame.columnconfigure(1, weight=1)
        ttk.Button(buttons_frame, text="💾 Enregistrer le verset actuel", command=self.save_current_verse).grid(row=0, column=0, sticky="ew", padx=(0,2))
        ttk.Button(buttons_frame, text="💾 Enregistrer le verset suivant", command=self.save_next_verse).grid(row=0, column=1, sticky="ew", padx=(2,0))

        self.status_label = ttk.Label(main_frame, text="Aucun passage sélectionné.", font=self.font_main, anchor="center")
        self.status_label.pack(fill=tk.X, pady=(5, 0))

    def on_editor_key_release(self, event=None):
        self.manager.update_live_text(self.editor_text.get("1.0", tk.END).strip())

    def on_preview_key_release(self, event=None):
        self.manager.modified_next_verse_text = self.preview_text.get("1.0", tk.END).strip()

    def save_current_verse(self):
        if not self.manager.current_book_id: return
        text_to_save = self.editor_text.get("1.0", tk.END).strip()
        self.manager.bible_data[self.manager.current_book_id]['chapters'][self.manager.current_chapter][self.manager.current_verse_index] = text_to_save
        success, message = self.manager.save_verse(self.manager.current_book_id, self.manager.current_chapter, self.manager.current_verse_index, text_to_save)
        if success: messagebox.showinfo("Sauvegarde", message)
        else: messagebox.showerror("Erreur", message)

    def save_next_verse(self):
        next_info = self.manager.next_verse_info_cache
        if not next_info:
            messagebox.showwarning("Sauvegarde impossible", "Aucun 'prochain verset' n'est chargé.")
            return
        text_to_save = self.preview_text.get("1.0", tk.END).strip()
        self.manager.modified_next_verse_text = text_to_save
        success, message = self.manager.save_verse(next_info['book_id'], next_info['chapter'], next_info['verse_num'], text_to_save)
        if success: messagebox.showinfo("Sauvegarde", message)
        else: messagebox.showerror("Erreur", message)
    
    def on_book_selected(self, event=None):
        chapters = self.manager.get_chapters_for_book(self.book_var.get())
        self.chapter_combo['values'] = chapters;
        if chapters: self.chapter_combo.set(chapters[0]); self.on_chapter_selected()
    def on_chapter_selected(self, event=None):
        verses = self.manager.get_verses_for_chapter(self.book_var.get(), int(self.chapter_var.get()))
        self.verse_combo['values'] = list(range(1, len(verses)))
        if verses: self.verse_combo.set(1); self.on_verse_selected()
    def on_verse_selected(self, event=None):
        try: self.manager.set_passage(self.book_var.get(), int(self.chapter_var.get()), int(self.verse_var.get()))
        except (ValueError, TypeError): pass

    def update_book_list(self):
        books = self.manager.get_books(); self.book_combo['values'] = books
        if books: self.book_combo.set(books[0]); self.on_book_selected()
    
    def update_display(self):
        self.editor_text.unbind("<KeyRelease>")
        self.editor_text.delete("1.0", tk.END)
        self.editor_text.insert("1.0", self.manager.get_current_verse_text())
        self.editor_text.bind("<KeyRelease>", self.on_editor_key_release)
        if self.manager.current_book_id:
            self.book_var.set(self.manager.bible_data[self.manager.current_book_id]['name'])
            self.chapter_var.set(self.manager.current_chapter)
            self.verse_var.set(self.manager.current_verse_index)
        self.update_status_label()
        ref, text = self.manager.get_next_verse_info()
        self.preview_ref_label.config(text=ref)
        self.preview_text.unbind("<KeyRelease>")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", text)
        self.preview_text.bind("<KeyRelease>", self.on_preview_key_release)

    def update_status_label(self):
        if self.manager.current_book_id and self.manager.current_verse_index > 0:
            book_name = self.manager.bible_data[self.manager.current_book_id]['name']
            total_blocks = len(self.manager.display_blocks)
            status_text = f"Affiché : {book_name} {self.manager.current_chapter}:{self.manager.current_verse_index} (Page {self.manager.current_block_index + 1}/{total_blocks})"
            self.status_label.config(text=status_text)
        else: self.status_label.config(text="Aucun passage sélectionné.")