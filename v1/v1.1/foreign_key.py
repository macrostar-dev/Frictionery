def add_foreign_keys(columns):
    """
    PIECE: FOREIGN KEY table-level constraint adder.

    WHAT IT DOES:
        Lets the user mark an already-existing column as a
        FOREIGN KEY, indicating the table and column it
        references, e.g.:
        FOREIGN KEY(user_id) REFERENCES users(id)
        Can be repeated to add several different FKs
        (each on a different column).

    CHANGE:
        A validation was added to prevent declaring the same
        column as a FOREIGN KEY twice (before, the same column
        could be added with different or repeated references,
        generating conflicts in the final SQL).

    Receives the list of columns:
    [
        {"name": "user_id", "sql": "user_id INTEGER"},
        {"name": "email", "sql": "email TEXT"}
    ]
    """

    if not columns:
        print("You must create columns first.")
        return columns

    while True:
        print("\nAvailable columns for FOREIGN KEY:")
        for col in columns:
            print(f"- {col['name']}")

        fk_column = input(
            "\nEnter the column that will be a FOREIGN KEY (Enter to finish): "
        )

        # If Enter is pressed -> finish
        if fk_column == "":
            break

        valid_names = [col["name"] for col in columns]

        if fk_column not in valid_names:
            print("Invalid column.")
            continue

        # CHANGE: prevents declaring the same column as an FK more than once.
        already_fk = any(
            col["name"] == "__foreign_key__" and col["sql"].startswith(f"FOREIGN KEY({fk_column})")
            for col in columns
        )
        if already_fk:
            print(f"⚠️ Column '{fk_column}' already has a FOREIGN KEY defined.")
            continue

        reference_table = input("Enter the referenced table: ")
        reference_column = input("Enter the referenced column: ")

        if reference_table == "" or reference_column == "":
            print("Invalid reference.")
            continue

        fk_line = f"FOREIGN KEY({fk_column}) REFERENCES {reference_table}({reference_column})"

        columns.append({
            "name": "__foreign_key__",
            "sql": fk_line
        })

        print("FOREIGN KEY added successfully.")

    return columns
