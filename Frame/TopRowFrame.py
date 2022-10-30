from . import config as cfg
import tkinter as tk
import tkinter.ttk as ttk

class TopRowFrame(ttk.Frame):
    def __init__(self, master=None, num=1):
        super().__init__(master)
        self.master = master
        self.num_entry = num
        self.max_entry = 4
        self.grid(row=0, column=0)
        self.create_top_row()

    def create_top_row(self):
        WIDTH = 8
        btn_frame = ttk.Frame(self.master)
        add_btn = ttk.Button(btn_frame, text='+', command=self.add_entry, width=WIDTH)
        sub_btn = ttk.Button(btn_frame, text='-', command=self.sub_entry, width=WIDTH)
        show_btn = ttk.Button(btn_frame, text='show', command='', width=WIDTH)
        show_window_btn = ttk.Button(btn_frame, text='show window', command='', width=WIDTH+1)
        save_btn = ttk.Button(btn_frame, text='save', command='', width=WIDTH)
        self.num_var = tk.StringVar(value='表示数:' + str(self.num_entry))
        num_label = tk.Label(btn_frame, textvariable=self.num_var, width=WIDTH)
        percent_label_strvar = tk.StringVar(btn_frame, value='サイズ:' + str(cfg.size_percent) + '%')
        percent_label = tk.Label(btn_frame, textvariable=percent_label_strvar, width=WIDTH)

        add_btn.pack(side='left')
        sub_btn.pack(side='left')
        num_label.pack(side='left')
        show_window_btn.pack(side='right')
        show_btn.pack(side='right')
        save_btn.pack(side='right')
        percent_label.pack(side='right')
        btn_frame.grid(row=0, columnspan=7, sticky=tk.EW)

    def add_entry(self):
        if self.num_entry < self.max_entry:
            self.num_entry += 1
            self.num_var.set('表示数 : ' + str(self.num_entry))
            cfg.cnt_photo = self.num_entry
            #self.update()

    def sub_entry(self):
        if self.num_entry > 1:
            self.num_entry -= 1
            self.num_var.set('表示数 : ' + str(self.num_entry))
            cfg.cnt_photo = self.num_entry
            #self.update()
