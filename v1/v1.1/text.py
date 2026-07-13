# CHANGE: validations and escape_quotes moved to utils.py. DEFAULT uses
# validate_value(DATA_TYPE, value) for consistency with the other modules
# (although for TEXT it always returns True, since any text is valid;
# what actually protects the syntax is escape_quotes). The length in
# CHECK is NOT of type TEXT (it's a positive integer), so it still uses
# is_valid_positive_integer directly.
from utils import is_valid_identifier, is_valid_positive_integer, escape_quotes, validate_value

DATA_TYPE = "TEXT"  # PIECE: the data type this module handles


def generate_text_column_sql():
    """
    PIECE: TEXT column generator.

    WHAT IT DOES:
        Asks for the column name and its constraints (NOT NULL,
        UNIQUE, DEFAULT, COLLATE NOCASE, length CHECK) and
        builds the corresponding SQL fragment. Escapes single
        quotes in DEFAULT values so they don't break the SQL.

    WHAT IT RETURNS:
        {"name": <column name>, "sql": <SQL fragment>}
    """

    # PIECE: catalog of constraints available for TEXT columns.
    TEXT_MODEL = {
        "base": "TEXT",
        "constraints": {
            1: {"key": "not_null", "label": "Disallow NULL", "sql": "NOT NULL", "unique": True},
            2: {"key": "unique", "label": "Unique value", "sql": "UNIQUE", "unique": True},
            3: {"key": "default", "label": "Default value", "sql": "DEFAULT '{value}'", "unique": True},
            4: {"key": "collate", "label": "Case-insensitive comparison (NOCASE)", "sql": "COLLATE NOCASE", "unique": True},
            5: {"key": "check", "label": "CHECK condition", "sql": "CHECK({check})", "unique": False},
        }
    }

    # PIECE: catalog of CHECK conditions specific to TEXT (length).
    TEXT_CHECKS = {
        1: {"label": "Minimum length", "sql": 'LENGTH("{col}") >= {value}'},
        2: {"label": "Maximum length", "sql": 'LENGTH("{col}") <= {value}'},
        3: {"label": "Exact length", "sql": 'LENGTH("{col}") = {value}'},
    }

    # --- Validate name ---
    while True:
        name = input("Enter the column name: ")
        if is_valid_identifier(name):
            break
        print("⚠️ Invalid name. Use only letters, numbers, and _ (cannot start with a number).")

    column_parts = [name, TEXT_MODEL["base"]]
    used_constraints = set()

    while True:
        print("\n--- Available TEXT constraints ---")
        for num, data in TEXT_MODEL["constraints"].items():
            status = ""
            if data["unique"] and data["key"] in used_constraints:
                status = " [Already applied]"
            print(f"{num}. {data['label']}{status}")

        choice = input("Select an option (ENTER to finish): ")
        if not choice:
            break

        try:
            choice_idx = int(choice)
            constraint = TEXT_MODEL["constraints"][choice_idx]
        except (ValueError, KeyError):
            print("⚠️ Invalid option.")
            continue

        if constraint["unique"] and constraint["key"] in used_constraints:
            print("⚠️ This constraint was already added.")
            continue

        sql_piece = constraint["sql"]

        # DEFAULT
        # CHANGE: passed through validate_value(DATA_TYPE, val) for
        # consistency (TEXT always validates True), then single quotes
        # are escaped so they don't break the SQL syntax.
        if "{value}" in sql_piece:
            val = input("Default text: ")
            if validate_value(DATA_TYPE, val):
                val = escape_quotes(val)
                sql_piece = sql_piece.format(value=val)

        # CHECK LENGTH
        elif "{check}" in sql_piece:
            print("\n--- Text validation options (LENGTH) ---")
            for num, data in TEXT_CHECKS.items():
                print(f"{num}. {data['label']}")

            try:
                check_idx = int(input("Select an option: "))
                check_template = TEXT_CHECKS[check_idx]["sql"]
            except (ValueError, KeyError):
                print("⚠️ Invalid option.")
                continue

            # CHANGE: character count is a positive integer, not a value
            # of type TEXT, so it uses is_valid_positive_integer directly
            # instead of validate_value.
            while True:
                val = input("Number of characters: ")
                if is_valid_positive_integer(val):
                    break
                print("⚠️ Must be a positive integer.")

            check_sql = check_template.format(col=name, value=val)
            sql_piece = sql_piece.format(check=check_sql)

        column_parts.append(sql_piece)
        used_constraints.add(constraint["key"])

    final_sql = " ".join(column_parts)
    print(f"\n✅ TEXT definition generated: {final_sql}")

    # Return the dictionary so main.py doesn't fail and PK/FK can find the column
    return {"name": name, "sql": final_sql}


if __name__ == "__main__":
    result = generate_text_column_sql()
    print(f"Result: {result}")
