"""OpenAI API integration module."""

from pathlib import Path
from typing import cast

from openai import OpenAI


def prompt_assistant(
    logger, client: OpenAI, thread, ASSISTANT_ID: str, USER_NAME: str, text: str
) -> str:
    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=text
    )

    logger.info(f"Message added to thread: {message}")

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
        instructions=f"The user's name is {USER_NAME}.",
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread.id)

    logger.info(f"Messages retrieved: {messages}")

    return messages.data[0].content[0].text.value


def prompt_gpt_turbo(
    logger,
    client: OpenAI,
    user_message: str,
    system_message: str = "You are an assistant called Otto.",
) -> str:
    """
    A function to prompt the ChatGPT API to generate a response to a user message.
    :param user_message: The user's message to respond to.
    :param system_message: The system's message to respond to.
    :return: The response from the ChatGPT API.
    """

    logger.info("Starting to prompt the ChatGPT API.")

    try:
        logger.info(f"Prompting the ChatGPT API with: '{user_message}'.")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        )
        logger.info("Response received.")
        return cast(str, response.choices[0].message.content)
    except Exception as e:
        logger.error("Error: %s", e)
        return "..."


def speech_to_text(logger, client: OpenAI, audio_loc: Path) -> str:
    """
    Convert speech to text using the OpenAI Whisper API.
    :param client: The OpenAI client.
    :param audio_loc: The location of the audio file to be transcribed.
    :return: The transcribed text.
    """

    # The location of the audio file to be transcribed.
    audio_file = open(audio_loc, "rb")

    # Transcribe the audio file.
    text = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text",
    )

    # Log the transcribed text.
    logger.info(f"Transcribed text: {text}")

    return text
