

# 🎬 Video Downloader App

A modern, user-friendly Desktop Application to download videos and audio from YouTube. This tool provides a Graphical User Interface (GUI) to easily download single videos, entire playlists, and convert them to MP3 or MP4 format.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

---

## ✨ Features

-   **GUI Interface**: Clean design built with Tkinter.
-   **Format Selection**: Download as **MP4** (Video) or **MP3** (Audio).
-   **Quality Control**: Choose resolution (360p, 480p, 720p, 1080p, or Best).
-   **Playlist Support**: Download a single video or an entire playlist with one click.
-   **Custom Save Location**: Browse and select where files are stored.
-   **Progress Tracking**: Real-time progress bar and download speed indicator.
-   **Standalone EXE**: Can be run as an executable without installing Python.

---

## 📥 How to Download and Use

You can use this application in two ways:

### Option 1: Run the Executable (Recommended for most users)

1.  Go to the **[Releases](https://github.com/MahmoudAshrafYadem/Video_Dowinloader_App/releases)** section of this repository.
2.  Download the latest `YouTubeDownloader.exe`.
3.  Double-click the file to run it. No installation is needed!

### Option 2: Run from Source Code

**Prerequisites:**
*   Python 3.8 or higher installed.
*   FFmpeg (optional, but recommended for high-quality 1080p/4K downloads).

**Steps:**

1.  **Clone the repository**
    ```bash
    git clone https://github.com/MahmoudAshrafYadem/Video_Dowinloader_App.git
    ```

2.  **Navigate to the folder**
    ```bash
    cd Video_Dowinloader_App
    ```

3.  **Install dependencies**
    ```bash
    pip install yt-dlp
    ```

4.  **Run the app**
    ```bash
    python app.py
    ```

---

## 🛠️ How to Build the EXE (For Developers)

If you want to modify the code and build your own `.exe` file:

1.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2.  Run the build command:
    ```bash
    pyinstaller --onefile --noconsole --name "YouTubeDownloader" app.py
    ```

3.  Your new executable will be inside the `dist/` folder.

---

## ⚠️ Important Note on High Quality (1080p/4K)

To download videos in 1080p or higher, YouTube separates video and audio tracks. This app merges them automatically if **FFmpeg** is installed on your computer.

*   **Without FFmpeg**: The app may fallback to lower qualities (like 720p) or download video-only files for high resolutions.
*   **With FFmpeg**: Works perfectly for all resolutions and formats.

---

## 📜 Disclaimer

This software is provided for educational and personal use only. Please respect the Terms of Service of YouTube and copyright laws. The author is not responsible for any misuse of this application.


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

