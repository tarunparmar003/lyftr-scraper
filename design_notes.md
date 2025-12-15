# Design Notes

## Static vs JS Fallback – Strategy
The scraper follows a static-first strategy. It first fetches raw HTML using `httpx` with a proper User-Agent and parses it using BeautifulSoup. If the extracted text length is below a threshold (heuristic: very little meaningful text or missing main content), the system falls back to JS rendering using Playwright. This approach keeps scraping fast for static pages while still supporting modern SPA/JS-heavy websites.

## Wait Strategy for JS
- [x] Network idle
- [ ] Fixed sleep
- [ ] Wait for selectors

**Details:**  
When using Playwright, the scraper waits for the `networkidle` state to ensure JavaScript execution and API calls are complete. This proved reliable for React/Vite/Next.js sites without hardcoding selectors.

## Click & Scroll Strategy
- **Click flows implemented:** None (scroll-based exploration only in current version)
- **Scroll / pagination approach:** Infinite scroll simulation using mouse wheel scrolling
- **Stop conditions:** Fixed scroll depth of 3 iterations with a short wait between each scroll

The scraper scrolls the page vertically three times to trigger lazy loading or infinite scroll behavior. Each scroll is recorded in the `interactions.scrolls` field.

## Section Grouping & Labels
- **How DOM is grouped into sections:**  
  Sections are identified using semantic HTML landmarks (`header`, `nav`, `main`, `section`, `footer`).  
  For SPA/React sites without semantic tags, the scraper falls back to the root container (`#root` or `#__next__`), and finally to the `<body>` element.

- **How section `type` and `label` are derived:**  
  All sections default to type `section`.  
  If no explicit heading exists, a fallback label is generated using the first 5–7 words of the section’s text content.

## Noise Filtering & Truncation
- **Noise filtering:**  
  No advanced noise filtering is applied. However, basic bot-blocking responses (e.g., Wikipedia robot warnings) are mitigated by using a proper User-Agent header.

- **HTML truncation:**  
  Raw HTML for each section is truncated to a fixed character limit to prevent oversized responses.  
  The `truncated` flag is set to `true` when truncation occurs.

