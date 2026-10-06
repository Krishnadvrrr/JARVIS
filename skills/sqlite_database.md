# Skill: SQLite Database Architecture & Data Access
keywords: [database, sqlite, sql, schema, tables, queries, persistence, crud, orm]

## 1. Schema Design
- Use primary keys with `INTEGER PRIMARY KEY AUTOINCREMENT` or UUIDs.
- Explicitly enforce constraints: `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`.
- Define foreign keys with `REFERENCES` and enforce `PRAGMA foreign_keys = ON;`.
- Add indices on frequently filtered or joined columns (`CREATE INDEX idx_user_email ON users(email);`).

## 2. Safe Query Execution (Anti-SQL Injection)
- **CRITICAL**: NEVER use f-strings, `%` formatting, or string concatenation to build SQL statements.
- **ALWAYS** use parameterized queries with `?` placeholders:
  ```python
  # SECURE:
  cursor.execute("SELECT * FROM users WHERE email = ? AND status = ?", (email, "active"))
  ```

## 3. Connection Management
- Use `sqlite3.Row` for dictionary-like column access.
- Wrap transactions in `with conn:` context managers so commits and rollbacks happen automatically.
- Safely close cursors and connections upon task completion.
