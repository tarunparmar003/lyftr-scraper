from bs4 import BeautifulSoup
from urllib.parse import urljoin

MAX_HTML = 1200


def parse_html(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    sections = []

    # ---- NORMAL SEMANTIC BLOCKS ----
    blocks = soup.find_all(["header", "nav", "main", "section", "footer"])

    # ---- REACT / SPA FALLBACK ----
    if not blocks:
        root = soup.find(id="root") or soup.find(id="__next__")
        if root:
            blocks = [root]
        elif soup.body:
            blocks = [soup.body]

    for i, block in enumerate(blocks):
        text = block.get_text(" ", strip=True)
        if not text:
            continue

        label = " ".join(text.split()[:7])

        raw = str(block)
        truncated = len(raw) > MAX_HTML

        sections.append({
            "id": f"section-{i}",
            "type": "section",
            "label": label,
            "sourceUrl": base_url,
            "content": {
                "headings": [h.get_text(strip=True) for h in block.find_all(["h1", "h2", "h3"])],
                "text": text,
                "links": [
                    {
                        "text": a.get_text(strip=True),
                        "href": urljoin(base_url, a["href"])
                    }
                    for a in block.find_all("a", href=True)
                ],
                "images": [
                    {
                        "src": urljoin(base_url, img.get("src")),
                        "alt": img.get("alt", "")
                    }
                    for img in block.find_all("img")
                ],
                "lists": [
                    [li.get_text(strip=True) for li in ul.find_all("li")]
                    for ul in block.find_all(["ul", "ol"])
                ],
                "tables": []
            },
            "rawHtml": raw[:MAX_HTML],
            "truncated": truncated
        })

    # ---- FINAL GUARANTEE (SPEC SAFETY NET) ----
    if not sections and soup.body:
        text = soup.body.get_text(" ", strip=True)
        if text:
            sections.append({
                "id": "fallback-0",
                "type": "section",
                "label": "Main Content",
                "sourceUrl": base_url,
                "content": {
                    "headings": [],
                    "text": text,
                    "links": [],
                    "images": [],
                    "lists": [],
                    "tables": []
                },
                "rawHtml": str(soup.body)[:MAX_HTML],
                "truncated": len(str(soup.body)) > MAX_HTML
            })

    return sections
