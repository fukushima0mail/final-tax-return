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

# データベースの接続とテーブルの作成
def init_db():
    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS account_titles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category SMALLINT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            date TEXT NOT NULL,
            debit_account_id INTEGER NOT NULL,
            credit_account_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            FOREIGN KEY(debit_account_id) REFERENCES account_titles(id),
            FOREIGN KEY(credit_account_id) REFERENCES account_titles(id)
        )
    ''')

    conn.commit()
    conn.close()

# メインアプリクラス
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("青色申告アプリ")
        self.geometry("400x400")

        self.frames = {}
        for F in (StartPage, AccountPage, JournalPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# スタートページ
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="メニュー", font=("Helvetica", 18, "bold")).pack(pady=20)

        btn_account = tk.Button(self, text="勘定科目の登録",
                                command=lambda: controller.show_frame("AccountPage"))
        btn_account.pack(pady=10)

        btn_journal = tk.Button(self, text="仕訳の入力",
                                command=lambda: controller.show_frame("JournalPage"))
        btn_journal.pack(pady=10)

# 勘定科目登録ページ
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
        self.listbox_titles.insert(tk.END, f"{name} ({category_text})")
        conn.close()

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
        self.listbox_titles.delete(selected)

# 仕訳入力ページ
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
        self.update_account_menu(self.debit_account_var)

        tk.Label(self, text="貸方勘定科目").pack()
        self.credit_account_var = tk.StringVar()
        self.update_account_menu(self.credit_account_var)

        tk.Label(self, text="金額").pack()
        self.entry_amount = tk.Entry(self)
        self.entry_amount.pack()

        btn_add = tk.Button(self, text="追加", command=self.add_journal_entry)
        btn_add.pack(pady=5)

        btn_back = tk.Button(self, text="戻る", command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(pady=5)

        self.listbox_journal = tk.Listbox(self)
        self.listbox_journal.pack(pady=10, fill="both", expand=True)

    def update_account_menu(self, var):
        conn = sqlite3.connect('accounting.db')
        c = conn.cursor()
        c.execute('SELECT name FROM account_titles')
        account_titles = [row[0] for row in c.fetchall()]
        conn.close()

        if account_titles:
            var.set(account_titles[0])

        menu = ttk.OptionMenu(self, var, *account_titles)
        menu.pack()

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
            date = f"{year}-{month:02d}-{day:02d}"
        else:
            date = f"{year + 1}-{month:02d}-{day:02d}"

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

        self.listbox_journal.insert(tk.END, f"{year}/{date_text}: {debit_account_name} -> {credit_account_name} {amount}円")

# アプリケーションを起動
if __name__ == "__main__":
    init_db()
    app = Application()
    app.mainloop()
