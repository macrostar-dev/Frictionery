# CHANGE: validations are no longer defined here; they now live once in
# utils.py and are imported. Also, DEFAULT and CHECK now use
# validate_value(data_type, value): since this column is of type "INTEGER",
# we pass that type and the central dispatcher decides which rule to validate with.
from utils import is_valid_identifier, validate_value

DATA_TYPE = "INTEGER"  # PIECE: the data type this module handles


def generate_integer_column_sql():
    """
    PIECE: INTEGER column generator.

    WHAT IT DOES:
        Interactively asks for the column name and its
        constraints (NOT NULL, UNIQUE, DEFAULT, CHECK) and
        builds the corresponding SQL fragment for that column.

    WHAT IT RETURNS:
        A dictionary {"name": <column name>, "sql": <SQL fragment>}
        that main.py uses to build the final CREATE TABLE.
    """

    # PIECE: catalog of constraints available for an INTEGER column
    # (NOT NULL, UNIQUE, DEFAULT, CHECK). "unique": True means that
    # constraint can only be applied once per column.
    INTEGER_MODEL = {
        "base": "INTEGER",
        "constraints": {
            1: {"key": "not_null", "label": "Disallow NULL", "sql": "NOT NULL", "unique": True},
            2: {"key": "unique", "label": "Unique value", "sql": "UNIQUE", "unique": True},
            3: {"key": "default", "label": "Default value", "sql": "DEFAULT {value}", "unique": True},
            4: {"key": "check", "label": "CHECK condition", "sql": "CHECK({check})", "unique": False},
        }
    }

    # PIECE: catalog of CHECK conditions specific to INTEGER
    # (numeric comparisons and ranges).
    INTEGER_CHECKS = {
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

    column_parts = [name, INTEGER_MODEL["base"]]
    used_constraints = set()

    while True:
        print("\n--- Available INTEGER constraints ---")
        for num, data in INTEGER_MODEL["constraints"].items():
            status = ""
            if data["unique"] and data["key"] in used_constraints:
                status = " [Already applied]"
            print(f"{num}. {data['label']}{status}")

        choice = input("Select an option (ENTER to finish): ")
        if not choice:
            break

        try:
            choice_idx = int(choice)
            constraint = INTEGER_MODEL["constraints"][choice_idx]
        except (ValueError, KeyError):
            print("⚠️ Invalid option.")
            continue

        if constraint["unique"] and constraint["key"] in used_constraints:
            print("⚠️ This constraint was already added.")
            continue

        sql_piece = constraint["sql"]

        # DEFAULT
        # CHANGE: validated with validate_value(DATA_TYPE, val) -> since
        # DATA_TYPE="INTEGER", it internally applies the same rule as
        # is_valid_integer, but now the decision of "which rule to use"
        # is centralized in utils.py.
        if "{value}" in sql_piece:
            while True:
                val = input("Default value (integer): ")
                if validate_value(DATA_TYPE, val):
                    break
                print("⚠️ Must be a valid integer.")
            sql_piece = sql_piece.format(value=val)

        # CHECK
        elif "{check}" in sql_piece:
            print("\n--- CHECK validation options ---")
            for num, data in INTEGER_CHECKS.items():
                print(f"{num}. {data['label']}")

            try:
                check_idx = int(input("Select an option: "))
                check_template = INTEGER_CHECKS[check_idx]["sql"]
            except (ValueError, KeyError):
                print("⚠️ Invalid option.")
                continue

            # CHANGE: CHECK comparison values must also be INTEGER values
            # (they're compared against an INTEGER column), so they use
            # the same validate_value(DATA_TYPE, ...).
            if "{value}" in check_template:
                while True:
                    val = input("Integer value: ")
                    if validate_value(DATA_TYPE, val):
                        break
                    print("⚠️ Must be a valid integer.")
                check_sql = check_template.format(col=name, value=val)
            else:
                while True:
                    min_val = input("Minimum value: ")
                    max_val = input("Maximum value: ")
                    if validate_value(DATA_TYPE, min_val) and validate_value(DATA_TYPE, max_val):
                        break
                    print("⚠️ Both values must be valid integers.")
                check_sql = check_template.format(col=name, min=min_val, max=max_val)

            sql_piece = sql_piece.format(check=check_sql)

        column_parts.append(sql_piece)
        used_constraints.add(constraint["key"])

    final_sql = " ".join(column_parts)
    print(f"\n✅ Definition generated: {final_sql}")

    # CHANGE: now we return a dictionary with the name and the SQL.
    # This makes main.py work without errors and lets PK/FK find the column.
    return {"name": name, "sql": final_sql}


if __name__ == "__main__":
    result = generate_integer_column_sql()
    print(f"Result for the orchestrator: {result}")
