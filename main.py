import os
import subprocess
import warnings
import whisper
from googletrans import Translator

# Ignore specific warnings to clean up terminal output
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


# Function to download audio from a video URL using yt-dlp
def download_audio(video_url, output_file="audio.mp3") -> str:
    try:
        # Command to download audio in mp3 format
        command = [
                "yt-dlp",
                "-x", "--audio-format", "mp3",
                "-o", output_file,
                video_url
        ]
        subprocess.run(command, check=True)  # Execute the command
        print(f"Audio downloaded successfully as {output_file}")
        return output_file  # Return the name of the downloaded file

    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        return None


# Function to transcribe audio and translate the transcription
def transcribe_and_translate(audio_file, target_language):
    try:
        # Load the Whisper model
        model = whisper.load_model("base")
        print("Transcribing... Please wait.")

        # Transcribe the audio file
        result = model.transcribe(audio_file)
        transcription = result['text']  # Extract the transcription text

        # Translate the transcription to the target language
        print(f"Translating to {target_language}... Please wait.")
        translator = Translator()
        translation = translator.translate(transcription, dest=target_language).text
        
        return transcription, translation


    except Exception as e:
        print(f"Error: {e}")
        return None, None


# Main function to execute the script
if __name__ == "__main__":

    # Prompt the user for the video URL and target translation language
    video_url = input("Enter the video link: ")
    target_language = input("Enter language key for translation: ")

    # Download the audio from the video link
    audio_file = download_audio(video_url, "audio.mp3")  

    # Transcribe and translate the downloaded audio
    transcripted_file, translation = transcribe_and_translate(audio_file, target_language)

    # Save the transcription to a text file
    if transcripted_file:
        output_txt = "transcription.txt"
        with open(output_txt, "w") as file:
            file.write(transcripted_file)
        print(f"Transcription saved to \"{output_txt}\"")

    # Save the translation to a separate text file
    if translation:
        output_txt = "translation.txt"
        with open(output_txt, "w") as file:
            file.write(translation)
        print(f"Translation saved to \"{output_txt}\"")

    # Clean up by removing the downloaded audio file
    if audio_file:
        os.remove(audio_file)

