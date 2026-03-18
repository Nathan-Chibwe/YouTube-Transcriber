# youtube-transcriber

Minimal helper to fetch YouTube captions or fall back to audio transcription.

Installation (PowerShell):

```powershell
python -m pip install -r requirements.txt
```

If you prefer a single command:

```powershell
python -m pip install youtube-transcript-api yt-dlp
```

Quick usage (from Python):

```python
from transcript import get_transcript

url = "https://www.youtube.com/watch?v=VIDEO_ID"
transcript, method, error = get_transcript(url)
if error:
    print("Error:", error)
else:
    print("Fetched via:", method)
    for item in transcript[:10]:
        print(item["timestamp"], item["text"])
```

Notes:
- If `youtube-transcript-api` is not installed the module will skip caption fetch
  and automatically fall back to the Whisper-based transcriber (if available).
- For Whisper-based transcription you may need to install an appropriate Whisper
  package (see `requirements.txt` comments).
# 🎬 YouTube Transcriber & Quote Extractor

A Streamlit web app that fetches transcripts from any YouTube video,
lets you search through them, and extract or auto-detect meaningful quotes.

---

## Features

| Feature | Details |
|---|---|
| **Transcript fetching** | Uses YouTube's built-in captions first; falls back to Whisper if unavailable |
| **Timestamped output** | Every line shows its `mm:ss` timestamp |
| **Keyword search** | Highlights matching lines in the transcript |
| **Manual quote saving** | Click "Save" next to any line |
| **Auto quote detection** | Heuristic scan for inspirational / emotional sentences |
| **Export** | Download quotes as `.txt` or copy from the sidebar |

---

## Project Structure

```
youtube-transcriber/
├── main.py                  # Streamlit UI
├── transcript.py            # Caption fetching logic
├── whisper_transcriber.py   # yt-dlp + Whisper fallback
├── quotes.py                # Quote detection & export
├── utils.py                 # Shared helpers
├── requirements.txt
└── README.md
```

---

## Prerequisites

- **Python 3.10+**
- **ffmpeg** – required by yt-dlp for audio conversion

### Install ffmpeg

| OS | Command |
|---|---|
| macOS | `brew install ffmpeg` |
| Ubuntu / Debian | `sudo apt install ffmpeg` |
| Windows | Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH |

---

## Installation

```bash
# 1. Unzip the project folder
unzip youtube-transcriber.zip
cd youtube-transcriber

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

> **Note on Whisper / PyTorch:**
> `openai-whisper` pulls in `torch`. On CPU-only machines this is large (~800 MB).
> If you only ever use videos with existing captions you can skip Whisper with:
> `pip install streamlit youtube-transcript-api yt-dlp`

---

## How to Run

```bash
streamlit run main.py
```

The app opens automatically at `http://localhost:8501`.

---

## Example Usage

1. Paste a YouTube URL into the input box:
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```
2. Click **🚀 Get Transcript**.
3. The app tries YouTube captions first. If none exist, it downloads the audio and runs Whisper.
4. Browse the timestamped transcript.
5. Type a keyword in the search bar to highlight matching lines.
6. Click **💬 Save** next to any line to save it as a quote.
7. Click **🤖 Detect Meaningful Quotes** to auto-find inspirational lines.
8. Use the **sidebar** to review saved quotes, copy them, or download as `saved_quotes.txt`.

---

## Configuration

### Change the Whisper model

Open `whisper_transcriber.py` and change the model size on this line:

```python
model = whisper.load_model("base")
#                           ^^^^
# Options: tiny | base | small | medium | large
# Larger = more accurate but slower and uses more RAM
```

### Change the auto-detection sensitivity

Open `quotes.py` and adjust `threshold` in `detect_meaningful_quotes()`:

```python
def detect_meaningful_quotes(transcript, threshold=1):
    # threshold=1  → many results
    # threshold=3  → only high-confidence quotes
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `No transcript found` | The video may have no captions and audio download will start automatically |
| `ffmpeg not found` | Install ffmpeg and ensure it is on your system PATH |
| Whisper is very slow | Use a smaller model (`tiny` or `base`) or run on a GPU |
| `Invalid YouTube URL` | Make sure the URL contains a valid video ID (11 characters) |

---

## License

MIT – free to use, modify, and distribute.
