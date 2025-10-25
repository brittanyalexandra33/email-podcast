from bs4 import BeautifulSoup
import trafilatura

def extract_text(html: str) -> str:
    # Try Trafilatura first (great boilerplate removal)
    txt = trafilatura.extract(html, include_comments=False, include_tables=False)
    if txt and len(txt.split()) > 60:
        return txt
    # Fallback: simple HTML → text
    soup = BeautifulSoup(html, 'lxml')
    for tag in soup(['script','style','nav','footer','header','form']):
        tag.decompose()
    return ' '.join(soup.get_text(separator=' ').split())
