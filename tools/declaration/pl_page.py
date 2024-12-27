import tkinter as tk
from tkinter import ttk
from lib.data import get_pl_data


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
        pl_data = get_pl_data()

        # Category 4: 収益
        for p in pl_data["profits"]:
            self.tree.insert("", "end", values=("収益", p["name"], f"{p['total']:,}"))
        self.tree.insert("", "end", values=("", "合計", f"{sum([p['total'] for p in pl_data['profits']]):,}"))
        self.tree.insert("", "end", values=("", "", ""))

        # Category 5: 費用
        for l in pl_data["losses"]:
            self.tree.insert("", "end", values=("費用", l["name"], f"{l['total']:,}"))
        self.tree.insert("", "end", values=("", "合計", f"{sum([l['total'] for l in pl_data['losses']]):,}"))
        self.tree.insert("", "end", values=("", "", ""))

        # 差引金額
        self.tree.insert("", "end", values=("差引金額", "", f"{pl_data['net']:,}"))

        # 所得金額
        self.tree.insert("", "end", values=("青色申告特別控除額", "", f"{pl_data['special_deduction']:,}"))
        self.tree.insert("", "end", values=("所得金額 (特別控除後)", "", f"{pl_data['income_amount']:,}"))

    def tkraise(self, *args, **kwargs):
        """ページが表示されたときに読み込む"""
        self.calculate_pl()
        super().tkraise(*args, **kwargs)
