import tkinter as tk
from tkinter import messagebox, ttk

from db.journal_entries import add_opening_balance_journal, get_opening_balance_journal, update_opening_balance_journal
from db.account_titles import get_opening_balance_account

class OpeningBalancePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="lightgray")

        tk.Label(self, text="期首値入力", font=("Helvetica", 16, "bold"), bg="lightgray").pack(pady=10)

        # Scrollable canvas
        self.canvas = tk.Canvas(self, bg="lightgray")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Dictionary to hold input fields for balances
        self.balance_entries = {}

        btn_back = ttk.Button(self, text="戻る", command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(pady=10)

        btn_save = ttk.Button(self, text="保存", command=self.save_balances)
        btn_save.pack(pady=10)

    def display_opening_balance_inputs(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.balance_entries.clear()

        account_titles = get_opening_balance_account()
        
        for account_id, account_name, category in account_titles:
            frame = ttk.Frame(self.scrollable_frame, padding=5)
            frame.pack(fill="x", padx=10, pady=2)

            # Account name label
            ttk.Label(frame, text=f"■{account_name} - {category}", width=20).pack(side="left")

            # Balance entry field
            entry = ttk.Entry(frame, width=15)
            entry.pack(side="left", padx=10)
            self.balance_entries[account_id] = entry

            # Load existing balance if available
            self.load_existing_balance(account_id, entry)

    def load_existing_balance(self, account_id, entry):
        """Load existing opening balance for the account if available."""
        journals = get_opening_balance_journal(account_id)
        
        if len(journals) > 1:
            messagebox.showerror("エラー", f"{account_id} に対して期首値の仕訳が複数存在します。1つに絞ってください。")
        elif journals:
            amount = journals[0][1]
            entry.insert(0, str(amount))

    def save_balances(self):
        """Save or update the opening balances for each account."""
        for account_id, entry in self.balance_entries.items():
            balance = int(entry.get()) if entry.get() else 0
            journals = get_opening_balance_journal(account_id)

            if journals:
                journal_id = journals[0][0]
                update_opening_balance_journal(journal_id, account_id, balance)
            else:
                add_opening_balance_journal(account_id, balance)
        self.display_opening_balance_inputs()


    def tkraise(self, *args, **kwargs):
        """ページが表示されたときに勘定科目と期首値を読み込む"""
        self.display_opening_balance_inputs()
        super().tkraise(*args, **kwargs)
