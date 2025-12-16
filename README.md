# Lyftr AI – Full Stack Assignment
## How To Run 
uvicorn app.main:app

## How to run
```bash
chmod +x run.sh
./run.sh


## Limitations
- Only http/https URLs are supported.
- Scraping is limited to the provided page URL (single origin).
- Some websites may block automated access or restrict scraping.
- In such cases, partial data is returned with details in the `errors[]` field.

