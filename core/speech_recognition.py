"""Speech recognition module for the core package."""

from pathlib import Path

import speech_recognition as sr


def listen_for_wake_words(
    logger, r: sr.Recognizer, wake_words: list, DURATION: int
) -> bool:
    """
    Listen for any of the wake words and return True if any is detected.
    :param logger: The logger object.
    :param r: The speech recognition object.
    :param wake_words: The list of wake words to listen for.
    :param DURATION: The duration to listen for the wake words.
    :return: True if any wake word is detected, otherwise False.
    """

    # Ensure all wake words are in lowercase for consistent comparison
    wake_words = [word.lower() for word in wake_words]

    # Capture audio from the microphone
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=DURATION)
        logger.info("Listening for wake words...")
        while True:
            audio = r.listen(source, phrase_time_limit=DURATION)

            try:
                # Recognize speech using Google's speech recognition
                text = r.recognize_google(audio, show_all=False).lower()
                logger.info(f"Recognized: {text}")

                # Check if any of the wake words were said
                if any(wake_word in text for wake_word in wake_words):
                    logger.info("Wake word detected!")
                    return True

            except sr.UnknownValueError:
                # Speech was unintelligible
                logger.info("Could not understand audio")
            except sr.RequestError as e:
                # Could not request results from Google's speech recognition service
                logger.error(f"Could not request results; {e}")

    return False  # If loop exits or wake word not detected


def microphone_input(logger) -> Path:
    """
    Record audio until the user stops speaking and save it to a file.
    :return: The location of the audio file.
    """

    # Initialize the recognizer
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        logger.info("Please start speaking. Recording will end when you stop speaking.")

        # Adjust the recognizer sensitivity to ambient noise
        r.adjust_for_ambient_noise(source)

        # Listen to the first audio source until silence is detected
        audio = r.listen(source)
        logger.info("Recording stopped.")

    # Set the path to the audio file
    audio_path = Path(__file__).parent.parent / "temp/input.wav"

    # Save the audio data to the specified file
    with open(audio_path, "wb") as f:
        f.write(audio.get_wav_data())

    return Path(audio_path)
