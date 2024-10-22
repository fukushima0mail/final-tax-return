import sqlite3


class DBConnection:
    def __init__(self):
        self.db_name = 'accounting.db'
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, *args, **kwargs):
        if exc_type is None:  # エラーが発生していない場合は commit
            self.conn.commit()
        
        self.conn.close()  # 接続を閉じる
