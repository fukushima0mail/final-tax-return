import sqlite3

def init_db():
    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS account_titles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category SMALLINT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            date TEXT NOT NULL,
            debit_account_id INTEGER NOT NULL,
            credit_account_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            FOREIGN KEY(debit_account_id) REFERENCES account_titles(id),
            FOREIGN KEY(credit_account_id) REFERENCES account_titles(id)
        )
    ''')

    conn.commit()
    conn.close()
