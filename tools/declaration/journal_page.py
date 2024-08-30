import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class JournalPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="仕訳の入力", font=("Helvetica", 16, "bold")).pack(pady=10)

        tk.Label(self, text="年度").pack()
        self.entry_year = tk.Entry(self)
        self.entry_year.pack()

        tk.Label(self, text="日付 (MM/DD)").pack()
        self.entry_date = tk.Entry(self)
        self.entry_date.pack()

        tk.Label(self, text="借方勘定科目").pack()
        self.debit_account_var = tk.StringVar()
        self.debit_account_menu = ttk.OptionMenu(self, self.debit_account_var, '')
        self.debit_account_menu.pack()

        tk.Label(self, text="貸方勘定科目").pack()
        self.credit_account_var = tk.StringVar()
        self.credit_account_menu = ttk.OptionMenu(self, self.credit_account_var, '')
        self.credit_account_menu.pack()

        tk.Label(self, text="金額").pack()
        self.entry_amount = tk.Entry(self)
        self.entry_amount.pack()

        btn_add = tk.Button(self, text="追加", command=self.add_journal_entry)
        btn_add.pack(pady=5)

        btn_back = tk.Button(self, text="戻る", command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(pady=5)

        # Treeview for displaying journal entries
        self.tree = ttk.Treeview(self, columns=("Date", "Debit Account", "Credit Account", "Amount"), show='headings')
        self.tree.heading("Date", text="日付")
        self.tree.heading("Debit Account", text="借方勘定科目")
        self.tree.heading("Credit Account", text="貸方勘定科目")
        self.tree.heading("Amount", text="金額")
        self.tree.pack(pady=10, fill="both", expand=True)

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
