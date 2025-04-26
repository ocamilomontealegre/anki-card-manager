import asyncio
from pathlib import Path
from google.cloud import texttospeech
from google.oauth2 import service_account


class GoogleUtils:
    @staticmethod
    async def synthetize_text(text: str, output_file: Path):
        credentials = service_account.Credentials.from_service_account_file(
            r"C:\Users\CAMILO\Documents\01_Software_Development\06_Projects\03_Python\anki-card-manager\protected\gothic-sled-457121-r0-07a2d7ada2ed.json"
        )

        client = texttospeech.TextToSpeechAsyncClient(credentials=credentials)

        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Wavenet-D",
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
    output_path = Path(
        "../../../uploads/random.mp3"
    )  # Full file path (with filename)
    output_path.parent.mkdir(
        parents=True, exist_ok=True
    )  # Make sure the directory exists
    await GoogleUtils.synthetize_text(
        "Hello my name is Camilo", output_file=output_path
    )


# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
