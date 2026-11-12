"""Customer data validation (system under test for LW#1)."""
import re
from datetime import datetime, date

def validate_code(code):
    """R1: personal code = 11 digits, first digit 1-6, valid checksum (Lithuanian format)."""
    if not isinstance(code, str) or not re.fullmatch(r"[1-6]\d{10}", code):
        return False
    d = [int(c) for c in code]
    s = sum(d[i] * ((i % 9) + 1) for i in range(10)) % 11
    if s == 10:
        s = sum(d[i] * (((i + 2) % 9) + 1) for i in range(10)) % 11
        if s == 10:
            s = 0
    return s != d[10]

def validate_name(name):
    """R2: name is letters only (Unicode), optional single hyphen/space, 1-50 chars."""
    return isinstance(name, str) and 1 <= len(name) <= 50 and \
        re.fullmatch(r"[^\W\d_]+(?:[- ][^\W\d_]+)*", name) is not None

def validate_birth_date(text):
    """R3: date in DD.MM.YYYY format, real calendar date, not in the future."""
    if not isinstance(text, str) or not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", text):
        return False
    try:
        d = datetime.strptime(text, "%d.%m.%Y").date()
    except ValueError:
        return False
    return d <= date.today()

class CustomerDB:
    """R4/R5: stores customers; duplicate codes rejected."""
    def __init__(self):
        self._rows = {}

    def add(self, code, first, last, birth):
        if not (validate_code(code) and validate_name(first)
                and validate_name(last) and validate_birth_date(birth)):
            raise ValueError("invalid customer data")
        if code in self._rows:
            raise KeyError("duplicate customer code")
        self._rows[code] = (first, last, birth)

    def get(self, code):
        return self._rows.get(code)

    def count(self):
        return len(self._rows)

def fits_screen(width, height, max_w=800, max_h=600):
    """R6: window must fit the 800x600 screen."""
    return 0 < width <= max_w and 0 < height <= max_h
