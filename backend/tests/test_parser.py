# backend/tests/test_parser.py
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pytest
from ai.resume_parser import ResumeParser
from core.exceptions import InvalidFileTypeError, FileTooLargeError


@pytest.fixture
def parser():
    return ResumeParser()


def test_parser_initialization(parser):
    assert parser.allowed_extensions == [".pdf", ".doc", ".docx"]
    assert parser.max_size_bytes == 5 * 1024 * 1024


def test_invalid_file_type(parser, tmp_path):
    fake_file = tmp_path / "resume.txt"
    fake_file.write_text("This is not a resume")

    with pytest.raises(InvalidFileTypeError):
        parser.parse(str(fake_file))


def test_file_not_found(parser):
    with pytest.raises(FileNotFoundError):
        parser.parse("nonexistent_file.pdf")


def test_sanitize_removes_null_bytes(parser):
    dirty_text = "Hello\x00World\x01Test"
    clean = parser._sanitize(dirty_text)
    assert "\x00" not in clean
    assert "\x01" not in clean


def test_sanitize_empty_text(parser):
    assert parser._sanitize("") == ""
    assert parser._sanitize(None) == ""


def test_sanitize_normalizes_whitespace(parser):
    messy = "Hello    World\t\tTest"
    clean = parser._sanitize(messy)
    assert "    " not in clean


if __name__ == "__main__":
    pytest.main([__file__, "-v"])