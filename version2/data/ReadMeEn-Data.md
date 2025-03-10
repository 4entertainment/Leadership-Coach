# 📌 README - Data Documentation 

## 📌 requirements.txt (English)  

The `requirements.txt` file documents all dependencies used during the project's development. It is generated using:  

```bash
pip freeze > requirements.txt
```

This ensures that all required libraries are recorded for easy replication.  

### ⚙️ **Setting Up the Environment**  

1. **Create a new Conda environment:**  
   ```bash
   conda create --name env_name python==3.10.16
   ```
   (Replace `env_name` with the desired environment name.)  

2. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```

This process ensures that all necessary packages are installed, replicating the development environment precisely.


## 📌 download_video_audio.py (English)  

This Python script is designed to download video and/or audio files from a given YouTube playlist. The user can choose to download videos in mp4 format, audio in mp3 format, or both. The script leverages the **yt-dlp** library for downloading.  

---

### 🛠 **Features**  
✔ Fetches and downloads content from a YouTube playlist URL.  
✔ Allows the user to choose between video, audio, or both modes.  
✔ Saves downloaded files in their respective formats.  
✔ Organizes files within designated directories.  

### ⚙ **Usage**  

1. **Run the script:**  
   ```bash
   python download_video_audio.py
   ```

2. **Choose a download mode:**  
   - `video` → Downloads video only (mp4 format).  
   - `audio` → Downloads audio only (mp3 format).  
   - `both` → Downloads both video and audio.  


## 📌 audio/ Directory (English)  

This directory contains **MP3 files** extracted from a selected YouTube playlist. The audio files are downloaded using the `download_video_audio.py` script and stored in this folder.  

---

### 📂 **Contents**  
✔ Audio files (MP3 format) extracted from the selected YouTube playlist.  
✔ File names are generated based on the original YouTube video titles.  
✔ Each file is stored in the highest available audio quality.  

## 📌 video/ Directory (English)  

This directory contains **MP4 video files** downloaded from a YouTube playlist. The file names are generated based on the original YouTube video titles. **Due to large file sizes, this directory has not been uploaded to GitHub.**  

---

### 📂 **Contents**  
✔ Downloaded YouTube playlist videos in **MP4 format**.  
✔ File names are based on the original YouTube video titles.  
✔ **Not included in the GitHub repository due to storage and size limitations.**  
✔ **Further data processing continues with audio-to-text conversion. The audio folder is used instead of the video folder.**  

**Note:** Use the `download_video_audio.py` script to download the videos.


## 📌 rename_or_revert_video_audio.py (English)  

This Python script automates the **renaming and reverting of video (MP4) and/or audio (MP3) files**. The user can specify the target file type and choose between renaming or reverting operations.  

---

### 🛠 **Features**  
✔ Cleans and renames file names based on user selection.  
✔ **Optionally converts Turkish characters to English equivalents**.  
✔ **Stores file name changes in a JSON file** for easy reversion.  
✔ Allows users to operate on **video (MP4), audio (MP3), or both**.  
✔ **Removes unwanted characters from file names**, ensuring a cleaner format.  
✔ Provides a **revert function to restore original file names**.  

### ⚙ **Usage**  

1. **Run the script:**  
   ```bash
   python rename_or_revert_video_audio.py
   ```

2. **Select operation type:**  
   - `1` → **Rename files with cleaned names**  
   - `2` → **Revert files back to their original names**  

3. **Select target files:**  
   - `audio` → **Process only MP3 files**  
   - `video` → **Process only MP4 files**  
   - `both` → **Process both MP3 and MP4 files**

## 📌 audio_to_text.py & audio_to_text_no_cut.py (English)  

These Python scripts convert **MP3 audio files to text using OpenAI Whisper Large v3**. They offer **two transcription approaches**:  
- **`audio_to_text.py`** → Processes audio **by splitting it into smaller chunks** (cut).  
- **`audio_to_text_no_cut.py`** → Processes the entire audio **without splitting** (no cut).  

---

### 🛠 **Features**  
✔ **Leverages OpenAI Whisper Large v3 for high-accuracy transcription.**  
✔ **Two processing modes:** chunked transcription (**cut**) or full transcription (**no cut**).  
✔ **Supports transcription in Turkish.**  
✔ **Converts MP3 files to mono and resamples them to 16kHz.**  
✔ **Adds timestamps for each processed segment (only in cut mode).**  
✔ **Stores results in JSON format.**  
✔ **Utilizes techniques like Beam Search and Attention Mask for improved accuracy.**  

### ⚙ **Usage**  

1. **Run the script:**  
   **For chunked transcription (cut mode):**  
   ```bash
   python audio_to_text.py
   ```
   **For full transcription without splitting (no cut mode):**  
   ```bash
   python audio_to_text_no_cut.py
   ```

2. **JSON output files:**  
   - `audio_to_text.py` saves output to **`transcriptions.json`**.  
   - `audio_to_text_no_cut.py` saves output to **`transcriptions-no-cut.json`**.  
   - JSON files contain **original file name, transcribed text, and (for cut mode) timestamps**.  

---

## 📌 Model Used: Whisper Large v3  

- **Model:** OpenAI **Whisper Large v3**  
- **Language:** Turkish (`tr`)  
- **Processing Type:** **FP16 (float16) GPU-accelerated transcription**  
- **Audio Sample Rate:** 16kHz  
- **Output Format:** JSON

## 📌 audio_to_text_elevenlabs.py (English)  

This Python script converts **MP3 audio files to text using ElevenLabs’ Speech-to-Text model**. **An API key is required to run** and must be stored in a `.env` file.  

---

### 🛠 **Features**  
✔ **Uses ElevenLabs `scribe_v1` model for transcription.**  
✔ **Transcribes audio in Turkish (`tur`).**  
✔ **Supports speaker diarization (identifies different speakers).**  
✔ **Can tag audio events like laughter, applause, etc. (optional).**  
✔ **Stores results in JSON format.**  
✔ **API key is securely stored in a `.env` file.**  

### ⚙ **Usage**  

1. **Add your API key to the `.env` file:**  
   Your `.env` file should be formatted as follows:  
   ```env
   ELEVENLABS_API_KEY=your_api_key_here
   ```

2. **Run the script:**  
   ```bash
   python audio_to_text_elevenlabs.py
   ```

3. **JSON output file:**  
   - Results are saved in **`output.json`** by default.  
   - JSON includes **original file name, transcribed text, and speaker diarization data.**


## 📌 dataset/ Directory (English)  

This directory contains **JSON-formatted transcript data** extracted from the YouTube playlist’s audio files.  

---

### 📂 **Contents**  
✔ **`transcriptions.json`** → Transcriptions are **chunked based on time segments**.  
✔ **`transcriptions-no-cut.json`** → **Full transcription stored as a single text**, without chunking.  
✔ **Both files** contain **file names and corresponding transcriptions in JSON format**.  
✔ **Chunk-based transcription** allows for future regex-based time-segment extraction and analysis.