import csv

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

from db.account_titles import get_export_accounts, import_accounts
from db.journal_entries import get_export_journals, import_journals


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

        # Frame for Opening Balance Section
        opening_balance_frame = tk.Frame(self)
        opening_balance_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        btn_opening_balance = ttk.Button(opening_balance_frame, text="期首値の入力", command=lambda: controller.show_frame("OpeningBalancePage"))
        btn_opening_balance.grid(row=0, column=0, padx=10)

        # Frame for Journal Section
        journal_frame = tk.Frame(self)
        journal_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        btn_journal = ttk.Button(journal_frame, text="仕訳の入力", command=lambda: controller.show_frame("JournalPage"))
        btn_journal.grid(row=0, column=0, padx=10)

        btn_export_journal_entries = ttk.Button(journal_frame, text="export", command=self.export_journal_entries)
        btn_export_journal_entries.grid(row=0, column=1, padx=10)

        btn_import_journal_entries = ttk.Button(journal_frame, text="import", command=self.import_journal_entries)
        btn_import_journal_entries.grid(row=0, column=2, padx=10)

        # Frame for General Section
        general_frame = tk.Frame(self)
        general_frame.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        btn_general_ledger = ttk.Button(general_frame, text="総勘定元帳", command=lambda: controller.show_frame("GeneralLedgerPage"))
        btn_general_ledger.grid(row=0, column=0, padx=10)

        # Frame for Balance Section
        balance_frame = tk.Frame(self)
        balance_frame.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        btn_balance_sheet = ttk.Button(balance_frame, text="貸借対照表", command=lambda: controller.show_frame("BalanceSheetPage"))
        btn_balance_sheet.grid(row=0, column=0, padx=10)

        self.load_logo()

    def load_logo(self):
        current_dir = os.path.dirname(__file__)
        logo_path = os.path.join(current_dir, 'src', 'title_logo.png')  # パスを組み立てる

        # 画像を開いて、tkinterで表示できる形式に変換
        image = Image.open(logo_path)
        image.thumbnail((300, 150), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(image)

        # ラベルを作成し、画像を配置
        logo_label = ttk.Label(self, image=self.logo)
        logo_label.image = self.logo  # 参照を保持するために必要
        logo_label.grid(row=0, column=0, pady=20)  # 上下の余白を指定して配置

    def export_account_titles(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            rows = get_export_accounts()
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["account_id", "name", "category", "borrowing_type", "allocation"])
                writer.writerows(rows)

    def import_account_titles(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = [tuple(row.values()) for row in reader]

            # 確認ダイアログを表示
            if messagebox.askyesno("確認", "入力済みの勘定科目が消えますが問題ないですか？"):
                import_accounts(rows)
            

    def export_journal_entries(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            rows = get_export_journals()

            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["journal_id", "date", "debit_account_id", "credit_account_id", "amount", "comment"])
                writer.writerows(rows)

    def import_journal_entries(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = [tuple(row.values()) for row in reader]

            # 確認ダイアログを表示
            if messagebox.askyesno("確認", "入力済みの仕訳が消えますが問題ないですか？"):
                import_journals(rows)
