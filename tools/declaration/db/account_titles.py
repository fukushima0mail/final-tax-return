from .connection import DBConnection

def create_account_titles_table():
    with DBConnection() as c:
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

def add_account(account_id, name, category, borrowing_type, allocation):
    with DBConnection() as c:
        c.execute('''
            INSERT INTO account_titles (account_id, name, category, borrowing_type, allocation)
            VALUES (?, ?, ?, ?, ?)
        ''', (account_id, name, category, borrowing_type, allocation))

def get_export_accounts():
    with DBConnection() as c:
        c.execute('SELECT account_id, name, category, borrowing_type, allocation FROM account_titles')
        rows = c.fetchall()
    return rows

def get_all_accounts():
    with DBConnection() as c:
        c.execute('SELECT * FROM account_titles')
        rows = c.fetchall()
    return rows

def get_account_names():
    with DBConnection() as c:
        c.execute('SELECT name FROM account_titles')
        rows = c.fetchall()
    return [row[0] for row in rows]

def update_account(account_id, name, category, borrowing_type, allocation):
    with DBConnection() as c:
        c.execute('''
            UPDATE account_titles
            SET name = ?, category = ?, borrowing_type = ?, allocation = ?
            WHERE account_id = ?
        ''', (name, category, borrowing_type, allocation, account_id))

def delete_account(account_id):
    with DBConnection() as c:
        c.execute('DELETE FROM account_titles WHERE account_id = ?', (account_id,))

def import_accounts(rows):
    casted_rows = [(account_id, name, int(category), int(borrowing_type), int(allocation)) for account_id, name, category, borrowing_type, allocation in rows]
    with DBConnection() as c:
        c.execute('DELETE FROM account_titles')
        c.executemany('INSERT INTO account_titles (account_id, name, category, borrowing_type, allocation) VALUES (?, ?, ?, ?, ?)', casted_rows)
