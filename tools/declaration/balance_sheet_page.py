import tkinter as tk
from tkinter import ttk


class BalanceSheetPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="lightgray")

        # Title
        tk.Label(self, text="貸借対照表", font=("Helvetica", 16, "bold"), bg="lightgray").pack(pady=10)

        # Treeview for displaying Balance Sheet data
        self.tree = ttk.Treeview(
            self, columns=("Section", "Account Name", "Start of Year", "End of Year"), show="headings"
        )
        self.tree.heading("Section", text="区分")
        self.tree.heading("Account Name", text="科目名")
        self.tree.heading("Start of Year", text="1月1日（期首）")
        self.tree.heading("End of Year", text="12月31日（期末）")
        self.tree.pack(pady=10, fill="both", expand=True, padx=20)

        # Back button to navigate to the previous page
        back_button = ttk.Button(self, text="戻る", command=lambda: controller.show_frame("StartPage"))
        back_button.pack(pady=10)

    def display_balance_sheet(self):
        """貸借対照表を計算して表示する"""
        self.tree.delete(*self.tree.get_children())

        # Example fixed data (replace this with actual calculations)
        assets = [
            ("資産", "現金", "¥316,957", "¥316,957"),
            ("資産", "当座預金", "", ""),
            ("資産", "その他預金", "¥839,014", "¥283,623"),
            ("資産", "棚卸資産", "¥107,007", "¥0"),
        ]
        liabilities_and_capital = [
            ("負債・資本", "支払手形", "", ""),
            ("負債・資本", "元入金", "¥1,262,978", "¥1,262,978"),
            ("負債・資本", "青色申告特別控除前の所得金額", "", "¥3,623,325"),
        ]

        # Insert assets
        for asset in assets:
            self.tree.insert("", "end", values=asset)
        self.tree.insert("", "end", values=("", "", "", ""))  # Blank row

        # Insert liabilities and capital
        for liability in liabilities_and_capital:
            self.tree.insert("", "end", values=liability)
        self.tree.insert("", "end", values=("", "", "", ""))  # Blank row

        # Totals
        self.tree.insert("", "end", values=("合計", "", "¥1,262,978", "¥4,886,303"))

    def tkraise(self, *args, **kwargs):
        """ページが表示されたときに読み込む"""
        self.display_balance_sheet()
        super().tkraise(*args, **kwargs)
