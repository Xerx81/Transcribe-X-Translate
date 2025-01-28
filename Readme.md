# LexiBot - Discord Transcription & Translation Bot

---

## Overview
LexiBot is a Discord bot that transcribes and translates audio from videos into text. Users provide a video URL, and the bot:
1. Downloads the video's audio.
2. Transcribes the audio using OpenAI's Whisper AI model.
3. Translates the transcription into the desired language using Google Translate.
4. Sends the transcription and translation as downloadable `.txt` files in Discord.

---

## Features
- Slash command (`/lexibot`) for ease of use.
- Supports multiple languages for translation.
- Handles large transcriptions and translations by saving them as `.txt` files.
- Powered by Whisper AI for accurate transcription.

---

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Xerx81/Transcribe-X-Translate.git
   cd Transcribe-X-Translate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Whisper and yt-dlp requires FFmpeg to work properly. Install [here](https://www.ffmpeg.org/download.html)

4. Add your bot's token in the `.env` file:
   ```
   TOKEN=your_discord_bot_token
   ```

5. Run the bot:
   ```bash
   python main.py
   ```

---

## Bot Command Details
- **Command**: `/lexibot`
  - **Parameters**:
    - `video_url`: URL of the video for transcription (e.g., YouTube link).
    - `translate_lang`: Language code for translation (e.g., `en` for English, `fr` for French).

---

## Credits
- **Transcription**: [Whisper AI](https://github.com/openai/whisper) by OpenAI.
- **Translation**: Google Translate API.
- **Audio Download**: yt-dlp.
- **Discord Bot Framework**: [discord.py](https://discordpy.readthedocs.io/).

---
