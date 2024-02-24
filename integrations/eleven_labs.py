"""ElevenLabs API integration module."""

from pathlib import Path

import requests
from pydub import AudioSegment
from pydub.playback import play


def text_to_speech(
    logger, ELEVEN_API_KEY: str, ELEVEN_VOICE_ID: str, text: str
) -> None:
    """
    Convert text to speech using the ElevenLabs API.
    :param ELEVEN_API_KEY: The API key for the ElevenLabs API.
    :param ELEVEN_VOICE_ID: The ID of the voice to use for the speech.
    :param text: The text to be converted to speech.
    :return: None
    """

    CHUNK_SIZE = 1024

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"

    data = {"model_id": "eleven_multilingual_v2", "text": text}
    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=data, headers=headers)

    output_path = Path(__file__).parent.parent / "temp/output.mp3"

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    # Play the audio
    audio = AudioSegment.from_mp3(output_path)
    play(audio)
