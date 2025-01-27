import os
import subprocess
import warnings
import whisper
from googletrans import Translator

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


def transcribe_and_translate(audio_file, target_language):
    try:
        model = whisper.load_model("base")
        print("Transcribing... Please wait.")
        result = model.transcribe(audio_file)
        transcription = result['text']

        # Translate the transcription to the target language
        print(f"Translating to {target_language}... Please wait.")
        translator = Translator()
        translation = translator.translate(transcription, dest=target_language).text
        
        return transcription, translation


    except Exception as e:
        print(f"Error: {e}")
        return None, None


if __name__ == "__main__":
    video_url = input("Enter the video link: ")
    target_language = input("Enter language key for translation: ")

    audio_file = download_audio(video_url, "audio.mp3")  
    transcripted_file, translation = transcribe_and_translate(audio_file, target_language)

    if transcripted_file:
        output_txt = "transcription.txt"
        with open(output_txt, "w") as file:
            file.write(transcripted_file)
        print(f"Transcription saved to \"{output_txt}\"")

    if translation:
        output_txt = "translation.txt"
        with open(output_txt, "w") as file:
            file.write(translation)
        print(f"Translation saved to \"{output_txt}\"")

    if audio_file:
        os.remove(audio_file)

