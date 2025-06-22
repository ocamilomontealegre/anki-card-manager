from pathlib import Path
from google.cloud import texttospeech
from google.oauth2 import service_account
from google.api_core.exceptions import GoogleAPIError
from google.auth.exceptions import DefaultCredentialsError

from common.loggers.app_logger import AppLogger
from common.enums import Language
from ..env.env_config import EnvVariables
from ..maps import language_voice_map


logger = AppLogger()


class GoogleUtils:
    @staticmethod
    async def synthetize_text(
        text: str, language: Language, output_file: Path
    ) -> str:
        file = GoogleUtils.__name__
        method = GoogleUtils.synthetize_text.__name__

        try:
            google_env = EnvVariables.get().google

            credentials = (
                service_account.Credentials.from_service_account_file(
                    google_env.credentials
                )
            )

            client = texttospeech.TextToSpeechAsyncClient(
                credentials=credentials
            )

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
                logger.debug(
                    f"Audio content written to {output_file}",
                    file=file,
                    method=method,
                )
            return str(output_file)
        except DefaultCredentialsError as e:
            logger.error(
                f"Google credentials error: {e}", file=file, method=method
            )
            raise

        except GoogleAPIError as e:
            logger.error(f"Google API error: {e}", file=file, method=method)
            raise

        except Exception as e:
            logger.error(
                f"Unexpected error during text synthesis: {e}",
                file=file,
                method=method,
            )
            raise
