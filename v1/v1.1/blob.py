# CHANGE: validations moved to utils.py. The DEFAULT value of a BLOB column
# uses validate_value(DATA_TYPE, value) because that value SHOULD be of the
# same type as the column (hexadecimal). The validations inside CHECK that
# ask for a "number of bytes" are NOT of type BLOB (they're a positive
# integer describing a size), so those still use is_valid_positive_integer
# directly instead of validate_value.
from utils import is_valid_identifier, is_valid_positive_integer, validate_value

DATA_TYPE = "BLOB"  # PIECE: the data type this module handles


def generate_blob_column_sql():
    """
    PIECE: BLOB column generator.

    WHAT IT DOES:
        Asks for the column name and its constraints (NOT NULL,
        UNIQUE, DEFAULT in hexadecimal, CHECK on size/type)
        and builds the corresponding SQL fragment.

    WHAT IT RETURNS:
        {"name": <column name>, "sql": <SQL fragment>}
    """

    # PIECE: catalog of constraints available for BLOB columns.
    BLOB_MODEL = {
        "base": "BLOB",
        "constraints": {
            1: {"key": "not_null", "label": "Disallow NULL", "sql": "NOT NULL", "unique": True},
            2: {"key": "unique", "label": "Unique value", "sql": "UNIQUE", "unique": True},
            3: {"key": "default", "label": "Default value (hex)", "sql": "DEFAULT x'{value}'", "unique": True},
            4: {"key": "check", "label": "CHECK condition", "sql": "CHECK({check})", "unique": False}
        }
    }

    # PIECE: catalog of CHECK conditions specific to BLOB
    # (byte size, forced type, hexadecimal comparison).
    BLOB_CHECKS = {
        1: {"label": "Limit maximum size (bytes)", "sql": 'length("{col}") <= {value}'},
        2: {"label": "Limit minimum size (bytes)", "sql": 'length("{col}") >= {value}'},
        3: {"label": "Exact size (bytes)", "sql": 'length("{col}") = {value}'},
        4: {"label": "Disallow empty BLOB", "sql": 'length("{col}") > 0'},
        5: {"label": "Force BLOB type", "sql": 'typeof("{col}") = \'blob\''},
        6: {"label": "Compare with a specific hexadecimal value", "sql": '"{col}" = x\'{value}\''}
    }

    # --- Validate name ---
    while True:
        name = input("Enter the column name: ")
        if is_valid_identifier(name):
            break
        print("⚠️ Invalid name. Use only letters, numbers, and _ (cannot start with a number).")

    column_parts = [name, BLOB_MODEL["base"]]
    used_constraints = set()

    while True:
        print("\n--- Available BLOB constraints ---")
        for num, data in BLOB_MODEL["constraints"].items():
            status = ""
            if data["unique"] and data["key"] in used_constraints:
                status = " [Already applied]"
            print(f"{num}. {data['label']}{status}")

        choice = input("Select an option (ENTER to finish): ")
        if not choice:
            break

        try:
            choice_idx = int(choice)
            constraint = BLOB_MODEL["constraints"][choice_idx]
        except (ValueError, KeyError):
            print("⚠️ Invalid option.")
            continue

        if constraint["unique"] and constraint["key"] in used_constraints:
            print("⚠️ This constraint was already added.")
            continue

        sql_piece = constraint["sql"]

        # DEFAULT HEX
        # CHANGE: validate_value(DATA_TYPE, val) -> since DATA_TYPE="BLOB",
        # it applies the hexadecimal rule, same as before with is_valid_hex.
        if "{value}" in sql_piece and "{check}" not in sql_piece:
            while True:
                val = input("Hexadecimal value (without x''): ")
                if validate_value(DATA_TYPE, val):
                    break
                print("⚠️ Must contain only hexadecimal characters (0-9, A-F).")

            sql_piece = sql_piece.format(value=val)

        # CHECK
        elif "{check}" in sql_piece:
            print("\n--- CHECK validation options ---")
            for num, data in BLOB_CHECKS.items():
                print(f"{num}. {data['label']}")

            try:
                check_idx = int(input("Select an option: "))
                check_template = BLOB_CHECKS[check_idx]["sql"]
            except (ValueError, KeyError):
                print("⚠️ Invalid option.")
                continue

            if "{value}" in check_template:
                if "length" in check_template:
                    # CHANGE: this is a byte count (positive integer),
                    # not a value of type BLOB, so it does NOT use
                    # validate_value here: is_valid_positive_integer
                    # is the correct rule.
                    while True:
                        val = input("Number of bytes: ")
                        if is_valid_positive_integer(val):
                            break
                        print("⚠️ Must be a positive integer.")
                else:
                    # CHANGE: this comparison IS against a BLOB value
                    # (hexadecimal), so it uses validate_value(DATA_TYPE, ...).
                    while True:
                        val = input("Hexadecimal value: ")
                        if validate_value(DATA_TYPE, val):
                            break
                        print("⚠️ Must contain only hexadecimal characters.")

                check_sql = check_template.format(col=name, value=val)
            else:
                check_sql = check_template.format(col=name)

            sql_piece = sql_piece.format(check=check_sql)

        column_parts.append(sql_piece)
        used_constraints.add(constraint["key"])

    final_sql = " ".join(column_parts)
    print(f"\n✅ BLOB definition generated: {final_sql}")

    return {"name": name, "sql": final_sql}


if __name__ == "__main__":
    result = generate_blob_column_sql()
    print(f"Result: {result}")
