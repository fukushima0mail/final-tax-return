import tkinter as tk
from tkinter import ttk
from db.account_titles import get_pl


class PLPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="lightgray")

        # Title
        tk.Label(self, text="損益計算書", font=("Helvetica", 16, "bold"), bg="lightgray").pack(pady=10)

        # Treeview for displaying PL data
        self.tree = ttk.Treeview(self, columns=("Category", "Account Name", "Total"), show="headings")
        self.tree.heading("Category", text="カテゴリー")
        self.tree.heading("Account Name", text="勘定科目名")
        self.tree.heading("Total", text="金額")
        self.tree.pack(pady=10, fill="both", expand=True, padx=20)

        # Back button to navigate to the previous page
        back_button = ttk.Button(self, text="戻る", command=lambda: controller.show_frame("StartPage"))
        back_button.pack(pady=10)

    def calculate_pl(self):
        """損益計算書を計算して表示する"""
        self.tree.delete(*self.tree.get_children())
        accounts_pl = get_pl()

        # Category 4: 収益
        category_4_accounts = [a for a in accounts_pl if a[1] == 4]
        category_4_total = 0
        for account in category_4_accounts:
            name, _, allocation, borrowing_type, debit_total, credit_total = account
            total = round((debit_total - credit_total) * allocation / 100 * borrowing_type)
            category_4_total += total
            self.tree.insert("", "end", values=("収益", name, f"{total:,}"))
        self.tree.insert("", "end", values=("", "合計", f"{category_4_total:,}"))
        self.tree.insert("", "end", values=("", "", ""))

        # Category 5: 費用
        category_5_accounts = [a for a in accounts_pl if a[1] == 5]
        category_5_total = 0
        for account in category_5_accounts:
            name, _, allocation, borrowing_type, debit_total, credit_total = account
            total = round((debit_total - credit_total) * allocation / 100 * borrowing_type)
            category_5_total += total
            self.tree.insert("", "end", values=("費用", name, f"{total:,}"))
        self.tree.insert("", "end", values=("", "合計", f"{category_5_total:,}"))
        self.tree.insert("", "end", values=("", "", ""))

        # 差引金額
        net = category_4_total - category_5_total
        self.tree.insert("", "end", values=("差引金額", "", f"{net:,}"))

        # 所得金額
        special_deduction = 650000
        self.tree.insert("", "end", values=("青色申告特別控除額", "", f"{special_deduction:,}"))
        income_amount = max(0, net - special_deduction)
        self.tree.insert("", "end", values=("所得金額 (特別控除後)", "", f"{income_amount:,}"))

    def tkraise(self, *args, **kwargs):
        """ページが表示されたときに読み込む"""
        self.calculate_pl()
        super().tkraise(*args, **kwargs)
