import re
from urllib.parse import urlparse

from redirect_analyzer import contains_redirect_pattern
from url_checker import is_valid_url

BLACKLIST_KEYWORDS = [
    "login", "verify", "secure", "bank", "account", "password", "credential",
    "signin", "auth", "update", "confirm", "support", "billing", "reset"
]
SHORTENER_DOMAINS = [
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "buff.ly", "is.gd", "bc.vc",
    "shorte.st", "mcaf.ee", "rebrand.ly", "t.ly"
]
SUSPICIOUS_TLDS = [
    "xyz", "top", "loan", "work", "info", "click", "gq", "ml", "tk", "ga", "cf"
]


def analyze_payload(payload):
    text = payload.strip()
    score = 0
    verdict = "Safe"
    source_type = "QR Payload"
    analysis = {
        "transport": "Unknown",
        "domain": None,
        "https": False,
        "notes": []
    }

    if not text:
        return {
            "payload": text,
            "score": score,
            "verdict": verdict,
            "source_type": source_type,
            "analysis": analysis,
            "reasons": analysis["notes"]
        }

    if text.upper().startswith("WIFI:"):
        source_type = "WiFi Configuration"
        analysis["notes"].append("Decoded WiFi configuration from QR payload.")
        score = 10
        verdict = "Safe"
        analysis["transport"] = "Not applicable"
        return {
            "payload": text,
            "score": score,
            "verdict": verdict,
            "source_type": source_type,
            "analysis": analysis
        }

    if text.upper().startswith(("SMSTO:", "MAILTO:", "TEL:", "BITCOIN:", "ETH:", "UPI:")):
        source_type = "Intent Payload"
        score = 20
        verdict = "Suspicious"
        analysis["notes"].append("Payload contains a non-HTTP intent or payment string.")
        analysis["transport"] = "Intent"
        return {
            "payload": text,
            "score": score,
            "verdict": verdict,
            "source_type": source_type,
            "analysis": analysis
        }

    if is_valid_url(text):
        source_type = "URL"
        if text.startswith(("http://", "https://")):
            normalized = text
            scheme_provided = True
        else:
            normalized = f"https://{text}"
            scheme_provided = False
        parsed = urlparse(normalized)
        host = (parsed.hostname or "").lower().strip()

        analysis["domain"] = host

        if scheme_provided:
            analysis["transport"] = parsed.scheme.upper()
            analysis["https"] = parsed.scheme == "https"
        else:
            analysis["transport"] = "UNSPECIFIED"
            analysis["https"] = False
            analysis["notes"].append("No explicit transport protocol provided in QR payload.")

        if scheme_provided:
            if parsed.scheme == "http":
                score += 15
                analysis["notes"].append("Unencrypted HTTP transport detected.")
            elif parsed.scheme == "https":
                analysis["notes"].append("HTTPS transport detected.")

        if any(host.endswith(short) for short in SHORTENER_DOMAINS):
            score += 30
            analysis["notes"].append("Shortener or redirect domain detected.")

        if any(host.endswith(f".{tld}") or host == tld for tld in SUSPICIOUS_TLDS):
            score += 25
            analysis["notes"].append("Suspicious top-level domain detected.")

        for keyword in BLACKLIST_KEYWORDS:
            if keyword in normalized.lower():
                score += 12
                analysis["notes"].append(f"Suspicious keyword '{keyword}' found in URL.")

        if parsed.query and re.search(r"redirect|return|next|continue|url=|to=", parsed.query, re.IGNORECASE):
            score += 20
            analysis["notes"].append("Redirect parameters found in query string.")

        if contains_redirect_pattern(normalized):
            score += 20
            analysis["notes"].append("Redirect pattern detected in URL.")

    else:
        source_type = "Text Payload"
        analysis["transport"] = "Plain text"
        if any(keyword in text.lower() for keyword in BLACKLIST_KEYWORDS):
            score += 20
            analysis["notes"].append("Suspicious keyword found in text payload.")
        if re.search(r"https?://", text, re.IGNORECASE):
            score += 15
            source_type = "Embedded URL"
            analysis["notes"].append("Embedded URL detected within text payload.")
        if len(text) > 150:
            score += 5
            analysis["notes"].append("Long payload may contain hidden instructions.")

    score = max(0, min(score, 100))

    if score >= 65:
        verdict = "Malicious"
    elif score >= 35:
        verdict = "Suspicious"
    else:
        verdict = "Safe"

    if not analysis["notes"]:
        analysis["notes"].append("No obvious threat patterns detected.")

    return {
        "payload": text,
        "score": score,
        "verdict": verdict,
        "source_type": source_type,
        "analysis": analysis
    }
