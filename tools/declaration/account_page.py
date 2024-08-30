import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

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

        tk.Label(self, text="勘定科目の登録", font=("Helvetica", 16, "bold")).pack(pady=10)

        tk.Label(self, text="勘定科目名").pack()
        self.entry_name = tk.Entry(self)
        self.entry_name.pack()

        tk.Label(self, text="区分").pack()
        self.category_var = tk.StringVar(value=list(CATEGORY_OPTIONS.keys())[0])
        category_menu = ttk.OptionMenu(self, self.category_var, *CATEGORY_OPTIONS.keys())
        category_menu.pack()

        btn_add = tk.Button(self, text="追加", command=self.add_account_title)
        btn_add.pack(pady=5)

        btn_back = tk.Button(self, text="戻る", command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(pady=5)

        self.listbox_titles = tk.Listbox(self)
        self.listbox_titles.pack(pady=10, fill="both", expand=True)

        btn_delete = tk.Button(self, text="削除", command=self.delete_account_title)
        btn_delete.pack(pady=5)

        self.load_account_titles()

    def load_account_titles(self):
        """データベースから勘定科目を読み込んでリストボックスに表示する"""
        self.listbox_titles.delete(0, tk.END)
        conn = sqlite3.connect('accounting.db')
        c = conn.cursor()
        c.execute('SELECT name, category FROM account_titles')
        account_titles = c.fetchall()
        conn.close()

        for name, category in account_titles:
            category_text = [k for k, v in CATEGORY_OPTIONS.items() if v == category][0]
            self.listbox_titles.insert(tk.END, f"{name} ({category_text})")

    def add_account_title(self):
        name = self.entry_name.get()
        category_text = self.category_var.get()
        category = CATEGORY_OPTIONS.get(category_text)

        if not name or not category:
            messagebox.showerror("入力エラー", "すべてのフィールドを入力してください。")
            return

        conn = sqlite3.connect('accounting.db')
        c = conn.cursor()
        c.execute('INSERT INTO account_titles (name, category) VALUES (?, ?)', (name, category))
        conn.commit()
        conn.close()

        self.load_account_titles()  # 登録後にリストを更新

    def delete_account_title(self):
        selected = self.listbox_titles.curselection()
        if not selected:
            messagebox.showwarning("削除エラー", "削除する勘定科目を選択してください。")
            return

        conn = sqlite3.connect('accounting.db')
        c = conn.cursor()
        selected_text = self.listbox_titles.get(selected)
        name = selected_text.split(' ')[0]
        c.execute('DELETE FROM account_titles WHERE name = ?', (name,))
        conn.commit()
        conn.close()

        self.load_account_titles()  # 削除後にリストを更新
