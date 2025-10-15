# Bible Mepc montreal V1.0 - OBS Studio Script

A powerful Python script for OBS Studio designed to display and manage Bible verses for live church services, streams, or recordings. This tool provides a comprehensive control panel to navigate, display, and even live-edit scripture directly within OBS.

This script was inspired by and developed for the production team at [MEPC Montreal](https://www.mepcmontreal.ca).

![Script Navigator Screenshot](https://i.imgur.com/your-image-link-here.png)  ---

## ✨ Key Features

* **📖 Full Bible Navigation:** Quickly load an entire Bible from a single OSIS-formatted XML file. Easily navigate to any book, chapter, and verse through a user-friendly control panel.
* **✍️ Live Text Editing:** Any corrections or modifications made to the **currently displayed verse** are instantly reflected in the OBS GDI+ text source, perfect for on-the-fly typo fixes.
* **👀 Next Verse Preview & Preparation:** See and edit the upcoming verse in a separate editor. Your edits are automatically applied when you navigate to that verse, allowing for seamless transitions.
* **📄 Block Display:** Long verses are automatically broken down into readable "pages" or "blocks" (default is 5 lines) to avoid overwhelming the screen.
* **🖱️ Intuitive Controls:** Navigate between pages and verses with "Next" and "Previous" buttons or configurable hotkeys.
* **💾 Save Changes:** Permanently save your live edits back to the XML file, ensuring your corrections are kept for future use.

## ✅ Prerequisites

1.  **OBS Studio:** Version 27 or newer is recommended.
2.  **Python 3:** A working Python installation configured for OBS Studio scripts.
3.  **GDI+ Text Source:** You must have a "Text (GDI+)" source created in your OBS scene. This is the source the script will control.

## ⚙️ Installation & Setup

1.  **Download the Bible XML File:**
    * This script requires a Bible in the **OSIS XML format**.
    * You can download the recommended **Louis Segond 1910 (French)** version from this repository:
    * **[Download `fren.xml` Here](https://github.com/montrealmepc-netizen/biblefr)**

2.  **Install the Script in OBS:**
    * In OBS Studio, go to **Tools > Scripts**.
    * Click the **"+"** button in the bottom left corner and select the `bible_mepc_montreal_v1.py` file.

3.  **Configure the Script:**
    * With the script selected, you will see its properties on the right.
    * **Bible File (.xml):** Click "Browse" and select the `fren.xml` file you downloaded.
    * **Text Source (GDI+):** Select the GDI+ text source you created in your scene from the dropdown menu.

![Script Settings Screenshot](https://i.imgur.com/your-settings-screenshot.png) ## 🕹️ How to Use

1.  **Open the Navigator:**
    * In the Scripts window, click the **"Open Navigator"** button.

2.  **Navigate Scripture:**
    * Use the **Book**, **Chapter**, and **Verse** dropdown menus to select a passage. The text will immediately appear in your OBS text source.

3.  **Control Display:**
    * Use the **`<< Previous`** and **`Next >>`** buttons below the main editor to navigate between pages of a long verse, or to move to the previous/next verse.
    * The **`Clear Display`** button will empty the text source.

4.  **Live Editing:**
    * **Current Verse:** Simply type in the top editor box. The text in OBS will update as you type. Click **`Save Current Verse`** to make the change permanent in your XML file.
    * **Next Verse:** Type in the bottom editor box to prepare the upcoming verse. Your changes will be applied automatically when you navigate to it. Click **`Save Next Verse`** to save these changes to the XML file ahead of time.

## ⌨️ Hotkeys

You can set custom hotkeys for faster navigation:
* Go to **File > Settings > Hotkeys**.
* Search for "Bible" to find the "Next" and "Previous" actions and assign your preferred keys.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
