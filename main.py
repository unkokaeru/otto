"""A digital assistant named Otto."""

import re

import speech_recognition as sr
from openai import OpenAI

from config.cfg import (
    ASSISTANT_ID,
    DURATION,
    ELEVEN_API_KEY,
    ELEVEN_VOICE_ID,
    EXIT_COMMANDS,
    OPENAI_API_KEY,
    USER_NAME,
    WAKE_WORDS,
)
from core.speech_recognition import listen_for_wake_words, microphone_input
from integrations.eleven_labs import text_to_speech
from integrations.openai import prompt_assistant, speech_to_text
from utils.logger import get_logger


def main() -> None:
    """
    The main function for the Otto digital assistant.
    :return: None
    """

    # Initialise the required objects
    ai_client = OpenAI(api_key=OPENAI_API_KEY)
    logger = get_logger()
    recogniser = sr.Recognizer()
    thread = ai_client.beta.threads.create()

    # Keep the digital assistant running
    while True:
        # Listen for the wake word
        wake_word_detected = listen_for_wake_words(
            logger, recogniser, WAKE_WORDS, DURATION
        )

        if not wake_word_detected:
            logger.error("The wake word was not detected.")
            continue

        # Notify the user that the wake word was detected
        logger.info("The wake word was detected. Please speak.")

        # Record audio from the microphone
        user_audio_path = microphone_input(logger)

        # Convert speech to text
        text = speech_to_text(logger, ai_client, user_audio_path)

        # Check if the user wants to shut down the digital assistant
        if re.sub(r"[^a-z]", "", text.lower()) in EXIT_COMMANDS:
            logger.info("Shutdown command received. Turning off.")
            break  # Break the loop and end the program

        # Prompt the ChatGPT API with the transcribed text
        response = prompt_assistant(
            logger, ai_client, thread, ASSISTANT_ID, USER_NAME, text
        )
        logger.info(f"Response: {response}")

        # Convert the response to speech
        otto_audio_path = text_to_speech(
            logger, ELEVEN_API_KEY, ELEVEN_VOICE_ID, response
        )

    # Attempt to delete the audio files
    try:
        user_audio_path.unlink()
        otto_audio_path.unlink()
    except PermissionError:
        logger.error(
            "The audio file(s) could not be deleted. Please delete them manually."
        )


if __name__ == "__main__":
    main()
