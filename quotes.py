"""
quotes.py
─────────
Quote extraction utilities.

Auto-detection uses a keyword/heuristic approach to find
emotionally resonant, inspirational, or meaningful sentences.
"""


# ── Keyword banks ─────────────────────────────────────────────────────────────
INSPIRATIONAL_KEYWORDS = [
    "believe", "purpose", "meaning", "love", "hope", "dream", "journey",
    "strength", "courage", "faith", "soul", "heart", "life", "truth",
    "never give up", "power", "change", "grow", "inspire", "passion",
    "grateful", "gratitude", "bless", "light", "peace", "freedom",
    "wisdom", "learn", "transform", "potential", "achieve", "success",
    "overcome", "rise", "begin", "create", "vision", "mission",
]

# Minimum word count for a sentence to be considered as a quote candidate
MIN_WORDS = 6
# Maximum word count (very long sentences are usually not great quotes)
MAX_WORDS = 50


def _score_sentence(text: str) -> int:
    """
    Return a relevance score based on keyword presence.
    Higher score = more likely to be a meaningful quote.
    """
    text_lower = text.lower()
    score = 0
    for kw in INSPIRATIONAL_KEYWORDS:
        if kw in text_lower:
            score += 1
    return score


def detect_meaningful_quotes(transcript: list, threshold: int = 1) -> list:
    """
    Scan the transcript and return segments that look like meaningful quotes.

    Parameters
    ----------
    transcript : list[dict]
        Each dict has keys: start, timestamp, text
    threshold : int
        Minimum keyword score for a segment to be included.

    Returns
    -------
    list[dict] – filtered and scored transcript segments
    """
    candidates = []

    for entry in transcript:
        text = entry.get("text", "").strip()
        word_count = len(text.split())

        # Filter by length
        if word_count < MIN_WORDS or word_count > MAX_WORDS:
            continue

        # Filter by keyword score
        score = _score_sentence(text)
        if score >= threshold:
            candidates.append({
                "start":     entry["start"],
                "timestamp": entry["timestamp"],
                "text":      text,
                "score":     score,
            })

    # Sort by score descending so the best quotes appear first
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates


def save_quotes_to_file(quotes: list, filepath: str = "saved_quotes.txt") -> str:
    """
    Write the list of quote strings to a .txt file.

    Parameters
    ----------
    quotes   : list[str]
    filepath : str

    Returns
    -------
    str – absolute path of the saved file.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=== Saved Quotes ===\n\n")
        for i, quote in enumerate(quotes, start=1):
            f.write(f"{i}. {quote}\n\n")
    return filepath


def format_quote(timestamp: str, text: str) -> str:
    """Return a consistently formatted quote string."""
    return f"[{timestamp}] {text}"
