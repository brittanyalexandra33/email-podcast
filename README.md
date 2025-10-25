# Email → Podcast Agent (Starter)

Turn your subscribed newsletters into a private podcast feed.

## Features (MVP)
- Detect newsletters in Gmail using queries (Promotions/Updates + List-Id).
- Extract readable text from HTML emails.
- Summarize into a speakable script.
- Convert to audio (TTS stub provided; wire in your preferred provider).
- Publish/update a private RSS feed (`out/podcast.xml`) with episode mp3s.

## Quickstart

### 1) Python env
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Enable Gmail API
- Go to Google Cloud Console → Enable **Gmail API** for your project.
- Create **OAuth Client ID** (Desktop app).
- Download `client_secret.json` to `secrets/client_secret.json`.

First run will open a browser to authorize. Tokens will be saved to `secrets/gmail_token.json`.

### 3) Configure .env
Copy `.env.sample` to `.env` and edit values as needed.

### 4) Run
```bash
python -m app.main --since 7d
```
This will create `out/podcast.xml`. The audio function is a stub—replace it with your TTS provider (ElevenLabs/Azure/Polly/Coqui).

### 5) Host the feed
Upload `out/` to S3/Cloudflare (or any static host). Subscribe to the feed URL in your podcast player.

## Development Notes
- The LLM summarizer is a placeholder. Replace with your model/provider in `app/summarize.py`.
- TTS is a placeholder. Replace with your provider in `app/tts.py`.
- RSS is vanilla XML; extend as you like (GUIDs, artwork, categories).

## Useful Gmail queries
- `category:updates OR category:promotions`
- `list:(*)`
- `newer_than:7d`
- Exclude noise: `-subject:receipt -subject:invoice -from:noreply@*`

