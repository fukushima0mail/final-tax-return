import tkinter as tk
from tkinter import ttk

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="メニュー", font=("Helvetica", 18, "bold")).grid(row=0, column=0, columnspan=3, pady=20)

        # Frame for Account Section
        account_frame = tk.Frame(self)
        account_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        btn_account = ttk.Button(account_frame, text="勘定科目の登録", command=lambda: controller.show_frame("AccountPage"))
        btn_account.grid(row=0, column=0, padx=10)

        btn_export_account_titles = ttk.Button(account_frame, text="export", command=self.export_account_titles)
        btn_export_account_titles.grid(row=0, column=1, padx=10)

        btn_import_account_titles = ttk.Button(account_frame, text="import", command=self.import_account_titles)
        btn_import_account_titles.grid(row=0, column=2, padx=10)

        # Frame for Journal Section
        journal_frame = tk.Frame(self)
        journal_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        btn_journal = ttk.Button(journal_frame, text="仕訳の入力", command=lambda: controller.show_frame("JournalPage"))
        btn_journal.grid(row=0, column=0, padx=10)

        btn_export_journal_entries = ttk.Button(journal_frame, text="export", command=self.export_journal_entries)
        btn_export_journal_entries.grid(row=0, column=1, padx=10)

        btn_import_journal_entries = ttk.Button(journal_frame, text="import", command=self.import_journal_entries)
        btn_import_journal_entries.grid(row=0, column=2, padx=10)

        # Frame for General Section
        general_frame = tk.Frame(self)
        general_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        btn_general_ledger = ttk.Button(general_frame, text="総勘定元帳", command=lambda: controller.show_frame("GeneralLedgerPage"))
        btn_general_ledger.grid(row=0, column=0, padx=10)

    def export_account_titles(self):
        # Implement export logic here
        pass

    def import_account_titles(self):
        # Implement import logic here
        pass

    def export_journal_entries(self):
        # Implement export logic here
        pass

    def import_journal_entries(self):
        # Implement import logic here
        pass
