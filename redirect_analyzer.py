import re


def contains_redirect_pattern(text):
    if not isinstance(text, str):
        return False

    patterns = [
        r"redirect[\w]*=", r"return[\w]*=", r"next[\w]*=", r"continue[\w]*=", r"url=", r"to=",
        r"https?://[^\s]+/.*(redirect|login|secure|verify)",
    ]
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)
