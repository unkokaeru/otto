"""Speech recognition module for the core package."""

from pathlib import Path

import speech_recognition as sr


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
    audio_path = Path(__file__).parent / "temp/input.wav"

    # Save the audio data to the specified file
    with open(audio_path, "wb") as f:
        f.write(audio.get_wav_data())

    return Path(audio_path)
