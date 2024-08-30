import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

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
    c.execute('''
        CREATE TABLE IF NOT EXISTS account_titles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category SMALLINT NOT NULL
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
    listbox.insert(tk.END, f"{name} ({category_text})")
    conn.close()

# 勘定科目を削除
def delete_account_title():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("削除エラー", "削除する勘定科目を選択してください。")
        return

    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    selected_text = listbox.get(selected)
    name = selected_text.split(' ')[0]  # 名前部分のみを取得
    c.execute('DELETE FROM account_titles WHERE name = ?', (name,))
    conn.commit()
    conn.close()
    listbox.delete(selected)

# Tkinterウィンドウのセットアップ
root = tk.Tk()
root.title("勘定科目管理")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="勘定科目名").grid(row=0, column=0)
entry_name = tk.Entry(frame_input)
entry_name.grid(row=0, column=1)

tk.Label(frame_input, text="区分").grid(row=1, column=0)
category_var = tk.StringVar(value=list(CATEGORY_OPTIONS.keys())[0])
category_menu = ttk.OptionMenu(frame_input, category_var, *CATEGORY_OPTIONS.keys())
category_menu.grid(row=1, column=1)

btn_add = tk.Button(root, text="追加", command=add_account_title)
btn_add.pack(pady=5)

listbox = tk.Listbox(root)
listbox.pack(pady=10, fill=tk.BOTH, expand=True)

btn_delete = tk.Button(root, text="削除", command=delete_account_title)
btn_delete.pack(pady=5)

# アプリ起動時にデータベースを初期化
init_db()

root.mainloop()
