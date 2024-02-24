"""A digital assistant named Otto."""

import speech_recognition as sr
from openai import OpenAI

from config.cfg import (
    ELEVEN_API_KEY,
    ELEVEN_VOICE_ID,
    OPENAI_API_KEY,
    WAKE_WORD,
    DURATION,
)
from core.speech_recognition import microphone_input, listen_for_wake_word
from integrations.eleven_labs import text_to_speech
from integrations.openai import prompt_gpt_turbo, speech_to_text
from utils.logger import get_logger


def main() -> None:
    """
    The main function for the Otto digital assistant.
    :return: None
    """

    # Initialise the logger and OpenAI client
    ai_client = OpenAI(api_key=OPENAI_API_KEY)
    logger = get_logger()
    recogniser = sr.Recognizer()

    # Listen for the wake word
    wake_word_detected = listen_for_wake_word(logger, recogniser, WAKE_WORD, DURATION)

    if not wake_word_detected:
        logger.error("The wake word was not detected.")
        return

    # Notify the user that the wake word was detected
    logger.info("The wake word was detected. Please speak.")

    # Record audio from the microphone
    user_audio_path = microphone_input(logger)

    # Convert speech to text
    text = speech_to_text(logger, ai_client, user_audio_path)

    # Prompt the ChatGPT API with the transcribed text
    response = prompt_gpt_turbo(logger, ai_client, text)
    logger.info(f"Response: {response}")

    # Convert the response to speech
    text_to_speech(logger, ELEVEN_API_KEY, ELEVEN_VOICE_ID, response)

    # Attempt to delete the audio files
    try:
        user_audio_path.unlink()
    except PermissionError:
        logger.error(
            "The audio file(s) could not be deleted. Please delete them manually."
        )


if __name__ == "__main__":
    main()
