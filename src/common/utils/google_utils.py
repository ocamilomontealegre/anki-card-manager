import asyncio
from os import startfile
from pathlib import Path
from google.cloud import texttospeech
from google.oauth2 import service_account

from modules.language.models.enums import Language
from ..env.env_config import get_env_variables
from ..maps import language_voice_map


class GoogleUtils:
    @staticmethod
    async def synthetize_text(
        text: str, language: Language, output_file: Path
    ):
        google_env = get_env_variables().google

        credentials = service_account.Credentials.from_service_account_file(
            google_env.credentials
        )

        client = texttospeech.TextToSpeechAsyncClient(credentials=credentials)

        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_voice_map[language]["language_code"],
            name=language_voice_map[language]["voice_model"],
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = await client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        with open(output_file, "wb") as out:
            out.write(response.audio_content)
            print(f"Audio content written to {output_file}")


async def main():
    output_path = Path("../../../uploads/random.mp3")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    await GoogleUtils.synthetize_text(
        "Ich spreche kein Deutsch", output_file=output_path
    )
    startfile(output_path)

if __name__ == "__main__":
    asyncio.run(main())
