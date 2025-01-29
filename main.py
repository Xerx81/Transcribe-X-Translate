import discord
import os
import warnings
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path


# Ignore specific warnings to clean up terminal output
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


# Create necessary directories
Path("data/temp").mkdir(parents=True, exist_ok=True)

class LexiBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!',
                         intents=discord.Intents.all()
        )

    async def setup_hook(self):
        # Load cogs
        for cog_file in Path("cogs").glob("*.py"):
            if cog_file.stem != "__init__":
                await self.load_extension(f"cogs.{cog_file.stem}")

        await self.tree.sync()

def main():
    load_dotenv()
    client = LexiBot()
    client.run(os.getenv('TOKEN'))

if __name__ == "__main__":
    main()

