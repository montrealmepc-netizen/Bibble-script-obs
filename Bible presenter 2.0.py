# CODE: OBS BIBLE PRESENTER 2.0
# AUTHOR: Inspired and developed for MEPC Montreal
# DESCRIPTION: Displays a verse and its reference on two separate OBS text sources.
#              Features a modern UI, search, favorites, and hotkeys.

import obspython as obs
import tkinter as tk
from tkinter import ttk, font, messagebox, scrolledtext
from ttkthemes import ThemedTk
import xml.etree.ElementTree as ET
import os
import re
import unicodedata
import difflib
import json
import threading
import time
import textwrap

# --- MAPPING TABLES (No changes here) ---
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

# --- Global Variable ---
bible_manager = None
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bible_mepc_settings.json")

# ----------------------------------------------------------------------
# --- BibleManager Class ---
# ----------------------------------------------------------------------
class BibleManager:
    def __init__(self):
        self.text_source_name = ""
        self.reference_source_name = "" # NEW: For the reference text source
        self.navigator_window = None
        self.bibles = {}
        self.active_bible_name = None
        self.bible_folder_path = ""
        self.favorites = []
        self.search_history = []
        self.display_blocks, self.current_block_index = [], -1
        self.current_book_id, self.current_chapter, self.current_verse_index = "", 0, -1
        self.next_verse_info_cache, self.modified_next_verse_text = {}, None
        self.searchable_books = []
        self.folder_watcher_thread = None
        self.stop_watcher_event = threading.Event()
        self.PARAGRAPH_THRESHOLD = 220 
        self.LINE_WRAP_WIDTH = 45
        self._load_settings()

    def _load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.favorites = settings.get("favorites", [])
                    self.search_history = settings.get("search_history", [])
                    self.bible_folder_path = settings.get("bible_folder_path", "")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading settings: {e}")

    def _save_settings(self):
        try:
            settings = {
                "bible_folder_path": self.bible_folder_path,
                "favorites": self.favorites,
                "search_history": self.search_history
            }
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
        except IOError as e:
            print(f"Error saving settings: {e}")
    
    # ... (No changes to add_to_search_history, add_favorite, remove_favorite, _normalize_text) ...
    def add_to_search_history(self, query):
        if query in self.search_history: self.search_history.remove(query)
        self.search_history.insert(0, query)
        self.search_history = self.search_history[:5]
        self._save_settings()

    def add_favorite(self):
        if not self.active_bible_name or not self.current_book_id: return
        book_name = self.get_active_bible_data()['data'][self.current_book_id]['name']
        ref_str = f"{book_name} {self.current_chapter}:{self.current_verse_index}"
        for fav in self.favorites:
            if fav['ref_str'] == ref_str and fav['bible_name'] == self.active_bible_name: return
        fav = {"bible_name": self.active_bible_name, "book_name": book_name, "chapter": self.current_chapter, "verse": self.current_verse_index, "ref_str": ref_str}
        self.favorites.append(fav)
        self._save_settings()
        if self.navigator_window: self.navigator_window.update_favorites_list()

    def remove_favorite(self, fav_to_remove):
        self.favorites = [fav for fav in self.favorites if fav != fav_to_remove]
        self._save_settings()
        if self.navigator_window: self.navigator_window.update_favorites_list()
        
    def _normalize_text(self, text):
        if not text: return ""
        return ''.join(c for c in unicodedata.normalize('NFD', text.lower()) if unicodedata.category(c) != 'Mn')

    def load_bibles_from_folder(self, folder_path):
        self.bible_folder_path = folder_path
        if not folder_path or not os.path.isdir(folder_path):
            self.bibles.clear(); self.active_bible_name = None
            if self.navigator_window: self.navigator_window.update_all_ui()
            return
        xml_files = {os.path.splitext(f)[0]: os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.xml')}
        if set(self.bibles.keys()) == set(xml_files.keys()): return
        print("Bible folder changed, reloading...")
        self.bibles.clear()
        for bible_name, path in xml_files.items():
            bible_data = {'path': path, 'data': {}, 'flat_data': [], 'ordered_books': []}
            try:
                ET.register_namespace("", "http://www.bibletechnologies.net/2003/OSIS/namespace")
                tree = ET.parse(path)
                root = tree.getroot()
                namespace = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
                for book_node in root.findall('.//osis:div[@type="book"]', namespace):
                    book_id = book_node.get('osisID')
                    if book_id:
                        book_name_fr = OSIS_TO_FRENCH_BOOK_NAMES.get(book_id, book_id)
                        bible_data['data'][book_id] = {'name': book_name_fr, 'chapters': {}}
                        bible_data['ordered_books'].append(book_name_fr)
                        for chapter_node in book_node.findall('osis:chapter', namespace):
                            try:
                                chapter_num = int(chapter_node.get('osisID').split('.')[-1])
                                bible_data['data'][book_id]['chapters'][chapter_num] = [""]
                                for verse_node in chapter_node.findall('osis:verse', namespace):
                                    verse_text, verse_num = verse_node.text or "", int(verse_node.get('osisID').split('.')[-1])
                                    bible_data['data'][book_id]['chapters'][chapter_num].append(verse_text)
                                    bible_data['flat_data'].append({'book_id': book_id, 'book_name': book_name_fr, 'chapter': chapter_num, 'verse': verse_num, 'text': verse_text, 'norm_text': self._normalize_text(verse_text)})
                            except (ValueError, IndexError): pass
                self.bibles[bible_name] = bible_data
            except Exception as e:
                print(f"Error loading Bible {bible_name}: {e}")
        if self.bibles:
            if self.active_bible_name not in self.bibles:
                self.set_active_bible(list(self.bibles.keys())[0])
        else: self.active_bible_name = None
        self._build_searchable_books_list()
        self.reset_current_passage()
        if self.navigator_window:
            self.navigator_window.after(0, self.navigator_window.update_all_ui)
        print(f"{len(self.bibles)} Bibles loaded.")

    # ... (No changes to _watch_folder, start_folder_watcher, stop_folder_watcher, set_active_bible) ...
    def _watch_folder(self):
        while not self.stop_watcher_event.is_set():
            try:
                self.load_bibles_from_folder(self.bible_folder_path)
            except Exception as e:
                print(f"Error in folder watcher: {e}")
            time.sleep(5)

    def start_folder_watcher(self):
        if self.folder_watcher_thread is None or not self.folder_watcher_thread.is_alive():
            self.stop_watcher_event.clear()
            self.folder_watcher_thread = threading.Thread(target=self._watch_folder, daemon=True)
            self.folder_watcher_thread.start()
            print("Folder watcher started.")

    def stop_folder_watcher(self):
        self.stop_watcher_event.set()
        if self.folder_watcher_thread and self.folder_watcher_thread.is_alive():
            self.folder_watcher_thread.join(timeout=1)
        print("Folder watcher stopped.")

    def set_active_bible(self, bible_name):
        if bible_name in self.bibles:
            self.active_bible_name = bible_name
            self._build_searchable_books_list()
            self.reset_current_passage()
            if self.navigator_window: self.navigator_window.update_all_ui()
            
    # ... (The rest of the BibleManager class is mostly unchanged, only adding get_current_reference_string) ...
    def get_active_bible_data(self):
        return self.bibles.get(self.active_bible_name)
        
    def _build_searchable_books_list(self):
        self.searchable_books = []
        active_bible = self.get_active_bible_data()
        if not active_bible: return
        ordered_books = active_bible['ordered_books']
        for name in ordered_books:
            self.searchable_books.append({'norm_name': self._normalize_text(name), 'display_name': name, 'french_name': name})
        for en_name, fr_name in ENGLISH_TO_FRENCH.items():
            if fr_name in ordered_books:
                self.searchable_books.append({'norm_name': self._normalize_text(en_name), 'display_name': en_name, 'french_name': fr_name})
        for kr_name, fr_name in KIRUNDI_TO_FRENCH.items():
            if fr_name in ordered_books:
                self.searchable_books.append({'norm_name': self._normalize_text(kr_name), 'display_name': kr_name, 'french_name': fr_name})

    def save_verse(self, book_id, chapter, verse_num, new_text):
        active_bible = self.get_active_bible_data()
        if not active_bible: return
        backup_path = active_bible['path'] + ".bak"
        if not os.path.exists(backup_path):
            try:
                import shutil
                shutil.copy2(active_bible['path'], backup_path)
                print(f"Backup created: {backup_path}")
            except Exception as e:
                print(f"Failed to create backup: {e}")
        try:
            ET.register_namespace("", "http://www.bibletechnologies.net/2003/OSIS/namespace")
            tree = ET.parse(active_bible['path'])
            root = tree.getroot()
            namespace = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
            verse_osis_id = f"{book_id}.{chapter}.{verse_num}"
            verse_node = root.find(f".//osis:verse[@osisID='{verse_osis_id}']", namespace)
            if verse_node is not None:
                verse_node.text = new_text
                tree.write(active_bible['path'], encoding='utf-8', xml_declaration=True)
                active_bible['data'][book_id]['chapters'][chapter][verse_num] = new_text
        except Exception as e:
            print(f"Auto-save error: {e}")

    def get_books(self):
        active_bible = self.get_active_bible_data()
        return active_bible['ordered_books'] if active_bible else []
    def get_book_id_by_name(self, name):
        active_bible = self.get_active_bible_data()
        if not active_bible: return None
        normalized_name = name.lower()
        for book_id, data in active_bible['data'].items():
            if data['name'].lower() == normalized_name: return book_id
        return None
    def get_chapters_for_book(self, book_name):
        active_bible = self.get_active_bible_data()
        if not active_bible: return []
        book_id = self.get_book_id_by_name(book_name)
        if book_id in active_bible['data']: return sorted(active_bible['data'][book_id]['chapters'].keys())
        return []
    def get_verses_for_chapter(self, book_name, chapter_num):
        active_bible = self.get_active_bible_data()
        if not active_bible: return []
        book_id = self.get_book_id_by_name(book_name)
        if book_id and chapter_num in active_bible['data'][book_id]['chapters']: return active_bible['data'][book_id]['chapters'][chapter_num]
        return []

    def _auto_format_verse_for_editor(self, verse_text):
        if '\n' in verse_text or not verse_text:
            return verse_text
        
        text_with_breaks = re.sub(r'([.,:;!?])\s+', r'\1\n', verse_text.strip())
        
        final_lines = []
        for line in text_with_breaks.split('\n'):
            wrapped_lines = textwrap.wrap(line, width=self.LINE_WRAP_WIDTH, break_long_words=False, break_on_hyphens=False)
            final_lines.extend(wrapped_lines)

        result = "\n".join(final_lines)

        if len(verse_text) > self.PARAGRAPH_THRESHOLD:
            result = re.sub(r'([.!?])\n', r'\1\n\n', result)
        
        return result

    def _format_verse_text(self, full_text):
        if not full_text: return []
        clean_text = full_text.strip()
        if not clean_text: return []
        blocks = clean_text.split('\n\n')
        return [block.strip() for block in blocks if block.strip()]

    def set_passage(self, book_name, chapter, verse_num):
        active_bible = self.get_active_bible_data()
        if not active_bible: return
        self.current_book_id = self.get_book_id_by_name(book_name)
        if not self.current_book_id: return
        self.current_chapter, self.current_verse_index = int(chapter), int(verse_num)
        
        verse_text_to_display = self.get_current_verse_text()
        
        formatted_text = self._auto_format_verse_for_editor(verse_text_to_display)
        if formatted_text != verse_text_to_display:
            verse_text_to_display = formatted_text
            self.save_verse(self.current_book_id, self.current_chapter, self.current_verse_index, verse_text_to_display)

        if (self.modified_next_verse_text is not None and self.next_verse_info_cache.get('book_id') == self.current_book_id and self.next_verse_info_cache.get('chapter') == self.current_chapter and self.next_verse_info_cache.get('verse_num') == self.current_verse_index):
            verse_text_to_display = self.modified_next_verse_text
            self.get_active_bible_data()['data'][self.current_book_id]['chapters'][self.current_chapter][self.current_verse_index] = verse_text_to_display
            self.save_verse(self.current_book_id, self.current_chapter, self.current_verse_index, verse_text_to_display.strip())
            self.modified_next_verse_text = None
        
        self.update_live_text(verse_text_to_display)
        self.current_block_index = 0 if self.display_blocks else -1
        update_obs_text()
        if self.navigator_window: self.navigator_window.update_display()

    def update_live_text(self, full_verse_text, from_editor=False):
        if from_editor and self.current_book_id:
            self.save_verse(self.current_book_id, self.current_chapter, self.current_verse_index, full_verse_text.strip())
        self.display_blocks = self._format_verse_text(full_verse_text)
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
        active_bible = self.get_active_bible_data()
        if not active_bible or not self.current_book_id: return
        book_name = active_bible['data'][self.current_book_id]['name']
        verses = self.get_verses_for_chapter(book_name, self.current_chapter)
        new_verse_index = self.current_verse_index + direction
        if 1 <= new_verse_index < len(verses):
            self.set_passage(book_name, self.current_chapter, new_verse_index)
            
    def reset_current_passage(self):
        self.current_book_id, self.current_chapter, self.current_verse_index = "", 0, -1
        self.display_blocks.clear(); self.current_block_index = -1
        update_obs_text()
        if self.navigator_window: self.navigator_window.update_display()

    def get_current_block_text(self):
        if 0 <= self.current_block_index < len(self.display_blocks): return self.display_blocks[self.current_block_index]
        return ""

    def get_current_reference_string(self):
        active_bible_data = self.get_active_bible_data()
        if active_bible_data and self.current_book_id and self.current_verse_index > 0:
            book_name = active_bible_data['data'][self.current_book_id]['name']
            return f"{book_name} {self.current_chapter}:{self.current_verse_index}"
        return ""

    def get_current_verse_text(self):
        active_bible = self.get_active_bible_data()
        if not active_bible or not self.current_book_id or self.current_verse_index <= 0: return ""
        try: return active_bible['data'][self.current_book_id]['chapters'][self.current_chapter][self.current_verse_index]
        except (KeyError, IndexError): return ""

    def get_next_verse_info(self):
        active_bible = self.get_active_bible_data()
        self.modified_next_verse_text = None
        if not active_bible or not self.current_book_id or self.current_verse_index <= 0:
            self.next_verse_info_cache = {}; return "...", ""
        book_name = active_bible['data'][self.current_book_id]['name']
        verses = self.get_verses_for_chapter(book_name, self.current_chapter)
        if self.current_verse_index + 1 < len(verses):
            next_verse_num = self.current_verse_index + 1
            next_verse_text = verses[next_verse_num]

            formatted_text = self._auto_format_verse_for_editor(next_verse_text)
            if formatted_text != next_verse_text:
                self.save_verse(self.current_book_id, self.current_chapter, next_verse_num, formatted_text)
                next_verse_text = formatted_text
            
            self.next_verse_info_cache = {'book_id': self.current_book_id, 'chapter': self.current_chapter, 'verse_num': next_verse_num, 'ref': f"{book_name} {self.current_chapter}:{next_verse_num}"}
            return self.next_verse_info_cache['ref'], next_verse_text
        self.next_verse_info_cache = {}; return "End of chapter", ""

    def search(self, query):
        active_bible = self.get_active_bible_data()
        if not active_bible: return []
        query = query.strip()
        ref_match = re.match(r'^((\d\s)?[a-zA-Z\s]+)\s+(\d+)(?:\s*[:\s]\s*(\d+))?$', query, re.IGNORECASE)
        if ref_match:
            book_name_query = self._normalize_text(ref_match.group(1).strip())
            chapter_query = int(ref_match.group(3))
            verse_query = int(ref_match.group(4)) if ref_match.group(4) else None
            matched_book_entries = []
            for book_entry in self.searchable_books:
                if book_entry['norm_name'].startswith(book_name_query): matched_book_entries.append(book_entry)
            if not matched_book_entries:
                all_norm_names = [b['norm_name'] for b in self.searchable_books]
                best_matches = difflib.get_close_matches(book_name_query, all_norm_names, n=5, cutoff=0.5)
                if best_matches:
                    entries_by_norm_name = {b['norm_name']: b for b in self.searchable_books}
                    for match in best_matches: matched_book_entries.append(entries_by_norm_name[match])
            if not matched_book_entries: return []
            results = []
            processed_french_books = set()
            for entry in matched_book_entries:
                if entry['french_name'] in processed_french_books: continue
                processed_french_books.add(entry['french_name'])
                book_id = self.get_book_id_by_name(entry['french_name'])
                if book_id:
                    verses = [v.copy() for v in active_bible['flat_data'] if v['book_id'] == book_id and v['chapter'] == chapter_query and (verse_query is None or v['verse'] == verse_query)]
                    for verse in verses: verse['display_book_name'] = entry['display_name']
                    results.extend(verses)
            return results
        else:
            keywords = self._normalize_text(query).split()
            if not keywords: return []
            results = []
            for v in active_bible['flat_data']:
                   if all(kw in v['norm_text'] for kw in keywords):
                        res = v.copy()
                        res['display_book_name'] = res['book_name']
                        results.append(res)
            return results

# --- Global and OBS Functions ---
def update_obs_text():
    """ MODIFIED: Sends text to two separate sources. """
    global bible_manager
    if not bible_manager: return

    # --- Update Main Text Source (Verse) ---
    block_text = bible_manager.get_current_block_text()
    main_source_name = bible_manager.text_source_name
    if main_source_name:
        source = obs.obs_get_source_by_name(main_source_name)
        if source:
            settings = obs.obs_data_create()
            obs.obs_data_set_string(settings, "text", block_text)
            obs.obs_source_update(source, settings)
            obs.obs_source_release(source)
            obs.obs_data_release(settings)

    # --- Update Reference Text Source ---
    ref_text = bible_manager.get_current_reference_string()
    ref_source_name = bible_manager.reference_source_name
    if ref_source_name:
        source = obs.obs_get_source_by_name(ref_source_name)
        if source:
            settings = obs.obs_data_create()
            obs.obs_data_set_string(settings, "text", ref_text)
            obs.obs_source_update(source, settings)
            obs.obs_source_release(source)
            obs.obs_data_release(settings)

def on_hotkey_pressed(hotkey_id, pressed):
    if not pressed or not bible_manager: return
    if hotkey_id == "bible_next": bible_manager.navigate_block(1)
    elif hotkey_id == "bible_prev": bible_manager.navigate_block(-1)
    elif hotkey_id == "bible_next_verse": bible_manager.navigate_verse(1)
    elif hotkey_id == "bible_prev_verse": bible_manager.navigate_verse(-1)

def setup_hotkeys():
    obs.obs_hotkey_register_frontend("bible_next", "Bible: Next Block", lambda p: on_hotkey_pressed("bible_next", p))
    obs.obs_hotkey_register_frontend("bible_prev", "Bible: Previous Block", lambda p: on_hotkey_pressed("bible_prev", p))
    obs.obs_hotkey_register_frontend("bible_next_verse", "Bible: Next Verse", lambda p: on_hotkey_pressed("bible_next_verse", p))
    obs.obs_hotkey_register_frontend("bible_prev_verse", "Bible: Previous Verse", lambda p: on_hotkey_pressed("bible_prev_verse", p))

def open_navigator_callback(props, prop):
    global bible_manager
    if not bible_manager: return
    if not bible_manager.navigator_window or not bible_manager.navigator_window.winfo_exists():
        bible_manager.navigator_window = BibleNavigator(bible_manager)
        bible_manager.navigator_window.protocol("WM_DELETE_WINDOW", bible_manager.navigator_window.on_closing)
        bible_manager.navigator_window.mainloop()
    else: bible_manager.navigator_window.lift()

def script_description():
    """ MODIFIED: English and more concise. """
    return """
    <h2>OBS Bible Presenter 2.2</h2>
    <p>A tool to manage and display Bible verses live in OBS Studio.</p>
    <ul>
        <li>Sends the <b>verse reference and text</b> to two separate sources.</li>
        <li>Easy navigation by book, chapter, and verse.</li>
        <li>Quick search by reference or keyword.</li>
        <li>Manage favorites and search history.</li>
    </ul>
    <p>Download compatible Bibles (OSIS XML format) here:<br>
    <a href="https://github.com/montrealmepc-netizen/Compatible-bibles">Link to Compatible Bibles</a></p>
    """

def _populate_source_list(prop_list):
    """ Helper function to populate a list property with text sources. """
    sources = obs.obs_enum_sources()
    if sources:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id in ["text_gdiplus_v2", "text_ft2_source_v2", "text_gdiplus", "text_ft2_source"]:
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(prop_list, name, name)
        obs.source_list_release(sources)

def script_properties():
    """ MODIFIED: Added a second source list for the reference. """
    props = obs.obs_properties_create()
    obs.obs_properties_add_path(props, "bible_folder", "Bible Folder (.xml)", obs.OBS_PATH_DIRECTORY, "", None)
    
    # Main source for the verse text
    main_source_list = obs.obs_properties_add_list(props, "text_source", "Main Text Source (Verse)", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    _populate_source_list(main_source_list)

    # Optional source for the reference
    ref_source_list = obs.obs_properties_add_list(props, "reference_source", "Reference Text Source (Optional)", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_list_add_string(ref_source_list, "", "(None)") # Add a "None" option
    _populate_source_list(ref_source_list)

    obs.obs_properties_add_button(props, "navigator_button", "Open Navigator", open_navigator_callback)
    return props

def script_load(settings):
    """ MODIFIED: Load the reference source name. """
    global bible_manager
    bible_manager = BibleManager()
    bible_manager.text_source_name = obs.obs_data_get_string(settings, "text_source")
    bible_manager.reference_source_name = obs.obs_data_get_string(settings, "reference_source")
    
    folder_path = obs.obs_data_get_string(settings, "bible_folder")
    if not folder_path and bible_manager.bible_folder_path:
        folder_path = bible_manager.bible_folder_path
        obs.obs_data_set_string(settings, "bible_folder", folder_path)
    
    bible_manager.load_bibles_from_folder(folder_path)
    bible_manager.start_folder_watcher()
    setup_hotkeys()

def script_update(settings):
    """ MODIFIED: Update both source names. """
    global bible_manager
    if not bible_manager: return
    bible_manager.text_source_name = obs.obs_data_get_string(settings, "text_source")
    bible_manager.reference_source_name = obs.obs_data_get_string(settings, "reference_source")

    new_folder_path = obs.obs_data_get_string(settings, "bible_folder")
    if new_folder_path != bible_manager.bible_folder_path:
        bible_manager.load_bibles_from_folder(new_folder_path)
        bible_manager._save_settings()
    update_obs_text()

def script_unload():
    if bible_manager:
        bible_manager.stop_folder_watcher()
        if bible_manager.navigator_window:
            bible_manager.navigator_window.destroy()

# ----------------------------------------------------------------------
# --- Tkinter UI Class ---
# ----------------------------------------------------------------------
class BibleNavigator(ThemedTk):
    def __init__(self, manager):
        super().__init__(theme="arc")
        self.manager = manager
        self.title("OBS Bible Presenter 2.2") # MODIFIED: English Title
        self.geometry("850x700")
        self.font_main = font.Font(family="Segoe UI", size=10)
        self.editor_save_timer = None
        self.create_widgets()
        self.update_all_ui()
    
    # ... (The rest of the BibleNavigator class is identical to the previous version) ...
    def on_closing(self): self.manager.navigator_window = None; self.destroy()
    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.ref_font = font.Font(family="Segoe UI", size=14, weight="bold")
        self.current_ref_label = ttk.Label(main_frame, text="No passage selected", 
                                           font=self.ref_font, anchor="center")
        self.current_ref_label.pack(fill=tk.X, pady=(5, 10))

        self.notebook = ttk.Notebook(main_frame); self.notebook.pack(fill=tk.BOTH, expand=True)
        self.nav_frame = ttk.Frame(self.notebook, padding="10"); search_frame = ttk.Frame(self.notebook, padding="10"); favorites_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.nav_frame, text='Navigation'); self.notebook.add(search_frame, text='Search'); self.notebook.add(favorites_frame, text='⭐ Favorites')
        top_frame = ttk.Frame(self.nav_frame); top_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(top_frame, text="Version:").pack(side=tk.LEFT, padx=(0,5)); self.bible_var = tk.StringVar(); self.bible_combo = ttk.Combobox(top_frame, textvariable=self.bible_var, state="readonly", font=self.font_main, width=15); self.bible_combo.pack(side=tk.LEFT, padx=(0,10)); self.bible_combo.bind("<<ComboboxSelected>>", self.on_bible_selected)
        selection_frame = ttk.Frame(self.nav_frame); selection_frame.pack(fill=tk.X, pady=(0, 10)); selection_frame.columnconfigure(1, weight=1); selection_frame.columnconfigure(3, weight=1); selection_frame.columnconfigure(5, weight=1)
        ttk.Label(selection_frame, text="Book:").grid(row=0, column=0); self.book_var = tk.StringVar(); self.book_combo = ttk.Combobox(selection_frame, textvariable=self.book_var, state="readonly", font=self.font_main); self.book_combo.grid(row=0, column=1, sticky="ew", padx=5); self.book_combo.bind("<<ComboboxSelected>>", self.on_book_selected)
        ttk.Label(selection_frame, text="Chapter:").grid(row=0, column=2); self.chapter_var = tk.StringVar(); self.chapter_combo = ttk.Combobox(selection_frame, textvariable=self.chapter_var, state="readonly", width=5, font=self.font_main); self.chapter_combo.grid(row=0, column=3, sticky="ew", padx=5); self.chapter_combo.bind("<<ComboboxSelected>>", self.on_chapter_selected)
        ttk.Label(selection_frame, text="Verse:").grid(row=0, column=4); self.verse_var = tk.StringVar(); self.verse_combo = ttk.Combobox(selection_frame, textvariable=self.verse_var, state="readonly", width=5, font=self.font_main); self.verse_combo.grid(row=0, column=5, sticky="ew", padx=5); self.verse_combo.bind("<<ComboboxSelected>>", self.on_verse_selected)
        editor_frame = ttk.LabelFrame(self.nav_frame, text="Live Verse Editor (auto-saves)"); editor_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.editor_text = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD, height=5, font=self.font_main); self.editor_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5); self.editor_text.bind("<KeyRelease>", self.on_editor_key_release)
        control_frame = ttk.Frame(self.nav_frame); control_frame.pack(fill=tk.X, pady=(5,0)); ttk.Button(control_frame, text="⭐ Add to Favorites", command=self.manager.add_favorite).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2); ttk.Button(control_frame, text="<< Previous", command=lambda: self.manager.navigate_block(-1)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2); ttk.Button(control_frame, text="Next >>", command=lambda: self.manager.navigate_block(1)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2); ttk.Button(control_frame, text="Clear", command=self.manager.reset_current_passage).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        preview_frame = ttk.LabelFrame(self.nav_frame, text="Next Verse Editor (applies on selection)"); preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.preview_ref_label = ttk.Label(preview_frame, text="..."); self.preview_ref_label.pack(fill=tk.X, padx=5, pady=(5,0)); self.preview_text = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, height=3, font=self.font_main); self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5); self.preview_text.bind("<KeyRelease>", self.on_preview_key_release)
        self.status_label = ttk.Label(self.nav_frame, text="No passage selected.", anchor="center"); self.status_label.pack(fill=tk.X, pady=(10, 0))
        search_bar_frame = ttk.Frame(search_frame); search_bar_frame.pack(fill=tk.X); self.search_var = tk.StringVar(); self.search_combo = ttk.Combobox(search_bar_frame, textvariable=self.search_var, font=self.font_main); self.search_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5)); self.search_combo.bind("<Return>", self.perform_search); self.search_combo.bind("<<ComboboxSelected>>", self.perform_search); ttk.Button(search_bar_frame, text="Search", command=self.perform_search).pack(side=tk.LEFT)
        results_frame = ttk.LabelFrame(search_frame, text="Results"); results_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0)); self.results_listbox = tk.Listbox(results_frame, font=self.font_main); self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); self.results_listbox.bind("<Double-1>", self.on_result_selected); scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_listbox.yview); scrollbar.pack(side=tk.RIGHT, fill="y"); self.results_listbox.config(yscrollcommand=scrollbar.set); self.search_results_data = []
        fav_list_frame = ttk.LabelFrame(favorites_frame, text="Favorite Verses"); fav_list_frame.pack(fill=tk.BOTH, expand=True); self.favorites_listbox = tk.Listbox(fav_list_frame, font=self.font_main); self.favorites_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); self.favorites_listbox.bind("<Double-1>", self.on_favorite_selected); fav_scrollbar = ttk.Scrollbar(fav_list_frame, orient="vertical", command=self.favorites_listbox.yview); fav_scrollbar.pack(side=tk.RIGHT, fill="y"); self.favorites_listbox.config(yscrollcommand=fav_scrollbar.set)
        ttk.Button(favorites_frame, text="Remove Selected Favorite", command=self.remove_selected_favorite).pack(fill=tk.X, pady=(5,0))
    def on_editor_key_release(self, event=None):
        if self.editor_save_timer: self.after_cancel(self.editor_save_timer)
        self.editor_save_timer = self.after(1500, self._save_editor_content)
    def _save_editor_content(self):
        self.editor_save_timer = None
        self.manager.update_live_text(self.editor_text.get("1.0", tk.END), from_editor=True)
    def on_preview_key_release(self, event=None): self.manager.modified_next_verse_text = self.preview_text.get("1.0", tk.END)
    def perform_search(self, event=None):
        query = self.search_var.get();
        if not query: return
        self.manager.add_to_search_history(query); self.update_search_history()
        results = self.manager.search(query)
        self.results_listbox.delete(0, tk.END); self.search_results_data = results
        for item in results: self.results_listbox.insert(tk.END, f"{item['display_book_name']} {item['chapter']}:{item['verse']}")
    def on_result_selected(self, event=None):
        if not self.results_listbox.curselection(): return
        selected_data = self.search_results_data[self.results_listbox.curselection()[0]]
        self.manager.set_passage(selected_data['book_name'], selected_data['chapter'], selected_data['verse']); self.notebook.select(self.nav_frame)
    def on_favorite_selected(self, event=None):
        if not self.favorites_listbox.curselection(): return
        selected_fav = self.manager.favorites[self.favorites_listbox.curselection()[0]]
        self.manager.set_active_bible(selected_fav['bible_name'])
        self.manager.set_passage(selected_fav['book_name'], selected_fav['chapter'], selected_fav['verse']); self.notebook.select(self.nav_frame)
    def remove_selected_favorite(self):
        if not self.favorites_listbox.curselection(): return
        self.manager.remove_favorite(self.manager.favorites[self.favorites_listbox.curselection()[0]])
    def on_bible_selected(self, event=None): self.manager.set_active_bible(self.bible_var.get())
    def on_book_selected(self, event=None):
        chapters = self.manager.get_chapters_for_book(self.book_var.get())
        self.chapter_combo['values'] = chapters
        if chapters: self.chapter_combo.set(chapters[0]); self.on_chapter_selected()
    def on_chapter_selected(self, event=None):
        try:
            verses = self.manager.get_verses_for_chapter(self.book_var.get(), int(self.chapter_var.get())); self.verse_combo['values'] = list(range(1, len(verses)))
            if verses: self.verse_combo.set(1); self.on_verse_selected()
        except (ValueError, IndexError): pass
    def on_verse_selected(self, event=None):
        try: self.manager.set_passage(self.book_var.get(), int(self.chapter_var.get()), int(self.verse_var.get()))
        except (ValueError, TypeError): pass
    def update_all_ui(self): self.update_bible_versions_list(); self.update_book_list(); self.update_display(); self.update_favorites_list(); self.update_search_history()
    def update_bible_versions_list(self):
        versions = list(self.manager.bibles.keys())
        self.bible_combo['values'] = versions
        if self.manager.active_bible_name: self.bible_var.set(self.manager.active_bible_name)
        elif versions: self.bible_var.set(versions[0])
    def update_book_list(self):
        books = self.manager.get_books()
        self.book_combo['values'] = books
        if books: self.book_combo.set(books[0]); self.on_book_selected()
        else: self.book_combo.set(''); self.chapter_combo.set(''); self.verse_combo.set('')
    def update_display(self):
        self.editor_text.delete("1.0", tk.END); self.editor_text.insert("1.0", self.manager.get_current_verse_text())
        
        ref_text = self.manager.get_current_reference_string()
        self.current_ref_label.config(text=ref_text if ref_text else "No passage selected")
        
        active_bible_data = self.manager.get_active_bible_data()
        if active_bible_data and self.manager.current_book_id:
            self.book_var.set(active_bible_data['data'][self.manager.current_book_id]['name'])
            self.chapter_var.set(self.manager.current_chapter)
            self.verse_var.set(self.manager.current_verse_index)

        self.update_status_label()
        ref, text = self.manager.get_next_verse_info()
        self.preview_ref_label.config(text=ref); self.preview_text.delete("1.0", tk.END); self.preview_text.insert("1.0", text)
    def update_status_label(self):
        active_bible_data = self.manager.get_active_bible_data()
        if active_bible_data and self.manager.current_book_id and self.manager.current_verse_index > 0:
            book_name = active_bible_data['data'][self.manager.current_book_id]['name']
            self.status_label.config(text=f"Live: [{self.manager.active_bible_name}] {book_name} {self.manager.current_chapter}:{self.manager.current_verse_index} (Page {self.manager.current_block_index + 1}/{len(self.manager.display_blocks)})")
        else: self.status_label.config(text="No passage selected.")
    def update_favorites_list(self):
        self.favorites_listbox.delete(0, tk.END)
        for fav in self.manager.favorites: self.favorites_listbox.insert(tk.END, f"[{fav['bible_name']}] {fav['ref_str']}")
    def update_search_history(self): self.search_combo['values'] = self.manager.search_history