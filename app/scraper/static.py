import httpx
from bs4 import BeautifulSoup


def static_scrape(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; LyftrAssignment/1.0; +https://example.com)"
    }

    response = httpx.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "lxml")

    title = soup.title.text.strip() if soup.title else ""

    desc = soup.find("meta", attrs={"name": "description"})
    description = desc["content"].strip() if desc else ""

    language = soup.html.get("lang") if soup.html else ""

    canon = soup.find("link", rel="canonical")
    canonical = canon["href"] if canon else None

    text = soup.get_text(" ", strip=True)

    meta = {
        "title": title,
        "description": description,
        "language": language,
        "canonical": canonical
    }

    return response.text, meta, len(text)
