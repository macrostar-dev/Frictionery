# CHANGE: validations moved to utils.py. Also, DEFAULT and CHECK now use
# validate_value(data_type, value): the central dispatcher decides that,
# since DATA_TYPE="REAL", it must apply the real-number rule.
from utils import is_valid_identifier, validate_value

DATA_TYPE = "REAL"  # PIECE: the data type this module handles


def generate_real_column_sql():
    """
    PIECE: REAL column generator.

    WHAT IT DOES:
        Asks for the column name and its constraints (NOT NULL,
        UNIQUE, DEFAULT, CHECK) for decimal/floating-point
        numbers, and builds the corresponding SQL fragment.

    WHAT IT RETURNS:
        {"name": <column name>, "sql": <SQL fragment>}
    """

    # PIECE: catalog of constraints available for REAL columns.
    REAL_MODEL = {
        "base": "REAL",
        "constraints": {
            1: {"key": "not_null", "label": "Disallow NULL", "sql": "NOT NULL", "unique": True},
            2: {"key": "unique", "label": "Unique value", "sql": "UNIQUE", "unique": True},
            3: {"key": "default", "label": "Default value", "sql": "DEFAULT {value}", "unique": True},
            4: {"key": "check", "label": "CHECK condition", "sql": "CHECK({check})", "unique": False},
        }
    }

    # PIECE: catalog of CHECK conditions specific to REAL.
    REAL_CHECKS = {
        1: {"label": "Greater than", "sql": '"{col}" > {value}'},
        2: {"label": "Less than", "sql": '"{col}" < {value}'},
        3: {"label": "Between two values", "sql": '"{col}" BETWEEN {min} AND {max}'},
    }

    # --- Validate name ---
    while True:
        name = input("Enter the column name: ")
        if is_valid_identifier(name):
            break
        print("⚠️ Invalid name. Use only letters, numbers, and _ (cannot start with a number).")

    column_parts = [name, REAL_MODEL["base"]]
    used_constraints = set()

    while True:
        print("\n--- Available REAL constraints ---")
        for num, data in REAL_MODEL["constraints"].items():
            status = ""
            if data["unique"] and data["key"] in used_constraints:
                status = " [Already applied]"
            print(f"{num}. {data['label']}{status}")

        choice = input("Select an option (ENTER to finish): ")
        if not choice:
            break

        try:
            choice_idx = int(choice)
            constraint = REAL_MODEL["constraints"][choice_idx]
        except (ValueError, KeyError):
            print("⚠️ Invalid option.")
            continue

        if constraint["unique"] and constraint["key"] in used_constraints:
            print("⚠️ This constraint was already added.")
            continue

        sql_piece = constraint["sql"]

        # DEFAULT
        # CHANGE: validate_value(DATA_TYPE, val) replaces the direct call
        # to is_valid_real; the column's type (REAL) decides the rule.
        if "{value}" in sql_piece and "{check}" not in sql_piece:
            while True:
                val = input("Default value (e.g. 0.0): ")
                if validate_value(DATA_TYPE, val):
                    break
                print("⚠️ Must be a valid number (e.g. 10, -3, 4.5).")

            sql_piece = sql_piece.format(value=val)

        # CHECK
        elif "{check}" in sql_piece:
            print("\n--- CHECK validation options (REAL) ---")
            for num, data in REAL_CHECKS.items():
                print(f"{num}. {data['label']}")

            try:
                check_idx = int(input("Select the range option: "))
                check_template = REAL_CHECKS[check_idx]["sql"]
            except (ValueError, KeyError):
                print("⚠️ Invalid option.")
                continue

            # CHANGE: CHECK comparison values are also validated as REAL
            # through validate_value(DATA_TYPE, ...).
            if "{value}" in check_template:
                while True:
                    val = input("Value: ")
                    if validate_value(DATA_TYPE, val):
                        break
                    print("⚠️ Must be a valid number.")

                check_sql = check_template.format(col=name, value=val)

            else:
                while True:
                    min_val = input("Minimum value: ")
                    max_val = input("Maximum value: ")
                    if validate_value(DATA_TYPE, min_val) and validate_value(DATA_TYPE, max_val):
                        break
                    print("⚠️ Both values must be valid numbers.")

                check_sql = check_template.format(col=name, min=min_val, max=max_val)

            sql_piece = sql_piece.format(check=check_sql)

        column_parts.append(sql_piece)
        used_constraints.add(constraint["key"])

    final_sql = " ".join(column_parts)
    print(f"\n✅ REAL definition generated: {final_sql}")

    return {"name": name, "sql": final_sql}


if __name__ == "__main__":
    result = generate_real_column_sql()
    print(f"Result: {result}")
