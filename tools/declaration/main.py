import tkinter as tk
from tkinter import ttk
from db.init import init_table
from start_page import StartPage
from account_page import AccountPage
from opening_balance_page import OpeningBalancePage
from journal_page import JournalPage
from general_page import GeneralLedgerPage
from balance_sheet_page import BalanceSheetPage


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("青色申告アプリ")
        self.geometry("1200x700")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.frames = {}
        for F in (StartPage, AccountPage, OpeningBalancePage, JournalPage, GeneralLedgerPage, BalanceSheetPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    init_table()
    app = Application()
    app.mainloop()
