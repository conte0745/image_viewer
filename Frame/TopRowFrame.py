import os
import tkinter as tk
import tkinter.ttk as ttk
import logging as lg
import re

from . import config as cfg

class TopRowFrame(ttk.Frame):
    def __init__(self, master=None, topapp=None, num=1):
        super().__init__(master)
        self.master = master
        self.topapp = topapp
        self.num_entry = num
        self.max_entry = 4
        self.grid(row=0, column=0)
        self.create_top_row()

    def create_top_row(self):

        def integer_only(P, S):
            if re.match('\D', S):
                return False
            if P == '0' or P == '' or int(P) > 10000:
                return False
            cfg.size_percent = int(P) / 100
            return True

        WIDTH = 8
        btn_frame = ttk.Frame(self.master)
        tcl_integer_only = btn_frame.register(integer_only)
        add_btn = ttk.Button(btn_frame, text='+', command=self.add_entry, width=WIDTH)
        sub_btn = ttk.Button(btn_frame, text='-', command=self.sub_entry, width=WIDTH)
        show_btn = ttk.Button(btn_frame, text='show', command=self.show_btn_tapped, width=WIDTH)
        show_window_btn = ttk.Button(btn_frame, text='show window', command='', width=WIDTH+1)
        save_btn = ttk.Button(btn_frame, text='save', command=self.save_btn_tapped, width=WIDTH)
        self.num_var = tk.StringVar(value='表示数:' + str(self.num_entry))
        num_label = tk.Label(btn_frame, textvariable=self.num_var, width=WIDTH)
        size_label = tk.Label(btn_frame, text='サイズ')
        percent_label = tk.Label(btn_frame, text='%')
        cfg.percent_label_strvar = tk.StringVar(btn_frame, value=str(int(cfg.size_percent*100)))
        percent_spinbox = tk.Spinbox(btn_frame,
            from_=1,
            to=10000,
            increment=1,
            textvariable=cfg.percent_label_strvar,
            validate='all',
            validatecommand=(tcl_integer_only, '%P', '%S'),
            width=WIDTH)

        add_btn.pack(side='left')
        sub_btn.pack(side='left')
        num_label.pack(side='left')
        show_window_btn.pack(side='right')
        show_btn.pack(side='right')
        save_btn.pack(side='right')
        percent_label.pack(side='right')
        percent_spinbox.pack(side='right')
        size_label.pack(side='right')
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
    
    def show_btn_tapped(self):
        lg.info("tapped")
        for i in range(cfg.cnt_photos):
            if os.path.exists(cfg.photo_path[i]):
                self.topapp.update_image_frame(i, cfg.photo_path[i])
            else:
                lg.info("image file not exists")

    def save_btn_tapped(self):
        lg.info("¥n----canvas----")
        lg.info(cfg.photo_canvases)
        lg.info("¥n----id----")
        lg.info(cfg.photo_ids)
        lg.info("¥n----image----")
        lg.info(cfg.photo_imgs)
        lg.info("¥n----path----")
        lg.info(cfg.photo_path)