from pathlib import Path

from aiofiles import open
from google.api_core.exceptions import GoogleAPIError
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import texttospeech
from google.oauth2 import service_account
from injector import inject

from common.enums.language_enum import Language
from common.env.env_config import EnvVariables
from common.lib.tts.tts_adapter import TtsAdapter
from common.loggers.models.abstracts.logger_abstract import Logger
from common.maps import language_voice_map


class GoogleTtsAdapter(TtsAdapter):
    @inject
    def __init__(self, logger: Logger):
        self._file = GoogleTtsAdapter.__name__

        self._logger = logger
        self._env = EnvVariables().get().google

    async def synthetize_text(self, *, text: str, language: Language, output_file: Path) -> str:
        method = GoogleTtsAdapter.synthetize_text.__name__

        try:
            credentials = service_account.Credentials.from_service_account_file(
                self._env.credentials
            )

            client = texttospeech.TextToSpeechAsyncClient(credentials=credentials)

            synthesis_input = texttospeech.SynthesisInput(text=text)

            voice = texttospeech.VoiceSelectionParams(
                language_code=language_voice_map[language.value]["language_code"],
                name=language_voice_map[language.value]["voice_model"],
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = await client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            async with open(output_file, "wb") as out:
                await out.write(response.audio_content)
                self._logger.debug(
                    f"Audio content written to {output_file}",
                    file=self._file,
                    method=method,
                )
            return str(output_file)
        except DefaultCredentialsError as e:
            self._logger.error(f"Google credentials error: {e}", file=self._file, method=method)
            raise

        except GoogleAPIError as e:
            self._logger.error(f"Google API error: {e}", file=self._file, method=method)
            raise

        except Exception as e:
            self._logger.error(
                f"Unexpected error during text synthesis: {e}",
                file=self._file,
                method=method,
            )
            raise
