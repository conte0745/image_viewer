import os
import tkinter as tk
import tkinter.ttk as ttk

from . import config as cfg

class SearchFileFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self._num_entry = 0
        self.max_list_height = 10
        self.__max_entry = 4
        self._current_path = os.getcwd()
        self.set_label()
        

    def set_label(self):
        current_path_label_str = self.current_path[1:].replace('/', ' > ')
        self.current_path_strvar = tk.StringVar(self, current_path_label_str)
        self.current_path_label = ttk.Label(self, textvariable=self.current_path_strvar, relief=tk.SOLID)
        self.current_path_label.pack()
        self.update_listbox(self.current_path)

    def update_listbox(self, dir):
        list_dir = os.listdir(dir)
        list_dir.insert(0, '..')
        strvar_list_dir = tk.StringVar(value=list_dir)
        self.listbox = tk.Listbox(self,
            #width=20,
            height=min(self.max_list_height, len(list_dir)), 
            values=strvar_list_dir,
            )
        self.listbox.bind("<<listboxSelected>>", self.selected_listbox)
        self.listbox.pack(side='left')
    
    def selected_listbox(self, event):
        selected_path = self.listbox.get()

        if selected_path == '..':
            self.current_path = '/'.join(self.current_path.split('/')[:-1])
        else:
            self.current_path = os.path.join(self.current_path, selected_path)

        self.listbox.destroy()
        if not os.path.isfile(self.current_path):
            self.update_listbox(self.current_path)
        elif os.path.isfile(self.current_path) and \
            (self.current_path.split('.')[-1].lower() in {'png', 'jpg'}):
            pass

    def create_inc_btn(self):
        btn_frame = ttk.Frame(self.master)
        add_btn = ttk.Button(btn_frame, text='+', command=self.add_entry)
        sub_btn = ttk.Button(btn_frame, text='-', command=self.sub_entry)
        add_btn.pack(side=tk.LEFT)
        sub_btn.pack(side=tk.LEFT)
        btn_frame.pack(fill='x')

    def add_entry(self):
        if self.num_entry < self.__max_entry - 1:
            self.num_entry += 1
            print('add', self.num_entry)
    def sub_entry(self):
        if self.num_entry > 0:
            self.num_entry -= 1
            print('sub', self.num_entry)

    @property
    def current_path(self):
        return self._current_path

    @current_path.setter
    def current_path(self, current):
        self._current_path = current

    @property
    def num_entry(self):
        return self._num_entry

    @num_entry.setter
    def num_entry(self, num):
        self._num_entry = num