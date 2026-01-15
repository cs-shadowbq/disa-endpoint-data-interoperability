"""Symbol font to Unicode conversion utilities.

When Excel uses the Symbol font, ASCII characters are mapped to Greek letters
and special symbols. This module provides conversion back to standard Latin text.
"""

# ruff: noqa: F601

# Reverse mapping: Greek letters back to Latin
# This is used when Symbol font was applied in Excel
GREEK_TO_LATIN = {
    # Uppercase Greek to Latin
    'Α': 'A', 'Β': 'B', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E', 'Ζ': 'Z',
    'Η': 'H', 'Θ': 'Q', 'Ι': 'I', 'Κ': 'K', 'Λ': 'L', 'Μ': 'M',
    'Ν': 'N', 'Ξ': 'X', 'Ο': 'O', 'Π': 'P', 'Ρ': 'R', 'Σ': 'S',
    'Τ': 'T', 'Υ': 'U', 'Φ': 'F', 'Χ': 'C', 'Ψ': 'Y', 'Ω': 'W',
    # Lowercase Greek to Latin
    'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 'z',
    'η': 'h', 'θ': 'q', 'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm',
    'ν': 'n', 'ξ': 'x', 'ο': 'o', 'π': 'p', 'ρ': 'r', 'σ': 's',
    'τ': 't', 'υ': 'u', 'φ': 'f', 'χ': 'c', 'ψ': 'y', 'ω': 'w',
    # Variants
    'ς': 's',  # final sigma
    'ϑ': 'q',  # theta variant
    'ϕ': 'f',  # phi variant
    'ϖ': 'w',  # omega variant
}

# Special character mappings
# The key issue: ã (0xE3) in Symbol font represents © (copyright)
SYMBOL_SPECIAL_CHARS = {
    'ã': '©',
    '\xe3': '©',  # same as above, different encoding - F601 tripping
}


def decode_symbol_font(text: str) -> str:
    """
    Decode text that was extracted from Symbol font cells.

    When Excel uses Symbol font, ASCII characters appear as Greek letters.
    This function converts them back to Latin characters and handles special
    symbols like the copyright symbol.

    Args:
        text: Text string with Greek letters and Symbol font characters

    Returns:
        Text string with Latin characters and proper symbols restored

    Example:
        >>> decode_symbol_font("ã 2025 Τηε ΜΙΤΡΕ Χορπορατιον.")
        "© 2025 The MITRE Corporation."
    """
    if not text:
        return text

    result = []
    for char in text:
        # First check for special characters (like copyright)
        if char in SYMBOL_SPECIAL_CHARS:
            result.append(SYMBOL_SPECIAL_CHARS[char])
        # Then check for Greek to Latin conversion
        elif char in GREEK_TO_LATIN:
            result.append(GREEK_TO_LATIN[char])
        else:
            # Keep the character as-is if no mapping found
            result.append(char)

    return ''.join(result)


def is_symbol_font(font) -> bool:
    """
    Check if a font is Symbol font.

    Args:
        font: openpyxl Font object or None

    Returns:
        True if the font is Symbol font, False otherwise
    """
    if not font or not font.name:
        return False

    font_name = font.name.lower()
    return 'symbol' in font_name
