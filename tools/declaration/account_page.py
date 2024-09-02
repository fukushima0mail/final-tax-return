from uuid import uuid4
import tkinter as tk
from tkinter import messagebox, ttk

from db.account_titles import (
    add_account, get_all_accounts,
    update_account, delete_account
)
from lib.utils import SortableTreeview

CATEGORY_OPTIONS = {
    "資産": 1,
    "負債": 2,
    "純資産": 3,
    "収益": 4,
    "費用": 5
}

class AccountPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="lightgray")

        # Title
        tk.Label(self, text="勘定科目の登録", font=("Helvetica", 16, "bold"), bg="lightgray").pack(pady=10)

        # TreeView to display account titles
        self.tree = SortableTreeview(self, columns=("Account Id", "Category", "Name", "BorrowingType", "Allocation"), show='headings', selectmode='browse')
        self.tree.column("Account Id", width=0, stretch=False, minwidth=0)
        self.tree.heading("Category", text="カテゴリー")
        self.tree.heading("Name", text="勘定科目名")
        self.tree.heading("BorrowingType", text="借貸区分")
        self.tree.heading("Allocation", text="按分 (%)")
        self.tree.pack(pady=10, fill="both", expand=True, padx=20)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Frame for input form
        form_frame = tk.Frame(self, bg="lightgray")
        form_frame.pack(padx=20, pady=10, fill="x")

        # Create input widgets
        self.create_input_widgets(form_frame)

        # Button frame for actions (similar layout as journal page)
        button_frame = tk.Frame(self, bg="lightgray")
        button_frame.pack(pady=10)

        # Add and delete buttons
        btn_add = ttk.Button(button_frame, text="追加", command=self.add_account_title)
        btn_add.pack(side="left", padx=5)

        btn_update = ttk.Button(button_frame, text="更新", command=self.update_account_title)
        btn_update.pack(side="left", padx=5)

        btn_delete = ttk.Button(button_frame, text="削除", command=self.delete_account_title)
        btn_delete.pack(side="left", padx=5)

        # Back button
        btn_back = ttk.Button(self, text="戻る", command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(pady=10)

        # Set default size for TreeView
        self.tree.config(height=15)

        self.load_account_titles()

    def create_input_widgets(self, parent):
        """Create input widgets arranged horizontally."""
        # Category
        tk.Label(parent, text="カテゴリー", bg="lightgray").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.category_var = tk.StringVar()
        self.category_menu = ttk.OptionMenu(parent, self.category_var, '', '資産', '負債', '純資産', '収益', '費用')
        self.category_menu.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Account Title Name
        tk.Label(parent, text="勘定科目名", bg="lightgray").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.entry_name = tk.Entry(parent, width=30)
        self.entry_name.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        # Borrowing Type (1 or -1)
        tk.Label(parent, text="借貸区分 (1/-1)", bg="lightgray").grid(row=0, column=4, padx=10, pady=5, sticky="e")
        self.entry_borrowing_type = tk.Entry(parent, width=10)
        self.entry_borrowing_type.grid(row=0, column=5, padx=10, pady=5, sticky="w")

        # Allocation (0-100)
        tk.Label(parent, text="按分 (%)", bg="lightgray").grid(row=0, column=6, padx=10, pady=5, sticky="e")
        self.entry_allocation = tk.Entry(parent, width=10)
        self.entry_allocation.grid(row=0, column=6, padx=10, pady=5, sticky="w")

    def load_account_titles(self):
        """データベースから勘定科目を読み込んでリストボックスに表示する"""
        self.tree.delete(*self.tree.get_children())  # Clear existing entries
        account_titles = get_all_accounts()

        for entry_id, account_id, name, category, borrowing_type, allocation in account_titles:
            category_text = [k for k, v in CATEGORY_OPTIONS.items() if v == category][0]
            self.tree.insert('', 'end', iid=entry_id, values=(account_id, name, category_text, borrowing_type, allocation))

    def add_account_title(self):
        account_id = str(uuid4())
        name = self.entry_name.get()
        category_text = self.category_var.get()
        category = CATEGORY_OPTIONS.get(category_text)
        borrowing_type = int(self.entry_borrowing_type.get())
        allocation = int(self.entry_allocation.get())

        if not name or not category:
            messagebox.showerror("入力エラー", "すべてのフィールドを入力してください。")
            return

        add_account(account_id, name, category, borrowing_type, allocation)

        self.load_account_titles()

    def update_account_title(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("選択エラー", "更新する勘定科目を選択してください。")
            return
        values = self.tree.item(selected_item[0], "values")

        account_id = values[0]
        name = self.entry_name.get()
        category_text = self.category_var.get()
        category = CATEGORY_OPTIONS.get(category_text)
        borrowing_type = int(self.entry_borrowing_type.get())
        allocation = int(self.entry_allocation.get())

        update_account(account_id, name, category, borrowing_type, allocation)

        self.load_account_titles()  # Refresh the list

    def delete_account_title(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("削除エラー", "削除する勘定科目を選択してください。")
            return
        values = self.tree.item(selected_item[0], "values")

        account_id = values[0]
        delete_account(account_id)

        self.load_account_titles()  # 削除後にリストを更新

    def on_tree_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        selected_item = selection[0]
        if selected_item:
            values = self.tree.item(selected_item, "values")
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, values[1])

            category = values[2]
            self.category_var.set(category)

            self.entry_borrowing_type.delete(0, tk.END)
            self.entry_borrowing_type.insert(0, values[3])

            self.entry_allocation.delete(0, tk.END)
            self.entry_allocation.insert(0, values[4])


def number_to_category(category_num):
    for key, value in CATEGORY_OPTIONS.items():
        if value == category_num:
            return key
    return ''