import tkinter as tk
from tkinter import ttk

from db.journal_entries import get_general
from db.account_titles import get_all_accounts
from lib.utils import SortableTreeview

class GeneralLedgerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="lightgray")

        tk.Label(self, text="総勘定元帳", font=("Helvetica", 16, "bold"), bg="lightgray").pack(pady=10)

        btn_back = ttk.Button(self, text="戻る", command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(pady=10, side="bottom")

        # Scrollable canvas
        self.canvas = tk.Canvas(self, bg="lightgray")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def display_ledger(self):
        # Clear the frame before displaying the ledger
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        account_titles = get_all_accounts()
        for _, account_id, account_name, category, borrowing_type, allocation, _, _, _ in account_titles:
            journal_entries = get_general(account_id)
            if journal_entries:
                # Create a label for each account title
                account_label = tk.Label(self.scrollable_frame, text=f"■{account_name}", font=("Helvetica", 14, "bold"), bg="lightgray")
                account_label.pack(anchor="w", padx=10, pady=5)

                # Create TreeView for each account title
                tree = SortableTreeview(self.scrollable_frame, columns=("Date", "Counterparty Account", "Comment", "Debit", "Credit", "Balance"), show='headings')
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
                
                # 負債科目のみ、必要に応じて事業主貸が発生
                if balance and category == 5 and allocation != 100:
                    adjusted_amount = round(balance * ((100 - allocation) / 100))
                    balance -= adjusted_amount * borrowing_type
                    tree.insert('', 'end', values=('12-31', '事業主貸', '按分の個人分', 0, adjusted_amount, balance))



    def tkraise(self, *args, **kwargs):
        """ページが表示されたときに読み込む"""
        self.display_ledger()
        super().tkraise(*args, **kwargs)
