"""Configuration file for Otto."""

import os
from pathlib import Path

from dotenv import load_dotenv
from rich.logging import RichHandler

# General Configuration
USER_NAME = "William"  # Change this to your name
EXIT_COMMANDS = [
    "shutdown",
    "shotdown",
    "shotsdown",
    "exit",
    "quit",
    "goodbye",
    "bye",
    "turnoff",
]

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(message)s",
    "datefmt": "[%X]",
    "handlers": [RichHandler(rich_tracebacks=True)],
}

# OpenAI API Configuration
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = "asst_eBljvhz5O0DCf8n8lLbXkCRT"

# ElevenLabs API Configuration
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
ELEVEN_VOICE_ID = "rftVusAekuzb5nbS3Kc4"

# Wake Word Configuration
WAKE_WORDS = ["hey otto", "hey auto", "toyota", "otto", "auto", "hilton"]
DURATION = 3
