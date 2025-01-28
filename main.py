import discord
import os
import subprocess
import warnings
import whisper
from discord import app_commands
from dotenv import load_dotenv
from googletrans import Translator
from typing import Optional, Tuple 

# Ignore specific warnings to clean up terminal output
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


# Function to download audio from a video URL using yt-dlp
def download_audio(video_url, output_file="audio.mp3") -> Optional[str]:
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
def transcribe_and_translate(audio_file, target_language) -> Tuple[Optional[str], Optional[str]]:
    try:
        # Load the Whisper model
        model = whisper.load_model("base")
        print("Transcribing... Please wait.")

        # Transcribe the audio file
        result = model.transcribe(audio_file)
        transcription = result['text']  # Extract the transcription text
        print("Transcription Successfull")

        # Translate the transcription to the target language
        print(f"Translating to {target_language}... Please wait.")
        translator = Translator()
        translation = translator.translate(transcription, dest=target_language).text
        print("Translation Successfull")
        
        return transcription, translation


    except Exception as e:
        print(f"Error: {e}")
        return None, None


def create_txt_file(input_file, output_file):
        with open(output_file, "w") as file:
            file.write(input_file)
        print(f"{output_file} file is created")


# Main function to execute the script
if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file

    # Define intents to specify which events your bot will receive
    intents = discord.Intents.default()
    intents.message_content = True  # Allow the bot to read message content

    # Create a client instance with the specified intents
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)  # Set up a command tree for slash commands

    @client.event
    async def on_ready() -> None:
        print(f'We have logged in as {client.user}')
        try:
            synced = await tree.sync()  # Sync all commands
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    
    @tree.command(name="lexibot", description="Transcribe and Translate any video by its url")
    @app_commands.describe(video_url="Url of the video for transcription", translate_lang="Name of language for translation. e.g. en")
    async def run_bot(interaction: discord.Interaction, video_url: str, translate_lang: str) -> None:
        await interaction.response.defer(ephemeral=True)

        # Download the audio from the video link
        audio_file = download_audio(video_url, "audio.mp3")  

        # Transcribe and translate the downloaded audio
        transcription, translation = transcribe_and_translate(audio_file, translate_lang)

        embed = discord.Embed(
                    title="LexiBot",
                    description=f"Video url: {video_url}\nTranslate Language: {translate_lang}",
                    color=discord.Color.green()
                )

        # Add embed field
        embed.set_footer(text="Bot by @iamxerx")

        # Save transcription and translation as text files
        if transcription and translation:
            create_txt_file(transcription, "transcription.txt")
            create_txt_file(translation, "translation.txt")

        # Clean up by removing the downloaded audio file
        if audio_file:
            os.remove(audio_file)

        # Store files in a list
        files = [discord.File("transcription.txt"), discord.File("translation.txt")]
        
        # Send message with files attached
        await interaction.followup.send(embed=embed, files=files)

    client.run(os.getenv('TOKEN'))
