
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
import threading
import re

class YTDApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Desktop YouTube Downloader")
        self.geometry("600x450")
        self.resizable(False, False)
        
        # Variables
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="mp4")
        self.quality_var = tk.StringVar(value="best")
        self.playlist_var = tk.BooleanVar(value=False)
        self.save_path = tk.StringVar(value=os.path.expanduser("~\\Downloads")) # Default to Downloads
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- URL Input ---
        url_frame = ttk.LabelFrame(main_frame, text="Video / Playlist URL", padding="10")
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Entry(url_frame, textvariable=self.url_var, width=70).pack(fill=tk.X)
        
        # --- Options Frame ---
        opts_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        opts_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Row 1: Format (MP4/MP3)
        ttk.Label(opts_frame, text="Format:").grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Radiobutton(opts_frame, text="MP4 (Video)", variable=self.format_var, value="mp4").grid(row=0, column=1, padx=5)
        ttk.Radiobutton(opts_frame, text="MP3 (Audio)", variable=self.format_var, value="mp3").grid(row=0, column=2, padx=5)
        
        # Row 2: Quality
        ttk.Label(opts_frame, text="Quality:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        quality_options = ["best", "1080", "720", "480", "360"]
        ttk.Combobox(opts_frame, values=quality_options, textvariable=self.quality_var, width=10, state="readonly").grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Row 3: Playlist Checkbox
        ttk.Checkbutton(opts_frame, text="Download Whole Playlist", variable=self.playlist_var).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # --- Location ---
        loc_frame = ttk.LabelFrame(main_frame, text="Save Location", padding="10")
        loc_frame.pack(fill=tk.X, pady=(0, 10))
        
        path_entry = ttk.Entry(loc_frame, textvariable=self.save_path, width=50)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(loc_frame, text="Browse", command=self.browse_location).pack(side=tk.RIGHT)
        
        # --- Progress Bar ---
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.status_label = ttk.Label(progress_frame, text="Ready", font=("Helvetica", 9))
        self.status_label.pack(anchor=tk.W)
        
        # --- Download Button ---
        download_btn = ttk.Button(main_frame, text="Download", command=self.start_download_thread)
        download_btn.pack(fill=tk.X, ipady=5)
        
    def browse_location(self):
        folder = filedialog.askdirectory(initialdir=self.save_path.get())
        if folder:
            self.save_path.set(folder)
            
    def start_download_thread(self):
        # Start download in a separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.download_video)
        thread.start()
        
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            # Calculate percentage
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            
            if total_bytes:
                percent = (downloaded_bytes / total_bytes) * 100
                self.progress_bar['value'] = percent
                
            # Update status text
            speed = d.get('speed')
            if speed:
                speed_str = f"{speed/1024:.1f} KB/s"
            else:
                speed_str = "Calculating..."
                
            self.status_label.config(text=f"Downloading... {self.progress_bar['value']:.1f}% - Speed: {speed_str}")
            
        elif d['status'] == 'finished':
            self.progress_bar['value'] = 100
            self.status_label.config(text="Processing file (merging/converting)...")
            self.update_idletasks()

    def download_video(self):
        url = self.url_var.get()
        save_loc = self.save_path.get()
        
        if not url:
            messagebox.showwarning("Input Error", "Please enter a URL.")
            return
        
        # Configure yt-dlp options
        ydl_opts = {
            'progress_hooks': [self.progress_hook],
            'outtmpl': os.path.join(save_loc, '%(title)s.%(ext)s'),
            'noplaylist': not self.playlist_var.get(), # True if checkbox is unchecked
        }
        
        # Handle Format and Quality
        selected_format = self.format_var.get()
        selected_quality = self.quality_var.get()
        
        if selected_format == 'mp3':
            # Extract audio, convert to mp3
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else: 
            # MP4 Video logic
            # If user selects specific res, try to get that res + best audio
            # 'best' automatically selects best available
            if selected_quality == 'best':
                fmt_string = 'bestvideo+bestaudio/best'
            else:
                # Example: bestvideo[height<=720]+bestaudio
                fmt_string = f'bestvideo[height<={selected_quality}]+bestaudio/best[height<={selected_quality}]'
            
            ydl_opts.update({
                'format': fmt_string,
                'merge_output_format': 'mp4', # Ensure final file is mp4
            })
            
        try:
            self.status_label.config(text="Fetching metadata...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.status_label.config(text="Download Complete!")
            messagebox.showinfo("Success", "Download finished successfully!")
            self.progress_bar['value'] = 0
            
        except Exception as e:
            self.status_label.config(text="Error occurred.")
            messagebox.showerror("Download Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    app = YTDApp()
    app.mainloop()