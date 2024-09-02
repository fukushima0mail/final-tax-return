from tkinter import ttk


class SortableTreeview(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # カラムヘッダをクリックしたときのイベントをバインド
        self.heading('#0', text=self.heading('#0')['text'], command=lambda: self.sort_column('#0', False))
        for col in self['columns']:
            self.heading(col, text=self.heading(col)['text'], command=lambda _col=col: self.sort_column(_col, False))

    def sort_column(self, col, reverse):
        # カラムに基づいてツリーアイテムを取得し、ソート
        items = [(self.set(k, col), k) for k in self.get_children('')]
        items.sort(reverse=reverse)

        # ソートされた順番で再配置
        for index, (val, k) in enumerate(items):
            self.move(k, '', index)

        # 次回のクリックで逆順にソート
        self.heading(col, command=lambda: self.sort_column(col, not reverse))
