# Dual-Movie
Simple Python script that plays 2 videos and let's you swiftly switch between them with keyboard.
Example use: 
Watching a movie in two languages, phrase by phrase.

## Features
- Select any two video files from your current directory
- Switch between them instantly with `Tab`
- Pause/play with `Space`
- Rewind/forward 5 seconds with `w` & `e`

On some systems, the keyboard module may require administrative rights.
VLC must be installed and available via your system path.
Playback speed adjustments are synced across both videos.
Audio-only files will play without opening a video window.

### Video:
`.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, `.webm`, `.wmv`, `.mpeg`, `.mpg`, `.m4v`, `.3gp`

### Audio:
`.mp3`, `.wav`, `.ogg`, `.aac`, `.flac`, `.m4a`, `.wma`

## Requirements
- Python 3.7+
- VLC media player installed (required by `python-vlc`)

## Installation

### Step 1: Clone the repository OR download the Release.
```bash
pip install -r requirements.txt
```
### Step 2:
Run dual-movie.exe

### OR
If you wish to compile from source:

### Step 1:
```bash
pip install -r requirements.txt
```
### Step 2:
```bash
pip install pyinstaller
```

### Step 3:
```bash
pyinstaller --onefile dual-movie.py
```

### Step 4:
The exe file will be in the dist/ folder. 
Video files must be in the same folder as .exe!

