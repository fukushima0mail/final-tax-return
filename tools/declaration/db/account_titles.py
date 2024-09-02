from .connection import get_db_connection

def create_account_titles_table():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS account_titles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT NOT NULL,
            name TEXT NOT NULL,
            category SMALLINT NOT NULL,
            borrowing_type INTEGER DEFAULT 1,
            allocation INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_account(account_id, name, category, borrowing_type, allocation):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO account_titles (account_id, name, category, borrowing_type, allocation)
        VALUES (?, ?, ?, ?, ?)
    ''', (account_id, name, category, borrowing_type, allocation))
    conn.commit()
    conn.close()

def get_all_accounts():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM account_titles')
    rows = c.fetchall()
    conn.close()
    return rows

def get_account_names():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT name FROM account_titles')
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]

def update_account(account_id, name, category, borrowing_type, allocation):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE account_titles
        SET name = ?, category = ?, borrowing_type = ?, allocation = ?
        WHERE account_id = ?
    ''', (name, category, borrowing_type, allocation, account_id))
    conn.commit()
    conn.close()

def delete_account(account_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM account_titles WHERE account_id = ?', (account_id,))
    conn.commit()
    conn.close()
