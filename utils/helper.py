import whisper
from deep_translator import GoogleTranslator
from typing import Optional, Tuple

import config


async def create_txt_file(content: str, output_file: str) -> None:
    with open(output_file, "w", encoding='utf-8') as file:
        file.write(content)
    print(f"{output_file} file is created")

async def transcribe_and_translate(audio_file: str, target_language: str) -> Tuple[Optional[str], Optional[str]]:
    try:
        # Load the whisper model
        model = whisper.load_model(config.WHISPER_MODEL)

        # Transcribe the audio file
        print("Transcribing... Please wait.")
        result = model.transcribe(audio_file)
        transcription = result['text']
        print("Transcription Successful")

        # Translate the transcription to the target language
        print(f"Translating to {target_language}... Please wait.")
        translator = GoogleTranslator(source="auto", target=target_language)
        translation = translator.translate(transcription)
        print("Translation Successful")

        return transcription, translation

    except Exception as e:
        print(f"Error in transcription/translation: {e}")
        return None, None

