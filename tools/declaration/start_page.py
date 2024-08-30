import tkinter as tk

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
