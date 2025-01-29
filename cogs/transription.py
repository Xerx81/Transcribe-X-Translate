import discord
import os
from discord import app_commands
from discord.ext import commands

import config
from utils.audio import download_audio
from utils.helper import transcribe_and_translate, create_txt_file


class Transcription(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="lexibot", description="Transcribe and Translate any video by its url")
    @app_commands.describe(
            video_url="Url of the video for transcription",
            translate_lang="Name of language for translation. e.g. en"
            )
    async def transcribe(
            self,
            interaction: discord.Interaction,
            video_url: str,
            translate_lang: str
            ) -> None:
        await interaction.response.defer(ephemeral=True)

        try:
            # Download audio
            audio_file = download_audio(video_url)
            if not audio_file:
                await interaction.followup.send("Failed to download audio.")
                return

            # Transcribe and translate
            transcription, translation = await transcribe_and_translate(audio_file, translate_lang)
            if not transcription or not translation:
                await interaction.followup.send("Failed to transcribe or translate the audio.")
                return

            # Create embed
            embed = discord.Embed(
                    title="LexiBot",
                    description=f"Video url: {video_url}\nTranslate Language: {translate_lang}",
                    color=config.EMBED_COLOR
                    )
            embed.set_footer(text="Bot by @iamxerx")

            # Save files
            await create_txt_file(transcription, str(config.TRANSCRIPTION_FILE))
            await create_txt_file(translation, str(config.TRANSLATION_FILE))

            # Send response
            files = [
                    discord.File(config.TRANSCRIPTION_FILE),
                    discord.File(config.TRANSLATION_FILE)
                    ]
            await interaction.followup.send(embed=embed, files=files)

        finally:
            # Cleanup
            if os.path.exists(config.TEMP_AUDIO_FILE):
                os.remove(config.TEMP_AUDIO_FILE)

async def setup(bot):
    await bot.add_cog(Transcription(bot))
