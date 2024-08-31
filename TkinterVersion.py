import tkinter as tk
from tkinter import ttk, messagebox
from yt_dlp import YoutubeDL
import os

# Function to download video and show progress
def download_video(url, download_path):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Progress hook function for yt-dlp
def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes')
        downloaded_bytes = d.get('downloaded_bytes')
        if total_bytes and downloaded_bytes:
            progress = downloaded_bytes / total_bytes
            percent = progress * 100
            progress_var.set(percent)
            progress_label.config(text=f"{percent:.2f}%")

    elif d['status'] == 'finished':
        progress_var.set(100)
        progress_label.config(text="Download completed!")
        messagebox.showinfo("Download Complete", f"Download completed: {d['filename']}")

# Function to start download when button is clicked
def start_download():
    url = url_entry.get()
    if url:
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        download_video(url, download_path)
    else:
        messagebox.showwarning("Input Error", "Please enter a valid URL.")

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# URL input field
tk.Label(root, text="Enter YouTube video URL:").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Download button
download_button = tk.Button(root, text="Download", command=start_download)
download_button.pack(pady=10)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill=tk.X, padx=20)

# Progress percentage label
progress_label = tk.Label(root, text="0%")
progress_label.pack(pady=5)

# Start the Tkinter main loop
root.mainloop()
