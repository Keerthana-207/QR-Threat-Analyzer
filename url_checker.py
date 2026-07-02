from urllib.parse import urlparse


def is_valid_url(text):
    if not isinstance(text, str) or not text.strip():
        return False

    candidate = text.strip()
    if "://" not in candidate:
        candidate = f"http://{candidate}"

    parsed = urlparse(candidate)
    return bool(parsed.scheme in ("http", "https") and parsed.netloc and "." in parsed.netloc)
