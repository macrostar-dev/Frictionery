# ⌨️ Frictionery - Interactive SQL Architect

> **Prototype Note (v1):** This project is currently a Proof of Concept (PoC). Its primary goal is to validate modular logic, interactive auto-assembly, and strict syntax enforcement for SQLite through the terminal[cite: 1, 4].

**Frictionery** is an interactive CLI tool designed to streamline database architecture and manipulation. It enables developers to structure robust schemas, compose queries, and prepare data payloads via a guided process, completely eliminating manual formatting errors or misspelled SQL keywords.

---

## 🗺️ Project Roadmap

The project is designed to evolve incrementally, solidifying core terminal capabilities before migrating to visual user interfaces and live connected environments:

### 📦 Version 1: The Logic Engine & Console (Current Phase)
The ability to assemble complete SQL commands interactively through terminal prompts[cite: 1, 4]. It is divided into three critical sub-stages:
*   **v1.1 - Schema Definition:** Modeling and strict structuring of table blueprints (`CREATE TABLE`), managing advanced data types and constraints (Implemented).
*   **v1.2 - Query Builder:** An interactive wizard to compose read, filtering, and relationship statements (`SELECT`, `WHERE`, `JOIN`).
*   **v1.3 - Data Manipulation:** A secure engine to generate data insertion and modification statements (`INSERT INTO`, `UPDATE`).

### 🧩 Version 2: Block-Based Constructor
User interface evolution. It transitions the application into a visual, modular layout where complex SQL statements can be assembled using drag-and-drop style building blocks, accelerating workflows without writing code from scratch.

### 🔌 Version 3: Live Connection & Execution
Production environment integration. Enables native connection to real database engines to execute generated SQL statements directly onto `.db` files, unlocking live schema exploration and actual system persistence.

---

## 🏗️ Modular Architecture (v1)

The system is engineered around a segmented architecture to guarantee clean, decoupled, and maintainable code as new features scale out[cite: 1, 3, 4, 6, 7]:

| Module | Responsibility | Key Feature |
| :--- | :--- | :--- |
| **`main.py`** | The Orchestrator | Drives the CLI state machine and compiles the final SQL (`CREATE TABLE`)[cite: 4]. |
| **`utils.py`** | Central Validator | Centralizes regular expressions and hosts the data-type dispatcher (`validate_value`)[cite: 8]. |
| **`inter.py`** | Integer Engine | Manages `INTEGER` columns, numerical boundaries, and `BETWEEN` constraints[cite: 3, 4]. |
| **`real.py`** | Real/Float Engine | Governs `REAL` columns, decimal precision, and floating-point constraints[cite: 4, 6]. |
| **`text.py`** | String Handler | Handles `TEXT` columns, `COLLATE NOCASE` clauses, and character lengths[cite: 4, 7]. |
| **`blob.py`** | Binary Handler | Validates `BLOB` fields, byte sizing, and raw hexadecimal literals[cite: 1, 4]. |
| **`pk.py` / `foreign_key.py`** | Integrity Layer | Coordinates composite Primary and Foreign Key relational rules at the table level[cite: 2, 4, 5]. |

### 🧩 Syntactic Control Flow
The design adheres to low-coupling architectural principles:
1. **`main.py`** initializes execution and queries the user for structural metadata[cite: 4].
2. The specific **Type Engines** (`inter.py`, `text.py`, etc.) map out targeted constraints based on the SQLite standard[cite: 3, 4, 7].
3. **`utils.py`** functions as an intercepting middleware, evaluating formatting rules and blocking malformed entries before passing clean SQL segments back to the orchestrator[cite: 4, 8].

---

## 🛡️ Built-in Prevention Features

*   **Intelligent Auto-Assembly:** The engine automatically manages commas, parentheses, clauses, and structural SQL syntax in the background using data models[cite: 1, 3, 4, 6, 7]. Users focus strictly on parameters; the tool ensures perfect syntactic output[cite: 4].
*   **Active Input Guardrail (Strict Blocking):** The terminal operates as an active filter layer. Utilizing a centralized registry dispatcher (`validate_value`)[cite: 8], the application catches and rejects invalid entries instantly (e.g., rejecting plain text inside an `INTEGER` column or non-hex strings inside a `BLOB` constraint)[cite: 1, 3, 8], blocking them before they can compromise the SQL engine logic.
*   **Identifier Validation:** Regular expression filters (`is_valid_identifier`) systematically intercept illegal tokens, spaces, or numeric prefixes in table names and column attributes[cite: 4, 8].
*   **State Conflict Prevention:** An internal tracking system (`used_constraints`) isolates unique constraints, making it impossible to assign conflicting rules (such as two `DEFAULT` values)[cite: 1, 3, 6, 7] or multiple `PRIMARY KEY` table declarations[cite: 5].
*   **Sanitization Layer:** Automatic escaping of single quotes (`escape_quotes`) protects string literals, ensuring generated statements remain structurally sound against syntax injection or breakage[cite: 7, 8].

---

## 🛠️ Technical Usage (v1)

1. **Clone the repository and spin up the orchestrator:**
   ```bash
   python main.py
1. **Clonar el repositorio e iniciar el orquestador:**
   ```bash
   python main.py
