from pathlib import Path


# Paths
BASE_DIR = Path(__file__).parent
TEMP_DIR = BASE_DIR / "data" / "temp"

# Bot settings
WHISPER_MODEL = "base"
EMBED_COLOR = 0xADDEE6  # Cyan

# File settings
AUDIO_FORMAT = "mp3"
TEMP_AUDIO_FILE = TEMP_DIR / f"audio.{AUDIO_FORMAT}"
TRANSCRIPTION_FILE = TEMP_DIR / "transcription.txt"
TRANSLATION_FILE = TEMP_DIR / "translation.txt"
