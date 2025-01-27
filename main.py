import os
import subprocess
import warnings
import whisper

# Ignore warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


def download_audio(video_url, output_file="audio.mp3"):
    try:
        command = [
                "yt-dlp",
                "-x", "--audio-format", "mp3",
                "-o", output_file,
                video_url
        ]
        subprocess.run(command, check=True)
        print(f"Audio downloaded successfully as {output_file}")
        return output_file

    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        return None


def transcribe(audio_file):
    try:
        model = whisper.load_model("base")
        print("Transcribing... Please wait.")
        result = model.transcribe(audio_file)
        return result['text']

    except Exception as e:
        print(f"Error transcripting file: {e}")
        return None


if __name__ == "__main__":
    video_url = input("Enter the video link: ")

    audio_file = download_audio(video_url, "audio.mp3")  
    transcripted_file = transcribe(audio_file)

    if transcripted_file:
        output_txt = "transcription.txt"
        with open(output_txt, "w") as file:
            file.write(transcripted_file)
        print(f"Transcription saved to \"{output_txt}\"")

    if audio_file:
        os.remove(audio_file)

