import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# 区分の選択肢とその数値マッピング
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

    # 勘定科目テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS account_titles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category SMALLINT NOT NULL
        )
    ''')
    
    # 仕訳テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            date TEXT NOT NULL,
            debit_account_id INTEGER NOT NULL,
            debit_amount INTEGER NOT NULL,
            credit_account_id INTEGER NOT NULL,
            credit_amount INTEGER NOT NULL,
            FOREIGN KEY(debit_account_id) REFERENCES account_titles(id),
            FOREIGN KEY(credit_account_id) REFERENCES account_titles(id)
        )
    ''')

    conn.commit()
    conn.close()

# データベースに勘定科目を追加
def add_account_title():
    name = entry_name.get()
    category_text = category_var.get()
    category = CATEGORY_OPTIONS.get(category_text)

    if not name or not category:
        messagebox.showerror("入力エラー", "すべてのフィールドを入力してください。")
        return

    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    c.execute('INSERT INTO account_titles (name, category) VALUES (?, ?)', (name, category))
    conn.commit()
    listbox_titles.insert(tk.END, f"{name} ({category_text})")
    conn.close()

# 勘定科目を削除
def delete_account_title():
    selected = listbox_titles.curselection()
    if not selected:
        messagebox.showwarning("削除エラー", "削除する勘定科目を選択してください。")
        return

    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    selected_text = listbox_titles.get(selected)
    name = selected_text.split(' ')[0]  # 名前部分のみを取得
    c.execute('DELETE FROM account_titles WHERE name = ?', (name,))
    conn.commit()
    conn.close()
    listbox_titles.delete(selected)

# 仕訳データをデータベースに保存
def add_journal_entry():
    year = int(entry_year.get())
    date_text = entry_date.get()
    debit_account_name = debit_account_var.get()
    debit_amount = int(entry_debit_amount.get())
    credit_account_name = credit_account_var.get()
    credit_amount = int(entry_credit_amount.get())

    if not year or not date_text or not debit_account_name or not credit_account_name:
        messagebox.showerror("入力エラー", "すべてのフィールドを入力してください。")
        return

    # 日付のフォーマット
    month, day = map(int, date_text.split('/'))
    if 4 <= month <= 12:
        date = f"{year}-{month:02d}-{day:02d}"
    else:
        date = f"{year + 1}-{month:02d}-{day:02d}"

    # 勘定科目IDを取得
    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    
    c.execute('SELECT id FROM account_titles WHERE name = ?', (debit_account_name,))
    debit_account_id = c.fetchone()[0]

    c.execute('SELECT id FROM account_titles WHERE name = ?', (credit_account_name,))
    credit_account_id = c.fetchone()[0]

    # データベースに仕訳を追加
    c.execute('''
        INSERT INTO journal_entries 
        (year, date, debit_account_id, debit_amount, credit_account_id, credit_amount) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (year, date, debit_account_id, debit_amount, credit_account_id, credit_amount))

    conn.commit()
    conn.close()

    listbox_journal.insert(tk.END, f"{year}/{date_text}: {debit_account_name} {debit_amount} -> {credit_account_name} {credit_amount}")

# Tkinterウィンドウのセットアップ
root = tk.Tk()
root.title("青色申告アプリ")

# 勘定科目登録セクション
frame_account = tk.LabelFrame(root, text="勘定科目の登録")
frame_account.pack(pady=10, padx=10, fill="x")

tk.Label(frame_account, text="勘定科目名").grid(row=0, column=0)
entry_name = tk.Entry(frame_account)
entry_name.grid(row=0, column=1)

tk.Label(frame_account, text="区分").grid(row=1, column=0)
category_var = tk.StringVar(value=list(CATEGORY_OPTIONS.keys())[0])
category_menu = ttk.OptionMenu(frame_account, category_var, *CATEGORY_OPTIONS.keys())
category_menu.grid(row=1, column=1)

btn_add_title = tk.Button(frame_account, text="追加", command=add_account_title)
btn_add_title.grid(row=2, columnspan=2, pady=5)

listbox_titles = tk.Listbox(frame_account)
listbox_titles.grid(row=3, columnspan=2, pady=10, sticky="nsew")

btn_delete_title = tk.Button(frame_account, text="削除", command=delete_account_title)
btn_delete_title.grid(row=4, columnspan=2, pady=5)

# 仕訳入力セクション
frame_journal = tk.LabelFrame(root, text="仕訳の入力")
frame_journal.pack(pady=10, padx=10, fill="x")

# 年度入力
tk.Label(frame_journal, text="年度").grid(row=0, column=0)
entry_year = tk.Entry(frame_journal)
entry_year.grid(row=0, column=1)

# 日付入力
tk.Label(frame_journal, text="日付 (MM/DD)").grid(row=1, column=0)
entry_date = tk.Entry(frame_journal)
entry_date.grid(row=1, column=1)

# 借方勘定科目選択
tk.Label(frame_journal, text="借方勘定科目").grid(row=2, column=0)
debit_account_var = tk.StringVar(value="資産")
debit_account_menu = ttk.OptionMenu(frame_journal, debit_account_var, *CATEGORY_OPTIONS.keys())
debit_account_menu.grid(row=2, column=1)

# 借方金額入力
tk.Label(frame_journal, text="借方金額").grid(row=3, column=0)
entry_debit_amount = tk.Entry(frame_journal)
entry_debit_amount.grid(row=3, column=1)

# 貸方勘定科目選択
tk.Label(frame_journal, text="貸方勘定科目").grid(row=4, column=0)
credit_account_var = tk.StringVar(value="負債")
credit_account_menu = ttk.OptionMenu(frame_journal, credit_account_var, *CATEGORY_OPTIONS.keys())
credit_account_menu.grid(row=4, column=1)

# 貸方金額入力
tk.Label(frame_journal, text="貸方金額").grid(row=5, column=0)
entry_credit_amount = tk.Entry(frame_journal)
entry_credit_amount.grid(row=5, column=1)

# 仕訳追加ボタン
btn_add_journal = tk.Button(frame_journal, text="追加", command=add_journal_entry)
btn_add_journal.grid(row=6, columnspan=2, pady=10)

# 仕訳リスト表示
listbox_journal = tk.Listbox(frame_journal)
listbox_journal.grid(row=7, columnspan=2, pady=10, sticky="nsew")

# アプリ起動時にデータベースを初期化
init_db()

root.mainloop()
