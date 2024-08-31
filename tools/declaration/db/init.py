from db.account_titles import create_account_titles_table
from db.journal_entries import create_journal_entries_table

def init_table():
    create_account_titles_table()
    create_journal_entries_table()
