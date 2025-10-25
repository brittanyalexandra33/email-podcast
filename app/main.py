import argparse, hashlib, datetime as dt
from pathlib import Path
from email.utils import parsedate_to_datetime

from .config import *
from .gmail_client import gmail_service, list_messages, get_message, get_header, get_html_body
from .extract import extract_text
from .summarize import summarize_for_audio
from .tts import synthesize_to_mp3
from .rss import Episode, build_feed

QUERY_DEFAULT = '(category:updates OR category:promotions) list:(*) -subject:receipt -subject:invoice -from:noreply@*'

def episode_id(sender: str, subject: str, date_str: str) -> str:
    key = f"{sender}|{subject}|{date_str}"
    return hashlib.sha256(key.encode()).hexdigest()[:24]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--since', default=SINCE_DEFAULT, help="Gmail window like 7d, 30d (default from .env)")
    parser.add_argument('--query', default=QUERY_DEFAULT, help="Override Gmail query")
    args = parser.parse_args()

    out_dir = Path(OUT_DIR); out_dir.mkdir(parents=True, exist_ok=True)

    svc = gmail_service(SECRETS_DIR)
    q = f"{args.query} newer_than:{args.since}" if 'newer_than:' not in args.since and 'newer_than:' not in args.query else args.query
    ids = list_messages(svc, q, max_n=30)

    episodes = []
    for mid in ids:
        msg = get_message(svc, mid)
        subject = get_header(msg, 'Subject') or 'Newsletter'
        sender  = get_header(msg, 'From') or 'Unknown'
        date_h  = get_header(msg, 'Date') or ''
        try:
            pub_dt = parsedate_to_datetime(date_h)
            if pub_dt.tzinfo is None:
                pub_dt = pub_dt.replace(tzinfo=dt.timezone.utc)
        except Exception:
            pub_dt = dt.datetime.now(dt.timezone.utc)

        html = get_html_body(msg)
        text = extract_text(html)
        if len(text.split()) < 120:
            continue

        script = summarize_for_audio(text, source=sender, date_str=date_h)
        eid = episode_id(sender, subject, date_h)
        audio_path = out_dir / f"{eid}.mp3"
        synthesize_to_mp3(script, audio_path)

        audio_url = f"{AUDIO_BASE_URL}/{audio_path.name}"
        episodes.append(Episode(
            guid=eid, title=subject, description=f"{sender} — {subject}",
            pub_date=pub_dt, audio_url=audio_url, length_bytes=audio_path.stat().st_size
        ))

    feed_xml = build_feed(FEED_TITLE, FEED_PUBLIC_URL, FEED_DESCRIPTION, episodes)
    (out_dir / 'podcast.xml').write_text(feed_xml, encoding='utf-8')
    print(f"Wrote feed with {len(episodes)} episode(s) to {out_dir/'podcast.xml'}")

if __name__ == '__main__':
    main()
