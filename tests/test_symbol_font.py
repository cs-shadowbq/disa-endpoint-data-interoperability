"""Tests for Symbol font decoding."""

import pytest

from xls_extractor.symbol_font import decode_symbol_font, is_symbol_font, GREEK_TO_LATIN


class TestSymbolFontDecoding:
    """Test Symbol font decoding utilities."""

    def test_decodes_copyright_symbol(self):
        """Test decoding of copyright symbol from Symbol font."""
        # In Symbol font, 'ã' (0xE3) displays as ©
        result = decode_symbol_font('ã')
        assert result == '©'

    def test_decodes_greek_letters_to_latin(self):
        """Test decoding of Greek letters back to Latin."""
        # Uppercase
        assert decode_symbol_font('Α') == 'A'  # Alpha -> A
        assert decode_symbol_font('Β') == 'B'  # Beta -> B
        assert decode_symbol_font('Γ') == 'G'  # Gamma -> G
        assert decode_symbol_font('Τ') == 'T'  # Tau -> T

        # Lowercase
        assert decode_symbol_font('α') == 'a'  # alpha -> a
        assert decode_symbol_font('β') == 'b'  # beta -> b
        assert decode_symbol_font('η') == 'h'  # eta -> h
        assert decode_symbol_font('ε') == 'e'  # epsilon -> e

    def test_decodes_mitre_corporation(self):
        """Test decoding real-world example from Excel file."""
        # This is the actual text extracted from Symbol font in Excel
        result = decode_symbol_font('ã 2025 Τηε ΜΙΤΡΕ Χορπορατιον.')
        assert result == '© 2025 The MITRE Corporation.'

    def test_decodes_mixed_string(self):
        """Test that all characters in a string are decoded."""
        result = decode_symbol_font('Ηελλο123')
        # Η -> H (Eta), ε -> e (epsilon), λ -> l (lambda), ο -> o (omicron)
        assert result == 'Hello123'

    def test_handles_empty_string(self):
        """Test handling of empty string."""
        assert decode_symbol_font('') == ''
        assert decode_symbol_font(None) == None

    def test_handles_mixed_text(self):
        """Test handling of mixed text with Symbol and regular characters."""

    def test_preserves_unmapped_characters(self):
        """Test that characters without mappings are preserved."""
        # Numbers, punctuation, etc. should pass through unchanged
        result = decode_symbol_font('123 = abc')
        assert '1' in result
        assert '2' in result
        assert '3' in result
        assert '=' in result
        assert ' ' in result

    def test_is_symbol_font_detection(self):
        """Test Symbol font detection."""
        from openpyxl.styles import Font

        # Symbol font
        symbol_font = Font(name='Symbol')
        assert is_symbol_font(symbol_font) is True

        # Regular font
        regular_font = Font(name='Arial')
        assert is_symbol_font(regular_font) is False

        # None font
        assert is_symbol_font(None) is False

        # Font with no name
        no_name_font = Font()
        assert is_symbol_font(no_name_font) is False

    def test_symbol_font_case_insensitive(self):
        """Test that Symbol font detection is case-insensitive."""
        from openpyxl.styles import Font

        assert is_symbol_font(Font(name='Symbol')) is True
        assert is_symbol_font(Font(name='SYMBOL')) is True
        assert is_symbol_font(Font(name='symbol')) is True
