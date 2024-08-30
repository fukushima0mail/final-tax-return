import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

class JournalPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="lightgray")

        # Title
        tk.Label(self, text="仕訳の入力", font=("Helvetica", 16, "bold"), bg="lightgray").pack(pady=10)

        # Frame for input form
        form_frame = tk.Frame(self, bg="lightgray")
        form_frame.pack(padx=20, pady=10, fill="x")

        # Default year to last year
        self.current_year = datetime.now().year - 1

        # Create input widgets
        self.create_input_widgets(form_frame)

        # Treeview for displaying journal entries
        self.tree = ttk.Treeview(self, columns=("Date", "Debit Account", "Credit Account", "Amount"), show='headings')
        self.tree.heading("Date", text="日付")
        self.tree.heading("Debit Account", text="借方勘定科目")
        self.tree.heading("Credit Account", text="貸方勘定科目")
        self.tree.heading("Amount", text="金額")
        self.tree.pack(pady=10, fill="both", expand=True, padx=20)

        # Back button
        btn_back = tk.Button(self, text="戻る", command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(pady=10)

    def create_input_widgets(self, parent):
        """Create input widgets arranged horizontally."""
        # Year
        tk.Label(parent, text="年度", bg="lightgray").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_year = tk.Entry(parent, width=10)
        self.entry_year.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.entry_year.insert(0, self.current_year)

        # Date
        tk.Label(parent, text="日付 (MM/DD)", bg="lightgray").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.entry_date = tk.Entry(parent, width=10)
        self.entry_date.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        # Debit Account
        tk.Label(parent, text="借方勘定科目", bg="lightgray").grid(row=0, column=4, padx=10, pady=5, sticky="e")
        self.debit_account_var = tk.StringVar()
        self.debit_account_menu = ttk.OptionMenu(parent, self.debit_account_var, '')
        self.debit_account_menu.grid(row=0, column=5, padx=10, pady=5, sticky="w")

        # Credit Account
        tk.Label(parent, text="貸方勘定科目", bg="lightgray").grid(row=0, column=6, padx=10, pady=5, sticky="e")
        self.credit_account_var = tk.StringVar()
        self.credit_account_menu = ttk.OptionMenu(parent, self.credit_account_var, '')
        self.credit_account_menu.grid(row=0, column=7, padx=10, pady=5, sticky="w")

        # Amount
        tk.Label(parent, text="金額", bg="lightgray").grid(row=0, column=8, padx=10, pady=5, sticky="e")
        self.entry_amount = tk.Entry(parent, width=10)
        self.entry_amount.grid(row=0, column=9, padx=10, pady=5, sticky="w")

        # Add button
        btn_add = tk.Button(parent, text="追加", command=self.add_journal_entry)
        btn_add.grid(row=0, column=10, columnspan=2, padx=10, pady=5, sticky="ew")

    def update_account_menus(self):
        """データベースから勘定科目を読み込み、OptionMenuを更新する"""
        conn = sqlite3.connect('accounting.db')
        c = conn.cursor()
        c.execute('SELECT name FROM account_titles')
        account_titles = [row[0] for row in c.fetchall()]
        conn.close()

        self.debit_account_var.set(account_titles[0] if account_titles else '')
        self.credit_account_var.set(account_titles[0] if account_titles else '')

        menu = self.debit_account_menu['menu']
        menu.delete(0, 'end')
        for title in account_titles:
            menu.add_command(label=title, command=lambda value=title: self.debit_account_var.set(value))

        menu = self.credit_account_menu['menu']
        menu.delete(0, 'end')
        for title in account_titles:
            menu.add_command(label=title, command=lambda value=title: self.credit_account_var.set(value))

    def load_journal_entries(self):
        """データベースから仕訳を読み込んでTreeviewに表示する"""
        self.tree.delete(*self.tree.get_children())  # Clear existing entries
        conn = sqlite3.connect('accounting.db')
        c = conn.cursor()
        c.execute('''
            SELECT j.year, j.date, d.name, c.name, j.amount
            FROM journal_entries j
            JOIN account_titles d ON j.debit_account_id = d.id
            JOIN account_titles c ON j.credit_account_id = c.id
        ''')
        entries = c.fetchall()
        conn.close()

        for entry in entries:
            year, date, debit_account, credit_account, amount = entry
            self.tree.insert('', 'end', values=(f"{year}-{date}", debit_account, credit_account, amount))

    def add_journal_entry(self):
        year = int(self.entry_year.get())
        date_text = self.entry_date.get()
        debit_account_name = self.debit_account_var.get()
        credit_account_name = self.credit_account_var.get()
        amount = int(self.entry_amount.get())

        if not year or not date_text or not debit_account_name or not credit_account_name:
            messagebox.showerror("入力エラー", "すべてのフィールドを入力してください。")
            return

        month, day = map(int, date_text.split('/'))
        if 4 <= month <= 12:
            date = f"{month:02d}-{day:02d}"
        else:
            date = f"{month:02d}-{day:02d}"

        conn = sqlite3.connect('accounting.db')
        c = conn.cursor()
        
        c.execute('SELECT id FROM account_titles WHERE name = ?', (debit_account_name,))
        debit_account_id = c.fetchone()[0]

        c.execute('SELECT id FROM account_titles WHERE name = ?', (credit_account_name,))
        credit_account_id = c.fetchone()[0]

        c.execute('''
            INSERT INTO journal_entries 
            (year, date, debit_account_id, credit_account_id, amount) 
            VALUES (?, ?, ?, ?, ?)
        ''', (year, date, debit_account_id, credit_account_id, amount))

        conn.commit()
        conn.close()

        self.load_journal_entries()  # 追加後にリストを更新

    def tkraise(self, *args, **kwargs):
        """ページが表示されたときに勘定科目と仕訳を読み込む"""
        self.update_account_menus()
        self.load_journal_entries()
        super().tkraise(*args, **kwargs)
