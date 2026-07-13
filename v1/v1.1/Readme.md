# ⌨️ Frictionery v1.1 - Deep-Dive Technical Blueprint

> **Current Release (v1.1):** This document provides an exhaustive technical breakdown of the structural engine. Version 1.1 focuses entirely on automated, bulletproof schema generation (`CREATE TABLE`), processing column constraints, and executing active terminal-level input validation[cite: 1, 4, 8].

---

## 🛠️ Detailed Architectural Breakdown: How the Engine Works

The architecture is explicitly split into decoupled responsibilities to enforce the **Single Responsibility Principle**[cite: 1, 3, 4, 6, 7]. Below is the microscopic breakdown of how your files interact:

### 1. The Core Orchestrator (`main.py`)
`main.py` serves as the centralized state machine and execution manager[cite: 4].
* **Table Identification:** It captures the initial table name and subjects it to lexical evaluation[cite: 4].
* **The Option Dispatcher:** It exposes a unified loop mapped to a dictionary (`column_options`)[cite: 4]. This dictionary links numeric selections directly to the execution memory addresses of specific sub-modules[cite: 4].
* **State Preservation:** It maintains a local list called `columns` which dynamically appends structured dictionaries containing the precise metadata (`{"name": ..., "sql": ...}`) returned by the type modules[cite: 3, 4, 6, 7].
* **Duplicate Detection:** Before committing a new column to the schema array, `main.py` extracts all strings from the `"name"` keys and cross-references them[cite: 4]. If a collision is found, it drops the entry to prevent SQLite structural corruption[cite: 4].
* **Compilation Block:** Once an empty line breaks the collection loop, it iterates through the compiled lines, joins them via `,\n    `, injects them into the `CREATE TABLE {table_name} (\n    {body}\n);` template, and flushes the clean string to the terminal[cite: 4].

### 2. The Shared Validator Layer (`utils.py`)
`utils.py` is the defensive middleware of the entire engine, eradicating code duplication by centralizing regex parsers and typing constraints[cite: 8].
* **Lexical Validation (`is_valid_identifier`):** Enforces strict database naming conventions using the regular expression `^[A-Za-z_][A-Za-z0-9_]*$`[cite: 8]. This blocks spaces, operators, and illegal numeric prefixes[cite: 4, 8].
* **Granular Numeric Controls:** Features specialized evaluation tracks: `is_valid_integer` (permitting negative signs for signed standard defaults)[cite: 8] and `is_valid_positive_integer` (strictly unsigned strings, specifically tailored for byte/character sizes)[cite: 1, 7, 8].
* **The Central Dispatcher (`validate_value`):** Instead of individual modules deciding how to process an evaluation, they call `validate_value(data_type, value)`[cite: 1, 3, 6, 8]. This function looks up the database type in an internal register dictionary (`_TYPE_VALIDATORS`), executing the mapped lambda expression or validation function instantly[cite: 8].

### 3. The Specialized Data-Type Processors
Each data-type file runs an isolated loop that models attributes through a tracking configuration (`used_constraints`) to enforce single-assignment parameters[cite: 1, 3, 6, 7].

* **`inter.py` (Integer Engine):** Manages `INTEGER` storage allocation[cite: 3, 4]. Default inputs are verified against `is_valid_integer` via the registry[cite: 3, 8]. For `CHECK` generation, it handles basic inequality limits (`>`, `<`) or maps continuous evaluation thresholds using the `BETWEEN {min} AND {max}` template[cite: 3].
* **`real.py` (Real/Float Engine):** Handles precision floating-point syntax[cite: 4, 6]. It forces decimal tracking structures using the `is_valid_real` regex (`^-?\d+(\.\d+)?$`)[cite: 6, 8]. This allows the input of whole integers or standard fractional values while blocking alphanumeric noise[cite: 6, 8].
* **`text.py` (Text Engine):** Configures character arrays and string formatting[cite: 4, 7]. It includes specific SQLite optimizations like `COLLATE NOCASE` for case-insensitive indexing[cite: 7]. It uses `escape_quotes` to intercept strings and double single-quotes (`text.replace("'", "''")`) to ensure literal text entries do not prematurely break the SQL sequence string[cite: 7, 8].
* **`blob.py` (Binary Engine):** Processes raw hex-literals and binary mapping descriptors[cite: 1, 4]. It strictly forces hex values using `is_valid_hex` (`^[0-9A-Fa-f]+$`)[cite: 1, 8]. For advanced checks, it builds conditions checking size parameters directly via SQLite functions (`length("{col}")`) or data validation tests (`typeof("{col}") = 'blob'`)[cite: 1].

### 4. The Structural Integrity Layer (`pk.py` & `foreign_key.py`)
These files intercept the structural state to set up global table-level safety guards[cite: 2, 5].
* **`pk.py` (Primary Key Compiler):** Allows combining several attributes into a composite primary identifier (`PRIMARY KEY(id, code)`)[cite: 5]. It contains a critical bug-prevention check: if an entry containing the special `__primary_key__` identifier already exists in the column stack, it blocks execution, preventing SQLite from throwing multiple primary key runtime failures[cite: 5].
* **`foreign_key.py` (Foreign Key Mapper):** Collects local column names, confirms they exist in the current schema list, and captures external target entities to map reference rows (`FOREIGN KEY(col) REFERENCES table(col)`)[cite: 2]. It prevents data collision by blocking the mapping of multiple foreign references onto the exact same column element[cite: 2].

---
### 🔄 Data Lifecycle & Input Validation Flow

The diagram below illustrates the exact chronological execution path and active interception mechanism when a user attempts to apply a constraint (e.g., a `DEFAULT` value) to a column:

```text
 ┌────────────────────────────────────────────────────────┐
 │                   [User Type Input]                    │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │        inter.py captures input data string             │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │  utils.py: validate_value("INTEGER", input) dispatcher  │
 └───────────────────────────┬────────────────────────────┘
                             │
              Is the regex signature valid?
                             │
              ├── ❌ NO ────┴──► [ BLOCK & LOOP BACK ]
              │                  CLI rejects input instantly.
              │                  Prevents malformed SQL generation.
              │
              └──  YES ───┬────► [ PASS & FORMAT ]
                          │      Data advances to compilation.
                          │
                          ▼
 ┌────────────────────────────────────────────────────────┐
 │    inter.py wraps value into model: "DEFAULT {value}"  │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │       main.py appends dictionary to columns array      │
 └────────────────────────────────────────────────────────┘



1. **Capture:** The user chooses option `1` (`INTEGER`) in `main.py`[cite: 4], triggering the loop inside `inter.py`[cite: 3, 4].
2. **Constraint Choice:** The user chooses option `3` to append a `Default value`[cite: 3].
3. **Active Interception (The Guardrail):** The system prompts for the value[cite: 3]. If the user inputs `4.5` or `abc`, `inter.py` passes this string down to `utils.py` via `validate_value("INTEGER", val)`[cite: 3, 8].
4. **Active Blocking:** `utils.py` evaluates the string against `is_valid_integer`[cite: 8]. Since it fails the integer signature check, it returns `False`[cite: 8]. `inter.py` traps this return, throws a warning (`⚠️ Must be a valid integer.`), blocks the compilation process, and refuses to let the loop proceed until a clean string is provided[cite: 3].
5. **Auto-Assembly:** Once a valid input (like `42`) is provided, `utils.py` returns `True`[cite: 3, 8], the module formats the string into `"DEFAULT 42"`, and appends it to the column definition array automatically[cite: 3].

---

## 💎 Design Architectural Merits Summarized

By presenting your project with this layout, you are highlighting the implementation of professional architectural choices:
* **True Separation of Concerns:** Changing how integers are handled will never break the logic for processing binary large objects (`BLOB` strings)[cite: 1, 3].
* **Centralized Code Modification:** If you ever need to support signed hexadecimal characters or custom text parameters, you only need to modify one single utility dictionary inside `utils.py` instead of tracking strings across 4 isolated scripts[cite: 8].
* **Memory Integrity:** Using an internal tracking set (`used_constraints`) ensures that logic errors cannot be compiled into the final SQL string output[cite: 1, 3, 4, 6, 7].
