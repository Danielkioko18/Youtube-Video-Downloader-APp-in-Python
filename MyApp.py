import streamlit as st
from yt_dlp import YoutubeDL
import os
from tqdm import tqdm
import time

# Function to download video and show progress
def download_video(url, download_path):
    try:
        # Setting up yt-dlp options
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Progress hook function for yt-dlp
def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes')
        downloaded_bytes = d.get('downloaded_bytes')
        if total_bytes and downloaded_bytes:
            progress = downloaded_bytes / total_bytes
            progress_bar.progress(progress)
            status_text.text(f"Downloading: {d['filename']} ({d['_percent_str']} complete)")

    elif d['status'] == 'finished':
        progress_bar.progress(1.0)
        status_text.text(f"Download completed: {d['filename']}")

# Streamlit app interface
st.title("YouTube Video Downloader")

# Input field for YouTube URL
url = st.text_input("Enter YouTube video URL:")

# Button to trigger download
if st.button("Download"):
    if url:
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        progress_bar = st.progress(0)
        status_text = st.empty()
        download_video(url, download_path)
    else:
        st.error("Please enter a valid URL.")
