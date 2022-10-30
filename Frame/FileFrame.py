# -*- coding: utf-8 -*-

import os
import tkinter as tk
import tkinter.ttk as ttk

import tkinter.filedialog as filedialog
from . import config as cfg

class FileFrame(ttk.Frame):
    def __init__(self, master=None, row=1):
        super().__init__(master)
        self.master = master
        self.row = row
        self.max_list_height = 10
        self.current_path = os.path.dirname(__file__)
        self.init()
        self.update_listbox(self.current_path)

    def init(self):
        vcmd = self.register(self.update_label)
        style = ttk.Style().configure('Entry', relief='flat')
        self.label = ttk.Label(self.master, text=f'PATH{self.row}:')
        self.value = tk.StringVar(value=self.current_path)
        self.is_exist_value = tk.StringVar(value="✅")
        self.entry = ttk.Entry(self.master,
            textvariable=self.value,
            validate='key',
            style=style,
            name=f'entry_row{self.row}',
            validatecommand=(vcmd, '%P', '%S'),
            )
        open_file_dialog_btn = ttk.Button(self.master, 
            text='select',
            name=f'open_file_dialog_btn_row{self.row}',
            command=self.open_file_dialog)
        is_exist_label = tk.Label(self.master, textvariable=self.is_exist_value, justify='center')
        self.label.grid(row=self.row, column=0)
        self.entry.grid(row=self.row, column=1,sticky=tk.EW)
        open_file_dialog_btn.grid(row=self.row, column=3)
        is_exist_label.grid(row=self.row, column=2)
        self.master.grid_columnconfigure(1, weight=1)

    def open_file_dialog(self):
        fTyp = [("", "*")]
        file_name = filedialog.askopenfilename(
            filetypes=fTyp,
            initialdir=self.current_path,
            )
        if len(file_name) > 1:
            self.value.set(file_name)
            self.is_exist_value.set('✅')

    def update_label(self, P, S):
        flag = True
        if os.path.exists(P):
            self.is_exist_value.set('✅')
        if not os.path.exists(P):
            self.is_exist_value.set('❌')

        # if S == '/':
        #     self.listbox.pack()

        return flag
    

    def update_listbox(self, dir):
        list_dir = os.listdir(dir)
        list_dir.insert(0, '..')
        strvar_list_dir = tk.StringVar(value=list_dir)
        self.listbox = tk.Listbox(self,
            #width=20,
            height=min(self.max_list_height, len(list_dir)),
            listvariable=strvar_list_dir,
            )
        self.listbox.bind('<<ListboxSelect>>', self.selected_listbox)
        self.listbox.pack()
        print(self.listbox)
    
    def selected_listbox(self, event):
        selected_index = self.listbox.curselection()
        selected_path = self.listbox.get(selected_index)

        if selected_path == '..':
            self.current_path = '/'.join(self.current_path.split('/')[:-1])
        else:
            self.current_path = os.path.join(self.current_path, selected_path)

        self.listbox.destroy()
        if not os.path.isfile(self.current_path):
            self.update_listbox(self.current_path)
        elif os.path.isfile(self.current_path):
            pass
    
    @property
    def current_path(self):
        return self._current_path

    @current_path.setter
    def current_path(self, current):
        self._current_path = current