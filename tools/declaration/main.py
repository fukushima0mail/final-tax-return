import tkinter as tk
from db.init import init_table
from start_page import StartPage
from general_page import GeneralLedgerPage
from account_page import AccountPage
from journal_page import JournalPage

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("青色申告アプリ")
        self.geometry("1200x700")

        self.frames = {}
        for F in (StartPage, AccountPage, JournalPage, GeneralLedgerPage):
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
