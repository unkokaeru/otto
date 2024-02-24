# Otto

Otto is a digital assistant that can help you with a variety of tasks. It utilises the OpenAI GPT-3.5-Turbo language model to understand and respond to natural language commands, in combination with the ElevenLabs API to produce audio output and the OpenAI Whisper API to process speech input.

## Getting Started

Follow these instructions to get Otto up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.8 or newer
- pip (Python package manager)

### Installation

1. Clone the repository to your local machine:

```
git clone https://github.com/unkokaeru/otto.git
```

2. Navigate to the Otto directory:

```
cd otto
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

The `requirements.txt` includes:
- python-dotenv==1.0.1
- rich==12.5.1
- requests==2.31.0
- openai==1.7.1
- SpeechRecognition==3.10.1

4. Create a `.env` file in the config directory and add your API keys (replace with your actual keys):

```
OPENAI_API_KEY=your_openai_api_key_here
ELEVEN_API_KEY=your_eleven_api_key_here
```

5. Choose a voice ID in `cfg.py` from the ElevenLabs website and configure it accordingly.

### Usage

Run `main.py` to start Otto:

```
python main.py
```

Speak to Otto using your microphone, and it will respond with the chosen voice from ElevenLabs.

## Testing

Currently, testing involves direct interaction with Otto to ensure all integrated APIs are functioning as expected. Future versions will include automated tests.

## Deployment

For deploying Otto in a live environment, ensure that all environmental variables are securely configured, and follow best practices for deploying Python applications.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.