"""
text_cleaner.py

Cleans and normalizes raw resume text before skill extraction and matching.

Design decisions (documented per the assignment's "clean and normalize"
requirement):
- Lowercase everything so keyword matching is case-insensitive.
- Collapse repeated whitespace/newlines into single spaces.
- Strip most punctuation, but deliberately KEEP a short list of technical
  symbols (+, #, ., /) so multi-character tech terms like "C++", "C#",
  ".NET", and "CI/CD" survive cleaning intact -- stripping them naively
  would turn "C++" into "c" and "C#" into "c", both of which would then
  incorrectly match generic mentions of the letter C.
"""

import re

# Characters that must be preserved because they are part of real skill
# names, not just punctuation noise.
_PRESERVE_CHARS = r"+#./"


def normalize_whitespace(text: str) -> str:
    """Collapse runs of whitespace (including newlines/tabs) into single spaces."""
    return re.sub(r"\s+", " ", text).strip()


def clean_resume_text(raw_text: str) -> str:
    """Full cleaning pipeline: lowercase, strip noisy symbols, normalize spacing.

    Keeps +, #, ., / so technical terms like C++, C#, .NET, and CI/CD are
    not mangled into meaningless single letters.
    """
    text = raw_text.lower()

    # Remove characters that are not letters, digits, whitespace, or one of
    # the preserved technical symbols.
    pattern = rf"[^a-z0-9\s{re.escape(_PRESERVE_CHARS)}]"
    text = re.sub(pattern, " ", text)

    text = normalize_whitespace(text)
    return text


if __name__ == "__main__":
    # Quick manual sanity check when run directly.
    sample = """
    John Doe
    Email: john.doe@example.com | Phone: +1-555-123-4567

    SKILLS: Python, C++, C#, .NET, SQL, CI/CD, Machine Learning!!
    """
    cleaned = clean_resume_text(sample)
    print(cleaned)
    assert "c++" in cleaned
    assert "c#" in cleaned
    assert ".net" in cleaned
    assert "ci/cd" in cleaned
    print("Sanity checks passed: C++, C#, .NET, CI/CD all preserved.")
