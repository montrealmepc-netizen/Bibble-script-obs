# OBS Bible Presenter 2.0

A powerful Python script for OBS Studio designed to display Bible verses and their references seamlessly during live streams or recordings. This tool sends the verse text and the reference to two separate OBS text sources, allowing for independent styling and layout. It features a modern user interface, robust search capabilities, favorites, history, and hotkey support for efficient operation.

Inspired by and developed for MEPC Montreal.

## ✨ Features

* **Dual Source Output**: Sends the verse text and its reference (e.g., "John 3:16") to two different text sources in OBS for maximum layout flexibility.
* **Modern UI**: An intuitive navigator window built with Tkinter and ttkthemes for easy management.
* **Advanced Search**: Quickly find passages by reference (e.g., "1 Cor 13:4") or by keyword search within the text.
* **Favorites & History**: Save frequently used verses to your favorites and access your recent searches instantly.
* **Hotkey Support**: Navigate between verses and text blocks directly from OBS using configurable hotkeys.
* **Live Verse Editor**: Correct typos or reformat verses on the fly. Changes are saved automatically to the source XML file.
* **Multi-Bible Support**: Load multiple Bible versions (in OSIS XML format) and switch between them easily.

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed:

1.  **[OBS Studio](https://obsproject.com/)**: The latest version is recommended.
2.  **[Python](https://www.python.org/downloads/)**: The script requires a specific version of Python that matches your OBS installation.
    * To find the required version, open OBS and go to **Tools -> Scripts -> Python Settings**. It will specify the exact version you need to download.
    * **Crucial for Windows users**: During Python installation, make sure to check the box that says **"Add Python to PATH"**.
3.  **`ttkthemes` Library**: A Python package for styling the user interface.
4.  **Bible Files**: The script requires Bible texts in the **OSIS XML** format.

## 🚀 Installation & Configuration

Follow these steps to get the script running in OBS.

### Step 1: Install Python Dependencies

Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux) and run the following command to install the required library:

```bash
pip install ttkthemes
```

### Step 2: Prepare Bible Files

1.  Download compatible Bible versions from the [Compatible Bibles Repository](https://github.com/montrealmepc-netizen/Compatible-bibles).
2.  Create a folder on your computer (e.g., `C:\Bibles` or `Documents/Bibles`).
3.  Extract and place all the `.xml` Bible files directly into this folder.

### Step 3: Configure OBS Studio

1.  **Save the Script**: Save the script code as a Python file (e.g., `bible_presenter.py`).
2.  **Create Text Sources**: In your desired OBS scene, add two **Text (GDI+)** sources:
    * One for the verse text (e.g., name it `Verse Text`).
    * One for the reference (e.g., name it `Verse Reference`).
3.  **Load the Script**:
    * In OBS, go to **Tools -> Scripts**.
    * Click the `+` button and add the `bible_presenter.py` file.
4.  **Set Script Properties**:
    * With the script selected, configure the options on the right:
    * **Bible Folder**: Click `Browse` and select the folder where you saved your `.xml` Bible files.
    * **Main Text Source (Verse)**: Select your `Verse Text` source from the dropdown menu.
    * **Reference Text Source (Optional)**: Select your `Verse Reference` source.
5.  **Launch the Navigator**: Click the **"Open Navigator"** button in the script properties to launch the control window.

## 📖 Usage

The **Navigator Window** is your main control center.

* **Navigation Tab**: Select the Bible version, book, chapter, and verse using the dropdown menus.
* **Search Tab**: Type a reference or keyword to find verses. Double-click a result to display it.
* **Favorites Tab**: Access your saved verses. Double-click to display one.
* **Live Verse Editor**: The currently displayed verse appears here. You can edit it, and the changes will reflect in OBS and be saved to the XML file after a brief delay.
* **Navigation Buttons**: Use the `<< Previous`, `Next >>`, and `Clear` buttons to control the output.

### Hotkeys

You can set the following hotkeys in **OBS -> Settings -> Hotkeys**:

* `Bible: Next Block`: Displays the next paragraph/block of the current verse.
* `Bible: Previous Block`: Displays the previous paragraph/block.
* `Bible: Next Verse`: Jumps to the next verse.
* `Bible: Previous Verse`: Jumps to the previous verse.
