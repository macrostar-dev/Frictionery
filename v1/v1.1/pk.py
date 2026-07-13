def add_primary_keys(columns):
    """
    PIECE: PRIMARY KEY table-level constraint adder.

    WHAT IT DOES:
        Lets the user choose one or more already-created columns
        to form the table's composite PRIMARY KEY, e.g.:
        PRIMARY KEY(id, code).

    CHANGE (bug fixed):
        Before, this function could be run multiple times and
        several "PRIMARY KEY(...)" lines would be added to the
        CREATE TABLE, which SQLite rejects (a table can only have
        ONE table-level primary key). Now, if a PRIMARY KEY
        already exists among the columns, a warning is shown and
        another one cannot be added; you need to run it again and
        pick the correct columns if you want to change it.

    Receives the list of columns in the format:
    [
        {"name": "id", "sql": "id INTEGER"},
        {"name": "email", "sql": "email TEXT"}
    ]
    """

    if not columns:
        print("You must create columns first.")
        return columns

    # CHANGE: check for an already-existing PRIMARY KEY in the table.
    if any(col["name"] == "__primary_key__" for col in columns):
        print("⚠️ This table already has a PRIMARY KEY defined. "
              "SQLite only allows one PRIMARY KEY per table.")
        return columns

    while True:
        print("\nAvailable columns:")
        for col in columns:
            print(f"- {col['name']}")

        pk_input = input(
            "\nEnter columns for PRIMARY KEY separated by commas (Enter to finish): "
        )

        # If Enter is pressed without typing anything -> finish
        if pk_input == "":
            break

        pk_columns = [col.strip() for col in pk_input.split(",")]

        # Validate existing names
        valid_names = [col["name"] for col in columns]
        selected = [name for name in pk_columns if name in valid_names]

        if not selected:
            print("No valid columns.")
            continue

        pk_line = f"PRIMARY KEY({', '.join(selected)})"

        columns.append({
            "name": "__primary_key__",
            "sql": pk_line
        })

        print("PRIMARY KEY added successfully.")
        # CHANGE: since the only allowed PRIMARY KEY was just added,
        # exit the loop instead of continuing to prompt.
        break

    return columns
