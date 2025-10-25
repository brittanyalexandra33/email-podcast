import datetime as dt
from xml.sax.saxutils import escape
from dataclasses import dataclass
from typing import List

@dataclass
class Episode:
    guid: str
    title: str
    description: str
    pub_date: dt.datetime
    audio_url: str
    length_bytes: int

def build_feed(title: str, link: str, description: str, items: List[Episode]) -> str:
    now = dt.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
    head = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>'{title}'</title>
<link>'{link}'</link>
<description>'{description}'</description>
<lastBuildDate>'{now}'</lastBuildDate>
"""
    head = head.format(title=escape(title), link=escape(link), description=escape(description), now=now)
    body = []
    for it in items:
        item_xml = f"""<item>
<title>{escape(it.title)}</title>
<description>{escape(it.description)}</description>
<guid isPermaLink="false">{escape(it.guid)}</guid>
<pubDate>{it.pub_date.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
<enclosure url="{escape(it.audio_url)}" length="{it.length_bytes}" type="audio/mpeg"/>
</item>
"""
        body.append(item_xml)
    tail = "</channel></rss>\n"
    return head + ''.join(body) + tail
