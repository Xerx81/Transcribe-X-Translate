import subprocess
from typing import Optional

import config

def download_audio(video_url: str, output_file: str = str(config.TEMP_AUDIO_FILE)) -> Optional[str]:
    try:
        command = [
            "yt-dlp",
            "-x", "--audio-format", config.AUDIO_FORMAT,
            "-o", output_file,
            video_url
        ]
        subprocess.run(command, check=True)
        print(f"Audio downloaded successfully as {output_file}")
        return output_file

    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        return None
