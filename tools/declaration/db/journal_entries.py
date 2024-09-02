from .connection import get_db_connection

def create_journal_entries_table():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            journal_id TEXT NOT NULL,
            year INTEGER NOT NULL,
            date TEXT NOT NULL,
            debit_account_id INTEGER NOT NULL,
            credit_account_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            comment TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_journal(journal_id, year, date, debit_account_name, credit_account_name, amount, comment):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('SELECT account_id FROM account_titles WHERE name = ?', (debit_account_name,))
    debit_account_id = c.fetchone()[0]

    c.execute('SELECT account_id FROM account_titles WHERE name = ?', (credit_account_name,))
    credit_account_id = c.fetchone()[0]

    c.execute('''
        INSERT INTO journal_entries (journal_id, year, date, debit_account_id, credit_account_id, amount, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (journal_id, year, date, debit_account_id, credit_account_id, amount, comment))
    conn.commit()
    conn.close()

def update_journal(journal_id, year, date, debit_account_name, credit_account_name, amount, comment):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('SELECT account_id FROM account_titles WHERE name = ?', (debit_account_name,))
    debit_account_id = c.fetchone()[0]

    c.execute('SELECT account_id FROM account_titles WHERE name = ?', (credit_account_name,))
    credit_account_id = c.fetchone()[0]

    c.execute('''
        UPDATE journal_entries
        SET 'year' = ?, date = ?, debit_account_id = ?, credit_account_id = ?, amount = ?, comment = ?
        WHERE journal_id = ?
    ''', (year, date, debit_account_id, credit_account_id, amount, comment, journal_id))
    conn.commit()
    conn.close()

def get_all_journals():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT j.id, j.journal_id, j.year, j.date, d.name, c.name, j.amount, j.comment
        FROM journal_entries j
        JOIN account_titles d ON j.debit_account_id = d.account_id
        JOIN account_titles c ON j.credit_account_id = c.account_id
    ''')
    rows = c.fetchall()
    conn.close()
    return rows

def delete_journal(journal_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM journal_entries WHERE journal_id = ?', (journal_id,))
    conn.commit()
    conn.close()

def get_general(account_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT
            j.date,
            CASE 
                WHEN j.debit_account_id = ? THEN ac_credit.name
                ELSE ac_debit.name
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
        JOIN account_titles ac_debit ON j.debit_account_id = ac_debit.account_id
        JOIN account_titles ac_credit ON j.credit_account_id = ac_credit.account_id
        WHERE j.debit_account_id = ? OR j.credit_account_id = ?
        ORDER BY j.date
    ''', (account_id, account_id, account_id, account_id, account_id))
    rows = c.fetchall()
    conn.close()
    return rows
