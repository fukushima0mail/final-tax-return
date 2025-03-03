from uuid import uuid4

from .connection import DBConnection


CATEGORY_OPTIONS = {
    "資産": 1,
    "負債": 2,
    "純資産": 3,
    "収益": 4,
    "費用": 5
}


def create_account_titles_table():
    with DBConnection() as c:
        c.execute('''
            CREATE TABLE IF NOT EXISTS account_titles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT NOT NULL,
                name TEXT NOT NULL,
                category SMALLINT NOT NULL,
                borrowing_type INTEGER DEFAULT 1,
                allocation INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT (CURRENT_TIMESTAMP),
                updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP),
                is_deleted BOOLEAN DEFAULT 0
            )
        ''')

        trigger_name = "update_updated_at_account_titles"
        trigger_check_query = f'''
            SELECT name FROM sqlite_master
            WHERE type='trigger' AND name='{trigger_name}';
        '''
        c.execute(trigger_check_query)
        trigger_exists = c.fetchone() is not None

        if not trigger_exists:
            c.execute(f'''
                CREATE TRIGGER {trigger_name}
                AFTER UPDATE ON account_titles
                FOR EACH ROW
                BEGIN
                    UPDATE account_titles
                    SET updated_at = CURRENT_TIMESTAMP
                    WHERE id = OLD.id;
                END
            ''')

def add_account(name, category, borrowing_type, allocation):
    with DBConnection() as c:
        c.execute('''
            INSERT INTO account_titles (account_id, name, category, borrowing_type, allocation)
            VALUES (?, ?, ?, ?, ?)
        ''', (str(uuid4()), name, category, borrowing_type, allocation))

def get_export_accounts():
    with DBConnection() as c:
        c.execute('SELECT account_id, name, category, borrowing_type, allocation, created_at, updated_at, is_deleted FROM account_titles')
        rows = c.fetchall()
    return rows

def get_all_accounts():
    with DBConnection() as c:
        c.execute('SELECT * FROM account_titles')
        rows = c.fetchall()
    return rows

def get_opening_balance_account():
    with DBConnection() as c:
        c.execute('SELECT account_id, name, category FROM account_titles WHERE category in (1, 2)')
        rows = c.fetchall()
    return [(account_id, name, {v: k for k, v in CATEGORY_OPTIONS.items()}[category]) for account_id, name, category in rows]

def get_total_of_account():
    with DBConnection() as c:
        c.execute('''
            SELECT
                at.name,
                at.category,
                at.allocation,
                at.borrowing_type,
                COALESCE(SUM(CASE WHEN j.debit_account_id = at.account_id THEN j.amount ELSE 0 END), 0) AS debit_total,
                COALESCE(SUM(CASE WHEN j.credit_account_id = at.account_id THEN j.amount ELSE 0 END), 0) AS credit_total
            FROM
                account_titles at
            LEFT JOIN
                journal_entries j
            ON
                at.account_id = j.debit_account_id OR at.account_id = j.credit_account_id
            GROUP BY
                at.account_id, at.name, at.category, at.allocation, at.borrowing_type
            ''')
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
        c.execute('DELETE FROM journal_entries WHERE debit_account_id = ? OR credit_account_id = ?', (account_id, account_id))

def import_accounts(rows):
    casted_rows = [(account_id, name, int(category), int(borrowing_type), int(allocation), created_at, updated_at, int(is_deleted)) for account_id, name, category, borrowing_type, allocation, created_at, updated_at, is_deleted in rows]
    with DBConnection() as c:
        c.execute('DELETE FROM account_titles')
        c.executemany('INSERT INTO account_titles (account_id, name, category, borrowing_type, allocation, created_at, updated_at, is_deleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', casted_rows)
