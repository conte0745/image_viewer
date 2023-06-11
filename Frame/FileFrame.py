import os
import platform
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import logging as lg
from copy import deepcopy
from . import config as cfg

class FileFrame(ttk.Frame):
    def __init__(self, master=None, listbox_frame=None, path=None, row=1):
        super().__init__(master)
        self.master = master
        self.row = row
        self.max_list_height = 6
        self.listbox : tk.Listbox = None
        self.scroll : tk.Scrollbar = None
        self.listbox_frame : tk.Frame = listbox_frame
        self.strvar_list_dir : tk.StringVar = None
        self.prev_current_path = [".."]
        self.prev_idx = None
        cfg.photo_path[self.row-1] = path
        self.init()        

    def init(self):
        style = ttk.Style().configure('Entry', relief='flat')
        self.label = ttk.Label(self.master, text=f'PATH{self.row}:')
        self.value = tk.StringVar(value=cfg.photo_path[self.row-1])
        self.is_exist_value = tk.StringVar(value="✅")
        self.entry = ttk.Entry(self.master,
            textvariable=self.value,
            validate='key',
            style=style,
            name=f'entry_row{self.row}',
            )
        self.entry.bind("<FocusOut>", self.destroy_listbox)
        self.value.trace_add("write", self.callback)
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
        title = "Select compared image"

        fTyp = None
        if platform.system() == "Darwin":
            fTyp= [("Image file", ".png .jpg .jpeg")]
        else:
            fTyp = [("", "*.png")]

        file_name = filedialog.askopenfilename(
            title=title,
            filetypes=fTyp, 
            initialdir=cfg.default_dir,
            multiple=False
            )
    
        if len(file_name) > 0:
            self.value.set(file_name)
            self.update_label(file_name, None)


    def update_label(self, path):
        if os.path.exists(path) and path.lower().endswith(tuple(cfg.VALID_EX)):
            self.is_exist_value.set('✅')
        else:
            self.is_exist_value.set('❌')

    def callback(self, arg1, arg2, arg3):
        cfg.photo_path[self.row-1] = self.value.get()
        self.update_label(cfg.photo_path[self.row-1])
        self.create_listbox()


    def create_listbox(self):

        dir = cfg.photo_path[self.row-1]
        self.destroy_listbox(None)
        
        # pattern = ".+[^/]/"
        # repattern = re.compile(pattern)
        # if repattern.match(dir):
        #     dir = "/".join(dir.split("/")[:-1])

        if os.path.isdir("/".join(dir.split("/")[:-1])):
            list_dir = os.listdir("/".join(dir.split("/")[:-1]))
            list_dir.insert(0, '..')
            self.prev_current_path = deepcopy(list_dir)
        else:
            list_dir = self.prev_current_path
        
        self.scroll = tk.Scrollbar(self.listbox_frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        strvar_list_dir = tk.StringVar(value=list_dir)
        self.listbox = tk.Listbox(self.listbox_frame,
            width=20,
            height=min(self.max_list_height, len(list_dir)),
            listvariable=strvar_list_dir,
            yscrollcommand=self.scroll.set,
            relief="groove",
            bd=1,
            bg="#f5f5f5",
            takefocus=True
            )
        self.listbox.bind('<<ListboxSelect>>', self.selected_listbox)
        self.listbox.bind("<Motion>", self.change_color_listbox)

        self.listbox.pack(fill=tk.X)
        self.scroll.command = self.listbox.yview
        self.listbox_frame.pack(fill=tk.X, padx=10)

        lg.info(self.value.get())

    def change_color_listbox(self, event):
        idx = self.listbox.nearest(event.y)
        if idx != self.prev_idx and not self.prev_idx is None:
            self.listbox.itemconfig(self.prev_idx, bg="#f5f5f5")
        else:
            self.listbox.itemconfig(idx, bg="#87ceeb")
        self.prev_idx = deepcopy(idx)

    def selected_listbox(self, event):
        selected_index = self.listbox.curselection()
        selected_path = self.listbox.get(selected_index)

        if selected_path == '..':
            cfg.photo_path[self.row-1] = '/'.join(cfg.photo_path[self.row-1].split('/')[:-1])
        else:
            select = "/".join(cfg.photo_path[self.row-1].split("/")[:-1])
            cfg.photo_path[self.row-1] = os.path.join(select, selected_path)

        self.value.set(cfg.photo_path[self.row-1])
        

        if os.path.isfile(self.value.get()) or not os.path.exists(self.value.get()):
            self.listbox.destroy()
        if os.path.isdir(self.value.get()):
            cfg.photo_path[self.row-1] = cfg.photo_path[self.row-1] + "/"
            self.value.set(cfg.photo_path[self.row-1])
            self.create_listbox()

        idx = len(self.value.get())
        self.entry.icursor(idx)

    def destroy_listbox(self, event):
        if not self.listbox is None:
            self.listbox.destroy()
            self.scroll.destroy()
            self.listbox = None
        lg.info("out")
