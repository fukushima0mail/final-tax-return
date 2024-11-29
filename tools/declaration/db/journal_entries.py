from uuid import uuid4

from .connection import DBConnection

def create_journal_entries_table():
    with DBConnection() as c:
        c.execute('''
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                journal_id TEXT NOT NULL,
                date TEXT NOT NULL,
                debit_account_id INTEGER,
                credit_account_id INTEGER,
                amount INTEGER NOT NULL,
                comment TEXT
            )
        ''')

def add_journal(date, debit_account_name, credit_account_name, amount, comment):
    with DBConnection() as c:
        c.execute('SELECT account_id FROM account_titles WHERE name = ?', (debit_account_name,))
        debit_account_id = c.fetchone()[0]

        c.execute('SELECT account_id FROM account_titles WHERE name = ?', (credit_account_name,))
        credit_account_id = c.fetchone()[0]

        c.execute('''
            INSERT INTO journal_entries (journal_id, date, debit_account_id, credit_account_id, amount, comment)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (str(uuid4()), date, debit_account_id, credit_account_id, amount, comment))

def add_opening_balance_journal(debit_account_id, amount):
    with DBConnection() as c:
        c.execute('''
            INSERT INTO journal_entries (journal_id, date, debit_account_id, amount, comment)
            VALUES (?, ?, ?, ?, ?)
        ''', (str(uuid4()), "01-01", debit_account_id, amount, "期首値"))

def update_journal(journal_id, date, debit_account_name, credit_account_name, amount, comment):
    with DBConnection() as c:
        c.execute('SELECT account_id FROM account_titles WHERE name = ?', (debit_account_name,))
        debit_account_id = c.fetchone()[0]

        c.execute('SELECT account_id FROM account_titles WHERE name = ?', (credit_account_name,))
        credit_account_id = c.fetchone()[0]

        c.execute('''
            UPDATE journal_entries
            SET date = ?, debit_account_id = ?, credit_account_id = ?, amount = ?, comment = ?
            WHERE journal_id = ?
        ''', (date, debit_account_id, credit_account_id, amount, comment, journal_id))

def update_opening_balance_journal(journal_id, debit_account_id, amount):
    with DBConnection() as c:
        c.execute('''
            UPDATE journal_entries
            SET debit_account_id = ?, amount = ?
            WHERE journal_id = ?
        ''', (debit_account_id, amount, journal_id))

def get_export_journals():
    with DBConnection() as c:
        c.execute('''
            SELECT journal_id, date, debit_account_id, credit_account_id, amount, comment
            FROM journal_entries
        ''')
        rows = c.fetchall()
    return rows

def get_all_journals():
    with DBConnection() as c:
        c.execute('''
            SELECT j.id, j.journal_id, j.date, d.name, c.name, j.amount, j.comment
            FROM journal_entries j
            JOIN account_titles d ON j.debit_account_id = d.account_id
            JOIN account_titles c ON j.credit_account_id = c.account_id
            WHERE credit_account_id is not null
        ''')
        rows = c.fetchall()
    return rows

def get_opening_balance_journal(account_id):
    with DBConnection() as c:
        c.execute('''
            SELECT journal_id, amount
            FROM journal_entries
            WHERE debit_account_id = ? AND credit_account_id is null
        ''', (account_id,))
        
        rows = c.fetchall()
    return rows

def delete_journal(journal_id):
    with DBConnection() as c:
        c.execute('DELETE FROM journal_entries WHERE journal_id = ?', (journal_id,))

def get_general(account_id):
    with DBConnection() as c:
        c.execute('''
            SELECT
                j.date,
                CASE 
                    WHEN j.debit_account_id = ? THEN COALESCE(ac_credit.name, '')
                    ELSE COALESCE(ac_debit.name, '')
                END as counterparty_account,
                j.comment,
                CASE 
                    WHEN j.debit_account_id = ? THEN j.amount
                    ELSE 0
                END as debit,
                CASE 
                    WHEN j.credit_account_id = ? THEN j.amount
                    ELSE 0
                END as credit
            FROM journal_entries j
            LEFT JOIN account_titles ac_debit ON j.debit_account_id = ac_debit.account_id
            LEFT JOIN account_titles ac_credit ON j.credit_account_id = ac_credit.account_id
            WHERE j.debit_account_id = ? OR j.credit_account_id = ?
            ORDER BY j.date
        ''', (account_id, account_id, account_id, account_id, account_id))
        rows = c.fetchall()
    return rows

def import_journals(rows):
    with DBConnection() as c:
        c.execute('DELETE FROM journal_entries')
        c.executemany('INSERT INTO journal_entries (journal_id, date, debit_account_id, credit_account_id, amount, comment) VALUES (?, ?, ?, ?, ?, ?, ?)', rows)
