import tkinter as tk
from tkinter import ttk
import sqlite3

from db.journal_entries import get_general
from db.account_titles import get_all_accounts
from lib.utils import SortableTreeview


class GeneralLedgerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="lightgray")

        # Title
        tk.Label(self, text="総勘定元帳", font=("Helvetica", 16, "bold"), bg="lightgray").pack(pady=10)

        # Scrollable canvas
        canvas = tk.Canvas(self, bg="lightgray")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Load and display account data
        self.display_ledger(scrollable_frame)

        # Back button
        btn_back = ttk.Button(self, text="戻る", command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(pady=10)

    def display_ledger(self, parent):
        account_titles = get_all_accounts()
        for account_id, account_name, _, borrowing_type, _ in account_titles:
            journal_entries = get_general(account_id)
            if journal_entries:
                # Create a label for each account title
                account_label = tk.Label(parent, text=f"■{account_name}", font=("Helvetica", 14, "bold"), bg="lightgray")
                account_label.pack(anchor="w", padx=10, pady=5)

                # Create TreeView for each account title
                tree = SortableTreeview(parent, columns=("Date", "Counterparty Account", "Comment", "Debit", "Credit", "Balance"), show='headings')
                tree.heading("Date", text="日付")
                tree.heading("Counterparty Account", text="相手科目")
                tree.heading("Comment", text="コメント")
                tree.heading("Debit", text="借方")
                tree.heading("Credit", text="貸方")
                tree.heading("Balance", text="残高")

                # Adjust column widths
                tree.column("Date", width=100)
                tree.column("Counterparty Account", width=150)
                tree.column("Comment", width=200)
                tree.column("Debit", width=100, anchor="e")
                tree.column("Credit", width=100, anchor="e")
                tree.column("Balance", width=100, anchor="e")

                tree.pack(fill="x", padx=20, pady=5)

                balance = 0
                for entry in journal_entries:
                    date, counterparty_account, comment, debit, credit = entry
                    balance += (debit - credit) * borrowing_type
                    tree.insert('', 'end', values=(date, counterparty_account, comment, debit, credit, balance))
