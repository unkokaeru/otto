"""Configuration file for Otto."""

import os
from pathlib import Path

from dotenv import load_dotenv
from rich.logging import RichHandler

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

# ElevenLabs API Configuration
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
ELEVEN_VOICE_ID = "rftVusAekuzb5nbS3Kc4"

# Wake Word Configuration
WAKE_WORD = "hey otto"
DURATION = 3
