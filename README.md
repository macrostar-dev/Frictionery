# ⌨️ Frictionery - Interactive SQL Architect

> [!IMPORTANT]
> **PROTOTYPE NOTE (v1):** This project is currently a **Proof of Concept**. 
> Its primary goal is to validate modular logic and syntax generation for **SQLite**.

Tablify is a personal project designed to streamline the creation of database tables through an interactive CLI. It allows users with basic SQL knowledge to generate robust, professional schemas without fighting manual syntax errors.

---

## 🚀 Version 1: The Logic Engine
The first version (v1) focuses on **Business Logic** and **Syntax Integrity**. It doesn't just concatenate strings; it validates every step of the modeling process.

### 🏗️ Modular Architecture
The system is built on a **modular backbone**, separating concerns to ensure clean code and easy maintenance:

| Module | Responsibility | Key Feature |
| :--- | :--- | :--- |
| `main.py` | **The Orchestrator** | Assembles the final `CREATE TABLE` statement. |
| `inter.py` / `real.py` | **Numeric Engine** | Validates ranges and `CHECK` constraints. |
| `text.py` | **String Handler** | Manages `COLLATE NOCASE` and quote escaping. |
| `blob.py` | **Binary Handler** | Validates Hexadecimal literals for raw data. |
| `pk.py` / `fk.py` | **Integrity Layer** | Manages Primary Keys and Foreign Key relations. |

### 🛡️ Built-in Safety Features
* **Identifier Validation:** Uses Regex to block illegal characters in table/column names.
* **Conflict Prevention:** A tracking system prevents assigning duplicate constraints (e.g., two `DEFAULT` values).
* **Type Shield:** Rejects invalid inputs (e.g., text in an `INTEGER` field) before generating code.
* **SQL Injection Prevention:** Automatic escaping for single quotes in text fields.

---

## 🗺️ Project Roadmap

### 📦 v1: Logic Engine (Current)
* Full SQLite syntax support.
* Interactive CLI for step-by-step modeling.
* Advanced constraint management (`UNIQUE`, `NOT NULL`, `DEFAULT`).

### 🔌 v2: Connectivity & Execution
* **Direct DB Connection:** Execute generated code directly into `.db` files.
* **Query Builder:** Assistance for `SELECT`, `INSERT`, and `UPDATE` operations.

### 📊 v3: Data Visualizer & Excel
* **Table Browser:** View your data directly in the console.
* **Excel Bridge:** Export full databases to Excel and import mass data from spreadsheets.

---

## 🛠️ Usage
1. Run the orchestrator: `python main.py`
2. Follow the interactive prompts to define your columns.
3. Copy the resulting SQL command and use it in your favorite DB manager.

---
*Developed as a personal tool to bridge the gap between basic DB knowledge and professional SQL execution.*
