"""
=========================================================
 main.py
=========================================================
PIECE: Main orchestrator / CREATE TABLE assembler.

WHAT IT DOES:
    1. Asks for the table name.
    2. Shows a menu with the available column types
       (INTEGER, TEXT, BLOB, REAL) and the table-level
       constraint options (PRIMARY KEY, FOREIGN KEY).
    3. For each normal column, it calls the corresponding
       generator (inter.py, text.py, blob.py, real.py), which
       returns {"name": ..., "sql": ...}, and adds it to the
       `columns` list.
    4. For PRIMARY KEY / FOREIGN KEY, it delegates to
       pk.py / foreign_key.py, which modify `columns` directly
       (they add a special entry with the SQL fragment already built).
    5. Finally, it concatenates all the SQL fragments and builds
       the complete CREATE TABLE.

    This module does NOT connect to any database: it only builds
    the SQL command text so it can be used wherever needed.
=========================================================
"""

from blob import generate_blob_column_sql
from inter import generate_integer_column_sql
from real import generate_real_column_sql
from text import generate_text_column_sql
from pk import add_primary_keys
from foreign_key import add_foreign_keys
from utils import is_valid_identifier  # CHANGE: to validate the table name

# PIECE: menu of available column types / table-level constraints.
column_options = {
    1: {"name": "INTEGER", "function": generate_integer_column_sql},
    2: {"name": "TEXT", "function": generate_text_column_sql},
    3: {"name": "BLOB", "function": generate_blob_column_sql},
    4: {"name": "REAL", "function": generate_real_column_sql},
    5: {"name": "PRIMARY_KEY", "function": add_primary_keys},
    6: {"name": "FOREIGN_KEY", "function": add_foreign_keys},
}

# CHANGE: the table name is now validated the same way as a column name
# (before, any text was accepted, even with spaces or symbols, which
# generated an invalid CREATE TABLE).
while True:
    table_name = input("Enter the table name: ")
    if is_valid_identifier(table_name):
        break
    print("⚠️ Invalid table name. Use only letters, numbers, and _ (cannot start with a number).")

# List that will store dictionaries {"name": "...", "sql": "..."}
columns = []

while True:
    print("\nSelect the column type (Enter to finish):")

    for num, data in column_options.items():
        print(f"{num}. {data['name']}")

    option_input = input("Option: ")

    if option_input == "":
        break

    if not option_input.isdigit():
        print("⚠️ Invalid option.")
        continue

    option_selection = int(option_input)

    if option_selection not in column_options:
        print("⚠️ Option does not exist.")
        continue

    # PIECE: PRIMARY KEY / FOREIGN KEY are not "column types" but
    # table-level constraints; they modify `columns` directly and
    # don't return a new dictionary, which is why they're handled separately.
    if option_selection in [5, 6]:
        column_options[option_selection]["function"](columns)
        continue

    # PIECE: normal column types (INTEGER/TEXT/BLOB/REAL),
    # each one returns {"name": ..., "sql": ...}.
    result_dict = column_options[option_selection]["function"]()

    if not isinstance(result_dict, dict) or "name" not in result_dict or "sql" not in result_dict:
        print("⚠️ Error: the function did not return the expected format.")
        continue

    # CHANGE: validates that the column name is not repeated.
    # Before, two columns could be created with the same name and
    # the generated CREATE TABLE would be invalid.
    existing_names = [col["name"] for col in columns]
    if result_dict["name"] in existing_names:
        print(f"⚠️ A column named '{result_dict['name']}' already exists. "
              f"It was not added to avoid an invalid CREATE TABLE.")
        continue

    columns.append(result_dict)

# PIECE: final construction of the CREATE TABLE, joining all the
# column SQL fragments + table-level constraints (PK/FK).
if not columns:
    print("\n❌ No columns were added. The table could not be generated.")
else:
    body = ",\n    ".join(col["sql"] for col in columns)
    sql_command = f"CREATE TABLE {table_name} (\n    {body}\n);"

    print("\n" + "="*30)
    print("🚀 GENERATED SQL STATEMENT:")
    print("="*30)
    print(sql_command)
