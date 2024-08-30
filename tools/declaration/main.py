import tkinter as tk
from tkinter import messagebox
import sqlite3

# データベースの接続とテーブルの作成
def init_db():
    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS account_titles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# データベースに勘定科目を追加
def add_account_title():
    code = entry_code.get()
    name = entry_name.get()
    category = entry_category.get()

    if not code or not name or not category:
        messagebox.showerror("入力エラー", "すべてのフィールドを入力してください。")
        return

    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO account_titles (code, name, category) VALUES (?, ?, ?)', (code, name, category))
        conn.commit()
        listbox.insert(tk.END, f"{code}: {name} ({category})")
    except sqlite3.IntegrityError:
        messagebox.showerror("エラー", "勘定科目コードが重複しています。")
    finally:
        conn.close()

# Tkinterウィンドウのセットアップ
root = tk.Tk()
root.title("勘定科目管理")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="勘定科目コード").grid(row=0, column=0)
entry_code = tk.Entry(frame_input)
entry_code.grid(row=0, column=1)

tk.Label(frame_input, text="勘定科目名").grid(row=1, column=0)
entry_name = tk.Entry(frame_input)
entry_name.grid(row=1, column=1)

tk.Label(frame_input, text="区分").grid(row=2, column=0)
entry_category = tk.Entry(frame_input)
entry_category.grid(row=2, column=1)

btn_add = tk.Button(root, text="追加", command=add_account_title)
btn_add.pack(pady=5)

listbox = tk.Listbox(root)
listbox.pack(pady=10, fill=tk.BOTH, expand=True)

# アプリ起動時にデータベースを初期化
init_db()

root.mainloop()
