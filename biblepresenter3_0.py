# CODE: OBS BIBLE PRESENTER 3.0 (Stable - Build 3.2.9 Internally - Next Verse Edit Fix)
# AUTHOR: Inspired and developed for MEPC Montreal
# DESCRIPTION: Corrects the issue where edits in the "Next Verse" preview were lost when navigating to that verse. Controls visibility of main and reference text sources together. No voice recognition. Inactive books styled gold/bold.

# --- INSTALLATION (Run this in your command prompt/terminal) ---
# pip install customtkinter 

import obspython as obs
import tkinter as tk
from tkinter import scrolledtext, Listbox
import customtkinter as ctk
import xml.etree.ElementTree as ET
import os
import re
import unicodedata
import difflib
import json
import threading
import time
import textwrap
import traceback # For detailed error printing

# --- MAPPING & ORDERING TABLES ---
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
ENGLISH_TO_FRENCH = {"Genesis": "Genèse", "Exodus": "Exode", "Leviticus": "Lévitique", "Numbers": "Nombres", "Deuteronomy": "Deutéronome", "Joshua": "Josué", "Judges": "Juges", "Ruth": "Ruth", "1 Samuel": "1 Samuel", "2 Samuel": "2 Samuel", "1 Kings": "1 Rois", "2 Kings": "2 Rois", "1 Chronicles": "1 Chroniques", "2 Chronicles": "2 Chroniques", "Ezra": "Esdras", "Nehemiah": "Néhémie", "Esther": "Esther", "Job": "Job", "Psalms": "Psaumes", "Proverbs": "Proverbes", "Ecclesiastes": "Ecclésiaste", "Song of Solomon": "Cantique des Cantiques", "Isaiah": "Ésaïe", "Jeremiah": "Jérémie", "Lamentations": "Lamentations", "Ezekiel": "Ézéchiel", "Daniel": "Daniel", "Hosea": "Osée", "Joel": "Joël", "Amos": "Amos", "Obadiah": "Abdias", "Jonah": "Jonas", "Micah": "Michée", "Nahum": "Nahum", "Habakkuk": "Habacuc", "Zephaniah": "Sophonie", "Haggai": "Aggée", "Zechariah": "Zacharie", "Malachi": "Malachie", "Matthew": "Matthieu", "Mark": "Marc", "Luke": "Luc", "John": "Jean", "Acts": "Actes", "Romans": "Romains", "1 Corinthians": "1 Corinthiens", "2 Corinthians": "2 Corinthiens", "Galatians": "Galates", "Ephesians": "Éphésiens", "Philippians": "Philippiens", "Colossians": "Colossiens", "1 Thessalonians": "1 Thessaloniciens", "2 Thessalonians": "2 Thessaloniciens", "1 Timothy": "1 Timothée", "2 Timothy": "2 Timothée", "Titus": "Tite", "Philemon": "Philémon", "Hebrews": "Hébreux", "James": "Jacques", "1 Peter": "1 Pierre", "2 Peter": "2 Pierre", "1 John": "1 Jean", "2 John": "2 Jean", "3 John": "3 Jean", "Jude": "Jude", "Revelation": "Apocalypse"}
KIRUNDI_TO_FRENCH = {"Itanguriro": "Genèse", "Kuvayo": "Exode", "Abalevi": "Lévitique", "Guharūra": "Nombres", "Gusubira mu vyagezwe": "Deutéronome", "Yosuwa": "Josué", "Abacamanza": "Juges", "Rusi": "Ruth", "1 Samweli": "1 Samuel", "2 Samweli": "2 Samuel", "1 Abami": "1 Rois", "2 Abami": "2 Rois", "1 Ngoma": "1 Chroniques", "2 Ngoma": "2 Chroniques", "Ezira": "Esdras", "Nehemiya": "Néhémie", "Esiteri": "Esther", "Yobu": "Job", "Zaburi": "Psaumes", "Imigani": "Proverbes", "Umusiguzi": "Ecclésiaste", "Indirimbo ya Salomo": "Cantique des Cantiques", "Izaya": "Ésaïe", "Yeremiya": "Jérémie", "Gucura intimba": "Lamentations", "Ezekiyeli": "Ézéchiel", "Daniyeli": "Daniel", "Hoseya": "Osée", "Yoweli": "Joël", "Amosi": "Amos", "Obadiya": "Abdias", "Yona": "Jonas", "Mika": "Michée", "Nahumu": "Nahum", "Habakuki": "Habacuc", "Zefaniya": "Sophonie", "Hagayi": "Aggée", "Zekariya": "Zacharie", "Malaki": "Malachie", "Matayo": "Matthieu", "Mariko": "Marc", "Luka": "Luc", "Yohani": "Jean", "Ivyakozwe": "Actes", "Abaroma": "Romains", "1 Abakorinto": "1 Corinthiens", "2 Abakorinto": "2 Corinthiens", "Abagalatiya": "Galates", "Abanyefeso": "Éphésiens", "Abafilipi": "Philippiens", "Abakolosayi": "Colossiens", "1 Abatesalonika": "1 Thessaloniciens", "2 Abatesalonika": "2 Thessaloniciens", "1 Timoteyo": "1 Timothée", "2 Timoteyo": "2 Timothée", "Tito": "Tite", "Filemoni": "Philémon", "Abaheburayo": "Hébreux", "Yakobo": "Jacques", "1 Petero": "1 Pierre", "2 Petero": "2 Pierre", "1 Yohani": "1 Jean", "2 Yohani": "2 Jean", "3 Yohani": "3 Jean", "Yuda": "Jude", "Ivyahishuriwe": "Apocalypse"}
CANONICAL_BOOK_ORDER = list(OSIS_TO_FRENCH_BOOK_NAMES.keys())

# --- GLOBAL VARIABLES ---
bible_manager = None
# speech_handler supprimé
SETTINGS_FILE = os.path.join(os.path.expanduser("~"), "obs_bible_presenter_settings_v3.json")

# ----------------------------------------------------------------------
# --- Speech Recognition Handler (Supprimé) ---
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# --- BibleManager Class ---
# ----------------------------------------------------------------------
class BibleManager:
    def __init__(self):
        self.navigator_window = None; self.text_source_name = ""; self.reference_source_name = ""; self.bibles = {}; self.active_bible_name = None
        self.current_book_id, self.current_book_name, self.current_chapter, self.current_verse_index = "", "", 0, -1
        self.display_blocks, self.current_block_index = [], -1; self.next_verse_info_cache, self.modified_next_verse_text = {}, None; self.searchable_books = []
        
        # --- MODIFICATION ICI (Suppression speech_enabled et microphone_index) ---
        self.settings = { 
            "bible_folder_path": "", 
            "favorites": [], 
            "search_history": [], 
            "theme": "System", 
            "ref_template": "{livre} {chapitre}:{verset}", 
            # "speech_enabled": False, # Supprimé
            "max_words_per_line": 4, 
            "max_lines_per_block": 4
            # "microphone_index": None # Supprimé
        }
        # --- FIN MODIFICATION ---
        
        self._load_settings()
    def _load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f: 
                    loaded_settings = json.load(f)
                    # Supprimer les anciennes clés si elles existent
                    loaded_settings.pop("speech_enabled", None)
                    loaded_settings.pop("microphone_index", None)
                    self.settings.update(loaded_settings)
        except Exception as e: print(f"Error loading settings: {e}")
    def save_settings(self):
        try:
            # S'assurer que les clés supprimées ne sont pas sauvegardées
            settings_to_save = self.settings.copy()
            settings_to_save.pop("speech_enabled", None)
            settings_to_save.pop("microphone_index", None)
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f: json.dump(settings_to_save, f, indent=4)
        except IOError as e: print(f"Error saving settings: {e}")
    def add_to_search_history(self, query):
        history = self.settings["search_history"];
        if query in history: history.remove(query)
        history.insert(0, query); self.settings["search_history"] = history[:10]; self.save_settings()
    def add_favorite(self):
        if not self.active_bible_name or not self.current_book_id or self.current_verse_index <= 0: return
        book_name = self.get_active_bible_data()['data'][self.current_book_id]['name']; ref_str = f"{book_name} {self.current_chapter}:{self.current_verse_index}"
        for fav in self.settings["favorites"]:
            if fav['ref_str'] == ref_str and fav['bible_name'] == self.active_bible_name: return
        fav = {"bible_name": self.active_bible_name, "book_name": book_name, "chapter": self.current_chapter, "verse": self.current_verse_index, "ref_str": ref_str}
        self.settings["favorites"].append(fav); self.save_settings();
        if self.navigator_window: self.navigator_window.update_favorites_list()
    def remove_favorite(self, fav_to_remove):
        self.settings["favorites"] = [fav for fav in self.settings["favorites"] if fav != fav_to_remove]; self.save_settings();
        if self.navigator_window: self.navigator_window.update_favorites_list()
    def _normalize_text(self, text): return ''.join(c for c in unicodedata.normalize('NFD', text.lower()) if unicodedata.category(c) != 'Mn')
    def load_bibles_from_folder(self, folder_path):
        self.settings["bible_folder_path"] = folder_path
        if not folder_path or not os.path.isdir(folder_path): self.bibles.clear(); self.active_bible_name = None; return
        print("Loading Bibles..."); self.bibles.clear()
        for f in os.listdir(folder_path):
            if f.lower().endswith('.xml'):
                bible_name = os.path.splitext(f)[0]; path = os.path.join(folder_path, f)
                bible_data = {'path': path, 'data': {}, 'flat_data': [], 'ordered_books': []}
                try:
                    tree = ET.parse(path); root = tree.getroot(); namespace = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
                    for book_node in root.findall('.//osis:div[@type="book"]', namespace):
                        book_id = book_node.get('osisID')
                        if book_id:
                            book_name_fr = OSIS_TO_FRENCH_BOOK_NAMES.get(book_id, book_id)
                            bible_data['data'][book_id] = {'name': book_name_fr, 'chapters': {}}; bible_data['ordered_books'].append({'id': book_id, 'name': book_name_fr})
                            for chapter_node in book_node.findall('osis:chapter', namespace):
                                chapter_num = int(chapter_node.get('osisID').split('.')[-1]); bible_data['data'][book_id]['chapters'][chapter_num] = [""]
                                for verse_node in chapter_node.findall('osis:verse', namespace):
                                    verse_num = int(verse_node.get('osisID').split('.')[-1]); verse_text = (verse_node.text or "").strip()
                                    while len(bible_data['data'][book_id]['chapters'][chapter_num]) <= verse_num: bible_data['data'][book_id]['chapters'][chapter_num].append("")
                                    bible_data['data'][book_id]['chapters'][chapter_num][verse_num] = verse_text
                                    bible_data['flat_data'].append({'book_id': book_id, 'book_name': book_name_fr, 'chapter': chapter_num, 'verse': verse_num, 'text': verse_text, 'norm_text': self._normalize_text(verse_text)})
                    self.bibles[bible_name] = bible_data
                except Exception as e: print(f"Error loading {bible_name}: {e}")
        if self.bibles and (self.active_bible_name not in self.bibles): self.set_active_bible(list(self.bibles.keys())[0])
        else: self._build_searchable_books_list()
        if self.navigator_window: self.navigator_window.update_all_ui()
    def set_active_bible(self, name):
        if name in self.bibles:
            self.active_bible_name = name; self._build_searchable_books_list()
            if self.navigator_window: self.navigator_window.after(10, self.navigator_window.update_book_list)
    def get_active_bible_data(self): return self.bibles.get(self.active_bible_name)
    def _build_searchable_books_list(self):
        self.searchable_books = []; active_bible = self.get_active_bible_data()
        if not active_bible: return
        book_names_in_bible = {b['name'] for b in active_bible['ordered_books']}
        for b in active_bible['ordered_books']: self.searchable_books.append({'norm_name': self._normalize_text(b['name']), 'display_name': b['name'], 'french_name': b['name']})
        for en, fr in ENGLISH_TO_FRENCH.items():
            if fr in book_names_in_bible: self.searchable_books.append({'norm_name': self._normalize_text(en), 'display_name': en, 'french_name': fr})
        for ki, fr in KIRUNDI_TO_FRENCH.items():
            if fr in book_names_in_bible: self.searchable_books.append({'norm_name': self._normalize_text(ki), 'display_name': ki, 'french_name': fr})
    def get_books(self):
        active_bible = self.get_active_bible_data();
        if not active_bible: return []
        def sort_key(book_info):
            try: return CANONICAL_BOOK_ORDER.index(book_info['id'])
            except: return 999
        return sorted(active_bible['ordered_books'], key=sort_key)
    def get_book_id_by_name(self, name):
        active_bible = self.get_active_bible_data();
        if not active_bible: return None
        norm_name_to_find = self._normalize_text(name)
        for book_id, data in active_bible['data'].items():
            if self._normalize_text(data['name']) == norm_name_to_find: return book_id
        for searchable in self.searchable_books:
            if self._normalize_text(searchable['display_name']) == norm_name_to_find:
                french_name = searchable['french_name']
                for book_id, data in active_bible['data'].items():
                        if data['name'] == french_name: return book_id
        return None
    def get_chapters_for_book(self, book_name):
        book_id = self.get_book_id_by_name(book_name);
        try: return sorted(self.get_active_bible_data()['data'][book_id]['chapters'].keys())
        except: return []
    def get_verses_for_chapter(self, book_name, chapter_num):
        book_id = self.get_book_id_by_name(book_name);
        try: return list(range(1, len(self.get_active_bible_data()['data'][book_id]['chapters'][chapter_num])))
        except: return []

    def _auto_format_verse_for_editor(self, verse_text):
        try:
            max_words = int(self.settings.get('max_words_per_line', 4))
        except ValueError:
            max_words = 4
        try:
            max_lines = int(self.settings.get('max_lines_per_block', 4))
        except ValueError:
            max_lines = 4

        # Si les deux sont désactivés (0), on ne fait rien
        if max_words <= 0 and max_lines <= 0:
            return verse_text

        final_blocks = []
        # On respecte les paragraphes saisis par l'utilisateur (\n\n)
        initial_paragraphs = verse_text.split('\n\n')

        for para in initial_paragraphs:
            para = para.strip()
            if not para:
                continue

            # --- Étape 1 : Mots Max par Ligne ---
            # On remplace les sauts de ligne simples (\n) par des espaces
            text = para.replace('\n', ' ').strip()
            words = text.split()
            
            wrapped_lines = []
            if max_words > 0:
                # On groupe les mots par "max_words"
                for i in range(0, len(words), max_words):
                    wrapped_lines.append(" ".join(words[i:i + max_words]))
            else:
                # Le "Word Wrap" est désactivé, on garde le paragraphe sur une seule ligne
                wrapped_lines.append(text) 
            
            # --- Étape 2 : Lignes Max par Bloc ---
            if max_lines > 0:
                # On groupe les lignes nouvellement créées par "max_lines"
                for i in range(0, len(wrapped_lines), max_lines):
                    chunk = wrapped_lines[i:i + max_lines]
                    final_blocks.append("\n".join(chunk))
            else:
                # Le "Split Bloc" est désactivé, tout le paragraphe est un seul bloc
                final_blocks.append("\n".join(wrapped_lines))

        # On retourne tous les blocs, séparés par \n\n
        return "\n\n".join(final_blocks)
    
    def set_passage(self, book_name, chapter, verse):
        book_id = self.get_book_id_by_name(book_name)
        if not book_id: print(f"Erreur: ID livre '{book_name}' non trouvé"); return

        chapter_int = int(chapter)
        verse_int = int(verse)

        # Vérifier si ce passage correspond au cache du verset suivant modifié
        use_modified = (self.modified_next_verse_text is not None and
                            self.next_verse_info_cache.get('book_id') == book_id and
                            self.next_verse_info_cache.get('chapter') == chapter_int and
                            self.next_verse_info_cache.get('verse_num') == verse_int)

        self.current_book_name = book_name
        self.current_book_id = book_id
        self.current_chapter = chapter_int
        self.current_verse_index = verse_int

        if use_modified:
            print(f"Application du texte modifié pour {book_name} {chapter}:{verse}")
            full_text = self.modified_next_verse_text
            self.modified_next_verse_text = None # Réinitialiser après utilisation
            # On suppose que le texte modifié est déjà formaté comme l'utilisateur le souhaite.
            formatted_text = full_text 
        else:
            full_text = self.get_current_verse_text()
            # On applique le formatage auto seulement si ce n'est pas un texte modifié.
            formatted_text = self._auto_format_verse_for_editor(full_text)
        
        self.display_blocks = [block.strip() for block in formatted_text.split('\n\n') if block.strip()]
        self.current_block_index = 0 if self.display_blocks else -1
        update_obs_text()
        if self.navigator_window: self.navigator_window.update_display()

    def reset_current_passage(self):
        self.current_book_id = ""; self.current_book_name = ""; self.current_chapter = 0; self.current_verse_index = -1
        self.display_blocks.clear(); self.current_block_index = -1; update_obs_text()
        if self.navigator_window: self.navigator_window.update_display()
    def navigate_block(self, direction):
        if not self.display_blocks: return
        new_index = self.current_block_index + direction
        if 0 <= new_index < len(self.display_blocks):
            self.current_block_index = new_index; update_obs_text()
            if self.navigator_window: self.navigator_window.update_block_display()
        else: self.navigate_verse(direction)
    def navigate_verse(self, direction):
        if not self.current_book_name: return
        verses = self.get_verses_for_chapter(self.current_book_name, self.current_chapter)
        next_verse = self.current_verse_index + direction
        if next_verse in verses: self.set_passage(self.current_book_name, self.current_chapter, next_verse)
    def get_current_verse_text(self):
        # Assurer que book_id est valide avant d'accéder aux données
        if not self.current_book_id: return ""
        try: return self.get_active_bible_data()['data'][self.current_book_id]['chapters'][self.current_chapter][self.current_verse_index]
        except (KeyError, IndexError): return "" # Gérer chapitre/verset invalide

    def get_formatted_obs_texts(self):
        if not self.current_book_id or self.current_verse_index <= 0: return {"reference": "", "main": ""}
        main_text = self.display_blocks[self.current_block_index] if 0 <= self.current_block_index < len(self.display_blocks) else ""
        ref_text = self.settings['ref_template'].format(livre=self.current_book_name, chapitre=self.current_chapter, verset=self.current_verse_index)
        return {"reference": ref_text, "main": main_text}

    def get_next_verse_info(self):
        self.next_verse_info_cache = {} # Réinitialiser le cache
        if not self.current_book_id or self.current_verse_index < 0: return "...", ""
        
        verses = self.get_verses_for_chapter(self.current_book_name, self.current_chapter)
        next_verse = self.current_verse_index + 1
        
        if next_verse in verses:
            text = self.get_active_bible_data()['data'][self.current_book_id]['chapters'][self.current_chapter][next_verse]
            ref = f"{self.current_book_name} {self.current_chapter}:{next_verse}"
            # Mettre à jour le cache avec les infos du verset suivant trouvé
            self.next_verse_info_cache = {
                'book_id': self.current_book_id,
                'chapter': self.current_chapter,
                'verse_num': next_verse
            }
            return ref, text
            
        return "Fin du chapitre", ""

    def update_next_verse_text(self, new_text): self.modified_next_verse_text = new_text
    def search(self, query):
        active_bible = self.get_active_bible_data();
        if not active_bible: return []
        query = query.strip()
        ref_match = re.match(r'^((\d\s)?[a-zA-Z\s]+)\s+(\d+)(?:\s*[:\s.,]\s*(\d+))?$', query, re.IGNORECASE)
        if ref_match:
            book_query, chapter_query, verse_str = self._normalize_text(ref_match.group(1).strip()), int(ref_match.group(3)), ref_match.group(4)
            verse_query = int(verse_str) if verse_str else None
            matched_books = [b for b in self.searchable_books if b['norm_name'].startswith(book_query)]
            if not matched_books:
                matches = difflib.get_close_matches(book_query, [b['norm_name'] for b in self.searchable_books], n=1, cutoff=0.6)
                if matches: matched_books = [b for b in self.searchable_books if b['norm_name'] == matches[0]]
            if not matched_books: print(f"Book not found for '{ref_match.group(1).strip()}'"); return []
            results = []; french_name = matched_books[0]['french_name']; book_id = self.get_book_id_by_name(french_name)
            if not book_id: print(f"ID not found for '{french_name}'"); return []
            if chapter_query not in active_bible['data'][book_id]['chapters']: print(f"Chapter {chapter_query} not found in {french_name}"); return []
            if verse_query is not None and (verse_query <= 0 or verse_query >= len(active_bible['data'][book_id]['chapters'][chapter_query])): print(f"Verse {verse_query} not found in {french_name} {chapter_query}"); return []
            for item in active_bible['flat_data']:
                if item['book_id'] == book_id and item['chapter'] == chapter_query:
                    if verse_query is None or item['verse'] == verse_query:
                        res = item.copy(); res['display_book_name'] = matched_books[0]['display_name']; results.append(res)
            return results
        else: # Keyword search
            keywords = self._normalize_text(query).split()
            if not keywords: return []
            results = [v.copy() for v in active_bible['flat_data'] if all(kw in v['norm_text'] for kw in keywords)]
            for res in results: res['display_book_name'] = res['book_name']
            return results


# ----------------------------------------------------------------------
# --- OBS Integration Functions ---
# ----------------------------------------------------------------------
def update_obs_text():
    global bible_manager;
    if not bible_manager: return
    formatted = bible_manager.get_formatted_obs_texts()
    update_source_text(bible_manager.text_source_name, formatted["main"])
    update_source_text(bible_manager.reference_source_name, formatted["reference"])
def update_source_text(source_name, text):
    if not source_name: return
    source = obs.obs_get_source_by_name(source_name)
    if source: settings = obs.obs_data_create(); obs.obs_data_set_string(settings, "text", text); obs.obs_source_update(source, settings); obs.obs_data_release(settings); obs.obs_source_release(source)
def get_scene_item_visibility(source_name):
    if not source_name: return False
    source = obs.obs_get_source_by_name(source_name);
    if not source: return False
    current_scene_source = obs.obs_frontend_get_current_scene();
    if not current_scene_source: obs.obs_source_release(source); return False
    current_scene = obs.obs_scene_from_source(current_scene_source); scene_item = obs.obs_scene_find_source_recursive(current_scene, source_name)
    visible = False;
    if scene_item: visible = obs.obs_sceneitem_visible(scene_item)
    obs.obs_source_release(current_scene_source); obs.obs_source_release(source); return visible
def set_scene_item_visibility(source_name, visible):
    if not source_name: return # Ne rien faire si le nom de source est vide
    source = obs.obs_get_source_by_name(source_name);
    if not source: print(f"Source '{source_name}' not found."); return
    current_scene_source = obs.obs_frontend_get_current_scene();
    if not current_scene_source: obs.obs_source_release(source); print("Current scene not found."); return
    current_scene = obs.obs_scene_from_source(current_scene_source); scene_item = obs.obs_scene_find_source_recursive(current_scene, source_name)
    if scene_item: obs.obs_sceneitem_set_visible(scene_item, visible); #print(f"Visibility of '{source_name}' set to {'Visible' if visible else 'Hidden'}.")
    else: print(f"Scene item '{source_name}' not found in the current scene hierarchy.")
    obs.obs_source_release(current_scene_source); obs.obs_source_release(source)
def on_hotkey_pressed(hotkey_id, pressed):
    if pressed and bible_manager:
        if hotkey_id == "bible_next": bible_manager.navigate_block(1)
        elif hotkey_id == "bible_prev": bible_manager.navigate_block(-1)
        elif hotkey_id == "bible_next_verse": bible_manager.navigate_verse(1)
        elif hotkey_id == "bible_prev_verse": bible_manager.navigate_verse(-1)

# ----------------------------------------------------------------------
# --- Modern UI ---
# ----------------------------------------------------------------------
class BibleNavigator(ctk.CTk):
    def __init__(self, manager):
        super().__init__(); self.manager = manager; ctk.set_appearance_mode(self.manager.settings["theme"])
        self.title("OBS Bible Presenter 3.0"); self.geometry("1000x700")
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(0, weight=1)
        self.search_results_data = []
        # --- NOUVEAU : Police en gras ---
        self.bold_font = ctk.CTkFont(weight="bold")
        # --- FIN NOUVEAU ---
        
        self._create_sidebar(); self._create_main_content(); self.update_all_ui()
        self.editor_text.tag_configure("active_block", font=("Segoe UI", 14, "bold"), foreground="#3498db")
        self.editor_text.bind("<KeyRelease>", self.on_editor_key_release)
        self.preview_text.bind("<KeyRelease>", self.on_preview_key_release)
        self.sync_visibility_toggle()

    def _create_sidebar(self):
        sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0); sidebar_frame.grid(row=0, column=0, sticky="nsw"); sidebar_frame.grid_rowconfigure(3, weight=1) # Row index adjusted
        ctk.CTkLabel(sidebar_frame, text="Navigation", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=20)
        self.bible_combo = ctk.CTkComboBox(sidebar_frame, values=[], command=self.on_bible_selected); self.bible_combo.grid(row=1, column=0, padx=20, pady=(0,10), sticky="ew") # Adjusted pady
        nav_frame = ctk.CTkFrame(sidebar_frame, fg_color="transparent"); nav_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew"); nav_frame.columnconfigure((0,1), weight=1) # Row index adjusted
        self.chapter_combo = ctk.CTkComboBox(nav_frame, values=[], command=self.on_chapter_selected); self.chapter_combo.grid(row=0, column=0, padx=(0,5), sticky="ew")
        self.verse_combo = ctk.CTkComboBox(nav_frame, values=[], command=self.on_verse_selected); self.verse_combo.grid(row=0, column=1, padx=(5,0), sticky="ew")
        self.book_list_frame = ctk.CTkScrollableFrame(sidebar_frame, label_text="Livre"); self.book_list_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew"); self.book_buttons = {} # Row index adjusted

    def _create_main_content(self):
        main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent"); main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20);
        main_frame.grid_rowconfigure(1, weight=1);
        main_frame.grid_columnconfigure(0, weight=1);
        main_frame.grid_columnconfigure(1, weight=0);

        self.current_ref_label = ctk.CTkLabel(main_frame, text="Aucun passage sélectionné", font=ctk.CTkFont(size=24, weight="bold"), anchor="w");
        self.current_ref_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        self.tab_view = ctk.CTkTabview(main_frame, anchor="w");
        self.tab_view.grid(row=1, column=0, sticky="nsew")
        self.tab_view.add("Éditeur"); self.tab_view.add("Recherche"); self.tab_view.add("⭐ Favoris"); self.tab_view.add("Paramètres")
        self._create_editor_tab(); self._create_search_tab(); self._create_favorites_tab(); self._create_settings_tab()

        self.visibility_switch = ctk.CTkSwitch(main_frame, text="Show Text / Ref", command=self.toggle_text_source_visibility, progress_color="grey", switch_width=50, switch_height=25)
        self.visibility_switch.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky="ne")

    def _create_editor_tab(self):
        editor_tab = self.tab_view.tab("Éditeur"); editor_tab.grid_rowconfigure(0, weight=3); editor_tab.grid_rowconfigure(2, weight=2); editor_tab.grid_columnconfigure(0, weight=1)
        editor_frame = ctk.CTkFrame(editor_tab, fg_color=("gray90", "gray20")); editor_frame.grid(row=0, column=0, sticky="nsew", pady=(0,10)); editor_frame.grid_rowconfigure(0, weight=1); editor_frame.grid_columnconfigure(0, weight=1)
        self.editor_text = tk.Text(editor_frame, wrap=tk.WORD, relief="flat", borderwidth=0, font=("Segoe UI", 14), undo=True, height=10); self.editor_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        control_frame = ctk.CTkFrame(editor_tab, fg_color="transparent"); control_frame.grid(row=1, column=0, sticky="ew", pady=5); control_frame.columnconfigure((0,1,2,3), weight=1)
        ctk.CTkButton(control_frame, text="⭐ Favoris", command=self.manager.add_favorite).grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(control_frame, text="<< Préc.", command=lambda: self.manager.navigate_block(-1)).grid(row=0, column=1, padx=5, sticky="ew")
        ctk.CTkButton(control_frame, text="Suiv. >>", command=lambda: self.manager.navigate_block(1)).grid(row=0, column=2, padx=5, sticky="ew")
        ctk.CTkButton(control_frame, text="Vider", command=self.manager.reset_current_passage).grid(row=0, column=3, padx=5, sticky="ew")
        
        preview_frame = ctk.CTkFrame(editor_tab); preview_frame.grid(row=2, column=0, sticky="nsew"); preview_frame.grid_rowconfigure(1, weight=1); preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_ref_label = ctk.CTkLabel(preview_frame, text="Verset Suivant: ...", anchor="w"); self.preview_ref_label.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.preview_text = tk.Text(preview_frame, wrap=tk.WORD, relief="flat", borderwidth=0, font=("Segoe UI", 11), undo=True, height=5); self.preview_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.status_label = ctk.CTkLabel(editor_tab, text="", anchor="center"); self.status_label.grid(row=3, column=0, sticky="ew", pady=(10, 0))

    def _create_search_tab(self):
        search_tab = self.tab_view.tab("Recherche"); search_tab.grid_rowconfigure(1, weight=1); search_tab.grid_columnconfigure(0, weight=1)
        search_bar_frame = ctk.CTkFrame(search_tab, fg_color="transparent"); search_bar_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5); search_bar_frame.grid_columnconfigure(0, weight=1)
        self.search_combo = ctk.CTkComboBox(search_bar_frame, values=self.manager.settings["search_history"], command=lambda q: self.perform_search()); self.search_combo.grid(row=0, column=0, sticky="ew", padx=(0, 10)); self.search_combo.bind("<Return>", self.perform_search)
        search_button = ctk.CTkButton(search_bar_frame, text="Rechercher", width=100, command=self.perform_search); search_button.grid(row=0, column=1)
        results_frame = ctk.CTkFrame(search_tab); results_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5); results_frame.grid_rowconfigure(0, weight=1); results_frame.grid_columnconfigure(0, weight=1)
        self.results_listbox = Listbox(results_frame, font=("Segoe UI", 11), relief="flat", borderwidth=0); self.results_listbox.grid(row=0, column=0, sticky="nsew"); self.results_listbox.bind("<Double-1>", self.on_result_selected)

    def _create_favorites_tab(self):
        fav_tab = self.tab_view.tab("⭐ Favoris"); fav_tab.grid_rowconfigure(0, weight=1); fav_tab.grid_columnconfigure(0, weight=1)
        fav_frame = ctk.CTkFrame(fav_tab); fav_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5); fav_frame.grid_rowconfigure(0, weight=1); fav_frame.grid_columnconfigure(0, weight=1)
        self.favorites_listbox = Listbox(fav_frame, font=("Segoe UI", 11), relief="flat", borderwidth=0); self.favorites_listbox.grid(row=0, column=0, sticky="nsew"); self.favorites_listbox.bind("<Double-1>", self.on_favorite_selected)
        remove_button = ctk.CTkButton(fav_tab, text="Retirer le favori sélectionné", command=self.remove_selected_favorite); remove_button.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

    # --- MÉTHODE MODIFIÉE (Suppression des options micro/speech) ---
    def _create_settings_tab(self):
        settings_tab = self.tab_view.tab("Paramètres"); settings_tab.grid_columnconfigure(1, weight=1)
        
        # Row 0: Theme
        ctk.CTkLabel(settings_tab, text="Thème de l'application:").grid(row=0, column=0, padx=20, pady=10, sticky="w"); 
        self.theme_menu = ctk.CTkOptionMenu(settings_tab, values=["Light", "Dark", "System"], command=self.change_theme)
        self.theme_menu.set(self.manager.settings["theme"])
        self.theme_menu.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        
        # Row 1, 2: Reference Template
        ctk.CTkLabel(settings_tab, text="Modèle de référence:").grid(row=1, column=0, padx=20, pady=10, sticky="w"); 
        self.ref_template_entry = ctk.CTkEntry(settings_tab)
        self.ref_template_entry.insert(0, self.manager.settings["ref_template"])
        self.ref_template_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        ctk.CTkLabel(settings_tab, text="Variables: {livre}, {chapitre}, {verset}", text_color="gray").grid(row=2, column=1, padx=20, sticky="w")
        
        # Row 3, 4: Max Words per Line
        ctk.CTkLabel(settings_tab, text="Mots Max par Ligne:").grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.max_words_entry = ctk.CTkEntry(settings_tab)
        self.max_words_entry.insert(0, str(self.manager.settings.get("max_words_per_line", 4)))
        self.max_words_entry.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        ctk.CTkLabel(settings_tab, text="0 = désactiver le retour à la ligne auto.", text_color="gray").grid(row=4, column=1, padx=20, sticky="w")

        # Row 5, 6: Max Lines per Block
        ctk.CTkLabel(settings_tab, text="Lignes Max par Bloc:").grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.max_lines_entry = ctk.CTkEntry(settings_tab)
        self.max_lines_entry.insert(0, str(self.manager.settings.get("max_lines_per_block", 4)))
        self.max_lines_entry.grid(row=5, column=1, padx=20, pady=10, sticky="ew")
        ctk.CTkLabel(settings_tab, text="0 = désactiver la division de bloc auto.", text_color="gray").grid(row=6, column=1, padx=20, sticky="w")
        
        # Row 7: Save Button (Row number updated)
        save_button = ctk.CTkButton(settings_tab, text="Enregistrer les paramètres", command=self.save_all_settings); 
        save_button.grid(row=7, column=1, padx=20, pady=20, sticky="e") 

    # Méthodes supprimées: update_listening_indicator, toggle_speech_recognition, handle_voice_command

    def on_editor_key_release(self, event=None):
        current_text = self.editor_text.get("1.0", tk.END).strip()
        # Ne pas réappliquer le formatage auto ici, seulement couper par \n\n
        self.manager.display_blocks = [block.strip() for block in current_text.split('\n\n') if block.strip()]
        if self.manager.current_block_index >= len(self.manager.display_blocks): self.manager.current_block_index = max(0, len(self.manager.display_blocks) - 1)
        update_obs_text(); self._highlight_active_block()
        
    def on_preview_key_release(self, event=None): 
        # Sauvegarde le texte tel quel, sans formatage auto
        self.manager.update_next_verse_text(self.preview_text.get("1.0", tk.END).strip())

    def perform_search(self, event=None):
        query = self.search_combo.get();
        if not query: return
        self.manager.add_to_search_history(query); self.update_search_history()
        results = self.manager.search(query); self.search_results_data = results; self.results_listbox.delete(0, tk.END)
        if not results: self.results_listbox.insert(tk.END, " Aucun résultat trouvé.")
        else:
            for item in results: self.results_listbox.insert(tk.END, f" {item['display_book_name']} {item['chapter']}:{item['verse']} - {item['text'][:80].replace(chr(10), ' ')}...")
    def on_result_selected(self, event=None):
        if not self.results_listbox.curselection(): return
        idx = self.results_listbox.curselection()[0]
        if "Aucun résultat trouvé" in self.results_listbox.get(idx): return
        data = self.search_results_data[idx]; self.manager.set_passage(data['book_name'], data['chapter'], data['verse'])
        self.sync_nav_to_current_verse(); self.tab_view.set("Éditeur")
    def on_favorite_selected(self, event=None):
        if not self.favorites_listbox.curselection(): return
        fav = self.manager.settings["favorites"][self.favorites_listbox.curselection()[0]]
        self.manager.set_active_bible(fav['bible_name'])
        self.after(50, lambda fav=fav: self.manager.set_passage(fav['book_name'], fav['chapter'], fav['verse']))
        self.after(100, self.sync_nav_to_current_verse); self.tab_view.set("Éditeur")
    def remove_selected_favorite(self):
        if not self.favorites_listbox.curselection(): return
        fav = self.manager.settings["favorites"][self.favorites_listbox.curselection()[0]]; self.manager.remove_favorite(fav)
    def on_bible_selected(self, bible_name): self.manager.set_active_bible(bible_name)
    
    # --- MÉTHODE MODIFIÉE (Style des boutons) ---
    def on_book_selected(self, book_info):
        # Réinitialiser tous les boutons au style inactif (or, gras, transparent)
        for btn in self.book_buttons.values(): 
            btn.configure(fg_color="transparent", text_color="gold") # Police déjà en gras
            
        # Appliquer le style actif au bouton cliqué (fond gris, texte par défaut)
        selected_button = self.book_buttons.get(book_info['name'])
        if selected_button:
            selected_button.configure(fg_color=("gray85", "gray20"), text_color=ctk.ThemeManager.theme["CTkButton"]["text_color"]) # Utilise la couleur par défaut du thème
            
        self._selected_book_name = book_info['name']
        chapters = self.manager.get_chapters_for_book(book_info['name']); str_ch = [str(c) for c in chapters]; self.chapter_combo.configure(values=str_ch)
        if str_ch: self.chapter_combo.set(str_ch[0]); self.on_chapter_selected(str_ch[0])
        else: self.chapter_combo.set(""); self.verse_combo.configure(values=[]); self.verse_combo.set("")

    def on_chapter_selected(self, chapter):
        book = getattr(self, '_selected_book_name', None);
        if not chapter or not book: return
        self._selected_chapter = int(chapter)
        verses = self.manager.get_verses_for_chapter(book, int(chapter)); str_v = [str(v) for v in verses]; self.verse_combo.configure(values=str_v)
        if str_v: self.verse_combo.set(str_v[0]); self.on_verse_selected(str_v[0])
        else: self.verse_combo.set("")
    def on_verse_selected(self, verse):
        book = getattr(self, '_selected_book_name', None); chapter = getattr(self, '_selected_chapter', None)
        if not verse or not book or chapter is None: return
        try: self.manager.set_passage(book, chapter, verse)
        except Exception as e: print(f"Error setting passage: {e}")
    def update_all_ui(self): self.update_bible_list(); self.update_search_history(); self.update_favorites_list(); self.sync_visibility_toggle()
    def update_bible_list(self):
        bibles = list(self.manager.bibles.keys()); self.bible_combo.configure(values=bibles); current = self.manager.active_bible_name
        if current and current in bibles: self.bible_combo.set(current)
        elif bibles: self.bible_combo.set(bibles[0]); self.manager.set_active_bible(bibles[0])
        else: self.bible_combo.set("")
        self.update_book_list()
        
    # --- MÉTHODE MODIFIÉE (Style des boutons) ---
    def update_book_list(self):
        for w in self.book_list_frame.winfo_children(): w.destroy(); self.book_buttons.clear()
        books = self.manager.get_books()
        for book in books:
            # Appliquer le style par défaut ici (gras, or, transparent)
            btn = ctk.CTkButton(self.book_list_frame, 
                                text=book['name'], 
                                fg_color="transparent", 
                                text_color="gold", # Couleur or pour inactif
                                font=self.bold_font, # Police en gras
                                anchor="w", 
                                command=lambda b=book: self.on_book_selected(b))
            btn.pack(fill="x", pady=2); 
            self.book_buttons[book['name']] = btn
        self.sync_nav_to_current_verse() # Applique le style actif si nécessaire

    def update_display(self):
        ref = self.manager.get_formatted_obs_texts()["reference"]; self.current_ref_label.configure(text=ref or "Aucun passage")
        self.editor_text.delete("1.0", tk.END); self.editor_text.insert("1.0", "\n\n".join(self.manager.display_blocks))
        self.update_block_display(); self.update_next_verse_preview()
    def update_block_display(self):
        self.status_label.configure(text=f"Page {self.manager.current_block_index + 1} / {len(self.manager.display_blocks) if self.manager.display_blocks else 1}")
        self._highlight_active_block()
    
    def update_next_verse_preview(self):
        ref, text = self.manager.get_next_verse_info(); self.preview_ref_label.configure(text=f"Verset Suivant: {ref}")
        
        # Applique le même formatage auto que pour le verset principal
        formatted_text = self.manager._auto_format_verse_for_editor(text) 
        
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", formatted_text) # Utilise le texte formaté
    
    def _highlight_active_block(self):
        self.editor_text.tag_remove("active_block", "1.0", tk.END)
        if self.manager.current_block_index < 0 or not self.manager.display_blocks: return
        if self.manager.current_block_index >= len(self.manager.display_blocks): self.manager.current_block_index = max(0, len(self.manager.display_blocks) - 1);
        if self.manager.current_block_index < 0: return
        prev = "\n\n".join(self.manager.display_blocks[:self.manager.current_block_index]); offset = len(prev) + (len("\n\n") if self.manager.current_block_index > 0 else 0)
        curr_len = len(self.manager.display_blocks[self.manager.current_block_index]); start, end = f"1.0 + {offset} chars", f"1.0 + {offset + curr_len} chars"
        self.editor_text.tag_add("active_block", start, end)
        
    # --- MÉTHODE MODIFIÉE (Style des boutons) ---
    def sync_nav_to_current_verse(self):
        if self.manager.current_book_name and self.manager.current_chapter > 0 and self.manager.current_verse_index > 0:
            # Réinitialiser tous les boutons au style inactif (or, gras, transparent)
            for btn in self.book_buttons.values(): 
                btn.configure(fg_color="transparent", text_color="gold") # Police déjà en gras
            
            # Appliquer le style actif au bouton courant (fond gris, texte par défaut)
            current_button = self.book_buttons.get(self.manager.current_book_name)
            if current_button:
                 current_button.configure(fg_color=("gray85", "gray20"), text_color=ctk.ThemeManager.theme["CTkButton"]["text_color"]) # Utilise la couleur par défaut du thème
                 self._selected_book_name = self.manager.current_book_name
                 
            chapters = self.manager.get_chapters_for_book(self.manager.current_book_name); str_ch = [str(c) for c in chapters]; current_ch_str = str(self.manager.current_chapter)
            self.chapter_combo.configure(values=str_ch);
            if current_ch_str in str_ch: self.chapter_combo.set(current_ch_str); self._selected_chapter = self.manager.current_chapter
            verses = self.manager.get_verses_for_chapter(self.manager.current_book_name, self.manager.current_chapter); str_v = [str(v) for v in verses]; current_v_str = str(self.manager.current_verse_index)
            self.verse_combo.configure(values=str_v);
            if current_v_str in str_v: self.verse_combo.set(current_v_str)
            elif str_v: self.verse_combo.set(str_v[0])
            else: self.verse_combo.set("")

    def update_favorites_list(self): self.favorites_listbox.delete(0, tk.END); [self.favorites_listbox.insert(tk.END, f" {fav['bible_name']} | {fav['ref_str']}") for fav in self.manager.settings["favorites"]]
    def update_search_history(self): self.search_combo.configure(values=self.manager.settings["search_history"])
    
    def toggle_text_source_visibility(self):
        is_visible = self.visibility_switch.get() == 1
        set_scene_item_visibility(self.manager.text_source_name, is_visible)
        # Ajout pour contrôler aussi la source de référence
        set_scene_item_visibility(self.manager.reference_source_name, is_visible)
        
    def sync_visibility_toggle(self):
        # Vérifie la visibilité de la source principale pour l'état initial du bouton.
        visible = get_scene_item_visibility(self.manager.text_source_name);
        if visible:
            self.visibility_switch.select()
        else:
            self.visibility_switch.deselect()
            
    def change_theme(self, new_theme): ctk.set_appearance_mode(new_theme)
    
    # --- MÉTHODE MODIFIÉE (Suppression sauvegarde speech/mic) ---
    def save_all_settings(self): 
        self.manager.settings["theme"] = self.theme_menu.get()
        self.manager.settings["ref_template"] = self.ref_template_entry.get()
        # self.manager.settings["speech_enabled"] = self.speech_switch.get() == 1 # Supprimé
        
        try:
            self.manager.settings["max_words_per_line"] = int(self.max_words_entry.get())
        except ValueError:
            self.manager.settings["max_words_per_line"] = 4 
        try:
            self.manager.settings["max_lines_per_block"] = int(self.max_lines_entry.get())
        except ValueError:
            self.manager.settings["max_lines_per_block"] = 4 
            
        # Suppression sauvegarde microphone_index
            
        self.manager.save_settings()
        update_obs_text() 
        
        # Rafraîchit l'affichage actuel avec les nouveaux paramètres
        if self.manager.current_book_name and self.manager.current_chapter > 0 and self.manager.current_verse_index > 0:
             self.manager.set_passage(self.manager.current_book_name, self.manager.current_chapter, self.manager.current_verse_index)

    # toggle_speech_recognition supprimé
    # handle_voice_command supprimé
        
    def on_closing(self):
        print("Fermeture fenêtre...");
        try: self.save_all_settings()
        except Exception as e: print(f"Err sauvegarde fermeture: {e}")
        self.manager.navigator_window = None; 
        # global speech_handler supprimé
        # Arrêt speech_handler supprimé
        try: print("Destruction fenêtre..."); self.destroy(); print("Fenêtre détruite.")
        except Exception as e: print(f"Err destruction fenêtre: {e}")

# ----------------------------------------------------------------------
# --- OBS Script Boilerplate ---
# ----------------------------------------------------------------------
def script_description(): 
    # Mise à jour pour enlever la reconnaissance vocale
    return """<h2>OBS Bible Presenter 3.0</h2>
              <p>A comprehensive suite for displaying the Bible in OBS.</p>
              <ul>
                  <li><b>Modern interface</b> and intuitive navigation.</li>
                  <li><b>Full Search:</b> Multi-language, keyword, history.</li>
                  <li><b>Full Editor:</b> Preview, instant update, controls, visibility toggle.</li>
                  <li><b>Favorites and Templates</b> for presentation.</li>
                  <li><b>Automatic text formatting</b> (max words per line, max lines per block).</li>
                  <li>Visibility toggle controls both main text and reference.</li>
                  <li>Inactive book buttons styled gold/bold.</li>
              </ul>
              <p><b>Installation:</b> Ensure you have installed the required library (customtkinter).</p>"""

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_path(props, "bible_folder", "Bible Folder (.xml)", obs.OBS_PATH_DIRECTORY, "", None) 
    main_list = obs.obs_properties_add_list(props, "text_source", "Main Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING) 
    ref_list = obs.obs_properties_add_list(props, "reference_source", "Reference Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING) 
    sources = obs.obs_enum_sources()
    if sources:
        for s in sources:
            source_id = obs.obs_source_get_unversioned_id(s)
            # Vérifier si c'est une source de texte (différentes versions)
            if source_id in ["text_gdiplus_v2", "text_ft2_source_v2", "text_gdiplus", "text_ft2_source"]:
                name = obs.obs_source_get_name(s)
                obs.obs_property_list_add_string(main_list, name, name)
                obs.obs_property_list_add_string(ref_list, name, name)
        obs.source_list_release(sources)
    obs.obs_properties_add_button(props, "navigator_button", "Open Navigator 3.0", open_navigator_callback) 
    return props

def script_load(settings):
    global bible_manager; bible_manager = BibleManager()
    bible_manager.text_source_name = obs.obs_data_get_string(settings, "text_source")
    bible_manager.reference_source_name = obs.obs_data_get_string(settings, "reference_source")
    folder = obs.obs_data_get_string(settings, "bible_folder")
    if not folder and bible_manager.settings["bible_folder_path"]: folder = bible_manager.settings["bible_folder_path"]; obs.obs_data_set_string(settings, "bible_folder", folder)
    bible_manager.load_bibles_from_folder(folder); setup_hotkeys()
def script_update(settings):
    global bible_manager;
    if not bible_manager: return
    bible_manager.text_source_name = obs.obs_data_get_string(settings, "text_source")
    bible_manager.reference_source_name = obs.obs_data_get_string(settings, "reference_source")
    new_folder = obs.obs_data_get_string(settings, "bible_folder")
    if new_folder != bible_manager.settings["bible_folder_path"]: bible_manager.load_bibles_from_folder(new_folder); bible_manager.save_settings()
    update_obs_text()
    if bible_manager.navigator_window and bible_manager.navigator_window.winfo_exists(): bible_manager.navigator_window.sync_visibility_toggle()
def script_unload():
    print("Déchargement script..."); global bible_manager # speech_handler supprimé
    if bible_manager and bible_manager.navigator_window and bible_manager.navigator_window.winfo_exists():
        print("Fermeture fenêtre...");
        try: bible_manager.navigator_window.on_closing() # on_closing gère la sauvegarde
        except Exception as e: print(f"Err fermeture déchargement: {e}")
    # Arrêt speech_handler supprimé
    bible_manager = None; print("Script déchargé.")
def open_navigator_callback(props, prop):
    global bible_manager
    if not bible_manager or not hasattr(bible_manager, 'settings'): print("BibleManager not initialized."); return
    if not bible_manager.navigator_window or not bible_manager.navigator_window.winfo_exists(): threading.Thread(target=run_ui, daemon=True).start()
    else: bible_manager.navigator_window.lift()
def run_ui():
    global bible_manager
    try:
        nav = BibleNavigator(bible_manager); bible_manager.navigator_window = nav
        nav.protocol("WM_DELETE_WINDOW", nav.on_closing); nav.mainloop()
    except Exception as e: print(f"Erreur majeure UI: {e}"); traceback.print_exc();
    if bible_manager: bible_manager.navigator_window = None
def setup_hotkeys():
    obs.obs_hotkey_register_frontend("bible_next", "Bible: Next Block", lambda p: on_hotkey_pressed("bible_next", p))
    obs.obs_hotkey_register_frontend("bible_prev", "Bible: Previous Block", lambda p: on_hotkey_pressed("bible_prev", p))
    obs.obs_hotkey_register_frontend("bible_next_verse", "Bible: Next Verse", lambda p: on_hotkey_pressed("bible_next_verse", p))
    obs.obs_hotkey_register_frontend("bible_prev_verse", "Bible: Previous Verse", lambda p: on_hotkey_pressed("bible_prev_verse", p))