import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from db.journal_entries import add_journal, delete_journal, get_all_journals, update_journal
from db.account_titles import get_account_names
from lib.utils import SortableTreeview

class JournalPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="lightgray")

        # Title
        ttk.Label(self, text="仕訳の入力", font=("Helvetica", 16, "bold"), background="lightgray").pack(pady=10)

        # Default year to last year
        self.current_year = datetime.now().year - 1

        # Treeview for displaying journal entries
        self.tree = SortableTreeview(self, columns=("Year", "Date", "Debit Account", "Credit Account", "Amount", "Comment"), show='headings', selectmode='browse')
        self.tree.column("Year", width=0, stretch=False, minwidth=0)
        self.tree.heading("Date", text="日付")
        self.tree.heading("Debit Account", text="借方勘定科目")
        self.tree.heading("Credit Account", text="貸方勘定科目")
        self.tree.heading("Amount", text="金額")
        self.tree.heading("Comment", text="コメント")
        self.tree.pack(pady=10, fill="both", expand=True, padx=20)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Frame for input form
        form_frame = tk.Frame(self, bg="lightgray")
        form_frame.pack(padx=20, pady=10, fill="x")

        # Create input widgets
        self.create_input_widgets(form_frame)

        # Button frame for actions
        button_frame = tk.Frame(self, bg="lightgray")
        button_frame.pack(pady=10)

        # Add and delete buttons
        btn_add = ttk.Button(button_frame, text="追加", command=self.add_journal_entry)
        btn_add.pack(side="left", padx=5)

        btn_update = ttk.Button(button_frame, text="更新", command=self.update_journal_entry)
        btn_update.pack(side="left", padx=5)

        btn_delete = ttk.Button(button_frame, text="削除", command=self.delete_journal_entry)
        btn_delete.pack(side="left", padx=5)

        # Back button
        btn_back = ttk.Button(self, text="戻る", command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(pady=10)

        # Set default size for TreeView
        self.tree.config(height=15)  # Set the number of visible rows in the TreeView

    def create_input_widgets(self, parent):
        """Create input widgets arranged horizontally."""
        # Year
        ttk.Label(parent, text="年度", background="lightgray").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_year = ttk.Entry(parent, width=10)
        self.entry_year.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.entry_year.insert(0, self.current_year)

        # Date
        ttk.Label(parent, text="日付 (MM/DD)", background="lightgray").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.entry_date = ttk.Entry(parent, width=10)
        self.entry_date.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        # Debit Account
        ttk.Label(parent, text="借方勘定科目", background="lightgray").grid(row=0, column=4, padx=10, pady=5, sticky="e")
        self.debit_account_var = tk.StringVar()
        self.debit_account_menu = ttk.OptionMenu(parent, self.debit_account_var, '')
        self.debit_account_menu.grid(row=0, column=5, padx=10, pady=5, sticky="w")

        # Credit Account
        ttk.Label(parent, text="貸方勘定科目", background="lightgray").grid(row=0, column=6, padx=10, pady=5, sticky="e")
        self.credit_account_var = tk.StringVar()
        self.credit_account_menu = ttk.OptionMenu(parent, self.credit_account_var, '')
        self.credit_account_menu.grid(row=0, column=7, padx=10, pady=5, sticky="w")

        # Amount
        ttk.Label(parent, text="金額", background="lightgray").grid(row=0, column=8, padx=10, pady=5, sticky="e")
        self.entry_amount = ttk.Entry(parent, width=10)
        self.entry_amount.grid(row=0, column=9, padx=10, pady=5, sticky="w")
        self.entry_amount.bind("<Return>", self.handle_enter_key)

        # Comment
        ttk.Label(parent, text="コメント", background="lightgray").grid(row=0, column=10, padx=10, pady=5, sticky="e")
        self.entry_comment = ttk.Entry(parent, width=30)
        self.entry_comment.grid(row=0, column=11, padx=10, pady=5, sticky="w")

    def handle_enter_key(self, event):
        """Enterキーが押されたときの処理"""
        self.add_journal_entry()

    def update_account_menus(self):
        """データベースから勘定科目を読み込み、OptionMenuを更新する"""
        account_titles = get_account_names()

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

        entries = get_all_journals()

        for entry in entries:
            entry_id, year, date, debit_account, credit_account, amount, comment = entry
            self.tree.insert('', 'end', iid=entry_id, values=(year, date, debit_account, credit_account, amount, comment))

    def add_journal_entry(self):
        journal = self.get_input_journal_entry()
        add_journal(*journal)
        self.load_journal_entries()  # 追加後にリストを更新

    def update_journal_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("選択エラー", "更新する仕訳を選択してください。")
            return
        
        iid = selected_item[0]

        journal = self.get_input_journal_entry()
        update_journal(iid, *journal)

        self.load_journal_entries()

    def get_input_journal_entry(self):
        year = int(self.entry_year.get())
        date_text = self.entry_date.get()
        debit_account_name = self.debit_account_var.get()
        credit_account_name = self.credit_account_var.get()
        amount = int(self.entry_amount.get())
        comment = self.entry_comment.get()

        if not year or not date_text or not debit_account_name or not credit_account_name or not amount:
            messagebox.showerror("入力エラー", "すべてのフィールドを入力してください。")
            return

        month, day = map(int, date_text.split('/'))
        if 4 <= month <= 12:
            date = f"{year}-{month:02d}-{day:02d}"
        else:
            date = f"{year + 1}-{month:02d}-{day:02d}"

        return (year, date, debit_account_name, credit_account_name, amount, comment)

    def delete_journal_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("選択エラー", "削除する仕訳を選択してください。")
            return

        entry_id = selected_item[0]
        delete_journal(entry_id)

        self.load_journal_entries()  # 削除後にリストを更新

    def on_tree_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        selected_item = selection[0]
        if selected_item:
            values = self.tree.item(selected_item, "values")
            self.entry_year.delete(0, tk.END)
            self.entry_year.insert(0, values[0])

            date = values[1]
            entry_date = "/".join(date.split("-")[1:])
            self.entry_date.delete(0, tk.END)
            self.entry_date.insert(0, entry_date)

            self.debit_account_var.set(values[2])
            self.credit_account_var.set(values[3])

            self.entry_amount.delete(0, tk.END)
            self.entry_amount.insert(0, values[4])

            self.entry_comment.delete(0, tk.END)
            self.entry_comment.insert(0, values[5])

    def tkraise(self, *args, **kwargs):
        """ページが表示されたときに勘定科目と仕訳を読み込む"""
        self.update_account_menus()
        self.load_journal_entries()
        super().tkraise(*args, **kwargs)
