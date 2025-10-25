# Placeholder summarizer. Replace with your LLM provider.
# Keep outputs "speakable" and concise.

TEMPLATE = """INTRO:
{hook}

KEY POINTS:
{points}

CLOSER:
Actionable takeaway: {takeaway}
Source: {source} ({date})
"""

def summarize_for_audio(text: str, source: str, date_str: str) -> str:
    # A naive extractive approach; swap with an LLM for quality.
    words = text.split()
    hook = ' '.join(words[:30]) + ('...' if len(words) > 30 else '')
    points = []
    chunks = [words[i:i+70] for i in range(0, min(len(words), 700), 70)]
    for ch in chunks[:5]:
        points.append('• ' + ' '.join(ch))
    takeaway = 'Remember the key idea above and consider one concrete next step today.'
    return TEMPLATE.format(hook=hook, points='\n'.join(points), takeaway=takeaway, source=source, date=date_str)
