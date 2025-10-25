import os
from dotenv import load_dotenv
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Inbox Briefings")
FEED_TITLE = os.getenv("FEED_TITLE", "Inbox Briefings")
FEED_DESCRIPTION = os.getenv("FEED_DESCRIPTION", "Summarized newsletters.")
FEED_PUBLIC_URL = os.getenv("FEED_PUBLIC_URL", "https://example.com/podcast.xml")
AUDIO_BASE_URL = os.getenv("AUDIO_BASE_URL", "https://example.com/audio")
SINCE_DEFAULT = os.getenv("SINCE", "7d")

OUT_DIR = "out"
SECRETS_DIR = "secrets"

# Optional TTS keys
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
AZURE_TTS_KEY = os.getenv("AZURE_TTS_KEY")
AZURE_TTS_REGION = os.getenv("AZURE_TTS_REGION")
