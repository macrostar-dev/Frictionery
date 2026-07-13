"""
=========================================================
 utils.py
=========================================================
PIECE: Shared validation utilities.

WHAT IT DOES:
    Centralizes the validation functions (regex) that used to
    be copy-pasted in blob.py, inter.py, real.py, and text.py.
    Any adjustment to a validation rule is made once here and
    is reflected across all modules.

WHY IT WAS ADDED:
    Before, is_valid_identifier() and is_valid_integer() existed
    duplicated in 4 different files. If a regex ever needed a fix
    (e.g. to accept accented characters), you had to remember to
    change it in 4 places. Now it's changed in one place and all
    modules stay in sync.
=========================================================
"""

import re


def is_valid_identifier(name):
    """
    Validates a SQL identifier: must start with a letter or
    underscore (_), and may only contain letters, digits, or
    underscores. Used for both column names and the table name.
    """
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name) is not None


def is_valid_integer(value):
    """
    Validates an integer (signed).
    Used for values that can be negative or positive, e.g. a
    DEFAULT value for an INTEGER column.
    """
    return re.match(r'^-?\d+$', value) is not None


def is_valid_positive_integer(value):
    """
    Validates a positive integer (unsigned). Useful for byte
    sizes, text lengths, etc., where a negative number makes
    no sense.
    """
    return re.match(r'^\d+$', value) is not None


def is_valid_real(value):
    """
    Validates a REAL number: integer or decimal, positive or
    negative. E.g.: 10, -3, 4.5, -0.25
    """
    return re.match(r'^-?\d+(\.\d+)?$', value) is not None


def is_valid_hex(value):
    """
    Validates that the value is a valid hexadecimal string
    (0-9, A-F, a-f). Used for BLOB values in x'...' format.
    """
    return re.match(r'^[0-9A-Fa-f]+$', value) is not None


def escape_quotes(text):
    """
    Escapes single quotes by doubling them, so a text value
    containing quotes doesn't break the generated SQL syntax.
    E.g.: O'Brien -> O''Brien
    """
    return text.replace("'", "''")


# =========================================================
# PIECE: Central validation dispatcher by data type.
# =========================================================
# WHAT IT DOES:
#   Given the column type (INTEGER, TEXT, REAL, BLOB) and a
#   value entered by the user, it automatically decides which
#   validation rule to apply and returns True/False.
#
# WHY IT WAS ADDED:
#   Before, each module (inter.py, text.py, real.py, blob.py)
#   decided "by hand" which validation function to call
#   (is_valid_integer, is_valid_real, is_valid_hex...). That
#   decision now lives in a single place: if a new data type is
#   added in the future, or the rule for an existing type
#   changes, it's adjusted here and all modules stay
#   automatically in sync.
#
# HOW TO USE IT:
#   validate_value("INTEGER", "42")   -> True
#   validate_value("TEXT", "hello")   -> True (TEXT accepts any text)
#   validate_value("REAL", "3.14")    -> True
#   validate_value("BLOB", "A1F")     -> True (hexadecimal)
#   validate_value("BLOB", "hello")   -> False
# =========================================================

# Registry type -> validator function. Adding a new type is
# as simple as adding one line here.
_TYPE_VALIDATORS = {
    "INTEGER": is_valid_integer,
    "REAL": is_valid_real,
    "BLOB": is_valid_hex,
    "TEXT": lambda value: True,  # TEXT accepts any string (escaping is handled separately)
}


def validate_value(data_type, value):
    """
    Validates that 'value' is consistent with the column type 'data_type'.

    data_type: "INTEGER" | "TEXT" | "REAL" | "BLOB" (case-insensitive)
    value:     the string entered by the user to validate.

    Returns True if the value is valid for that type, False
    otherwise, and also False if 'data_type' is not a recognized type.
    """
    validator = _TYPE_VALIDATORS.get(data_type.upper())
    if validator is None:
        return False
    return validator(value)
