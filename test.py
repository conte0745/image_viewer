# -*- coding: utf-8 -*-

import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

from PIL import Image, ImageTk

class ImageViewFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self._image_path = '/Users/takeuchiryouya/Code/lab/Deep_White_Balance/result/dataset/Set2_output_images_WBDM/Mobile_00535.png'

        self.init()

    def init(self):
        global photo_img
        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(expand = True, fill = tk.BOTH)
        pil_img = Image.open(self.image_path)
        photo_img = ImageTk.PhotoImage(image=pil_img)
        # self.update()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        self.canvas.create_image(
            canvas_width / 2,
            canvas_height / 2,                   
            image=photo_img
            ) 

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, current):
        self._image_path = current

class SearchFileFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self._num_entry = 0
        self.max_list_height = 10
        self._current_path = os.getcwd()
        self.set_label()

    def set_label(self):
        current_path_label_str = self.current_path[1:].replace('/', ' > ')
        self.current_path_strvar = tk.StringVar(self, current_path_label_str)
        self.current_path_label = ttk.Label(self, textvariable=self.current_path_strvar, relief=tk.SOLID)
        self.current_path_label.pack()
        self.update_combobox(self.current_path)

    def update_combobox(self, dir):
        list_dir = os.listdir(dir)
        list_dir.insert(0, '..')
        strvar_list_dir = tk.StringVar(value=list_dir)
        value = tk.StringVar()
        self.combobox = ttk.Combobox(self,
            #width=20,
            height=min(self.max_list_height, len(list_dir)), 
            textvariable=value,
            values=strvar_list_dir,
            )
        self.combobox.bind("<<ComboboxSelected>>", self.selected_combobox)
        self.combobox.pack(side='left')
    
    def selected_combobox(self, event):
        selected_path = self.combobox.get()

        if selected_path == '..':
            self.current_path = '/'.join(self.current_path.split('/')[:-1])
        else:
            self.current_path = os.path.join(self.current_path, selected_path)

        self.combobox.destroy()
        current_path_label_str = self.current_path[1:].replace('/', ' > ')
        self.current_path_strvar.set(current_path_label_str)
        if not os.path.isfile(self.current_path):
            self.update_combobox(self.current_path)
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
            self.update()
            print('add', self.num_entry)
    def sub_entry(self):
        if self.num_entry > 0:
            self.num_entry -= 1
            self.update()
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

class FileFrame(ttk.Frame):
    def __init__(self, master=None, row=0):
        super().__init__(master)
        self.master = master
        self.row = row
        self.current_path = os.path.dirname(__file__)
        self.init()

    def init(self):
        vcmd = self.register(self.update_label)
        style = ttk.Style().configure('Entry', relief='flat')
        self.label = ttk.Label(self.master, text=f'PATH{self.row}')
        self.value = tk.StringVar(value=self.current_path)
        self.is_exit_value = tk.StringVar(value="✅")
        self.entry = ttk.Entry(self.master,
            textvariable=self.value,
            validate='focusout',
            style=style,
            validatecommand=(vcmd, '%P'),
            invalidcommand=self.failure_update_label
            )
        btn = ttk.Button(self.master, text="select", command=self.open_file_dialog)
        is_exit_label = tk.Label(self.master, textvariable=self.is_exit_value, justify='center')
        self.label.grid(row=self.row, column=0)
        self.entry.grid(row=self.row, column=1,sticky=tk.EW)
        btn.grid(row=self.row, column=3)
        is_exit_label.grid(row=self.row, column=2)
        self.master.grid_columnconfigure(1, weight=1)

    def open_file_dialog(self):
        fTyp = [("", "*")]
        file_name = filedialog.askopenfilename(
            filetypes=fTyp,
            initialdir=self.current_path,
            )
        if len(file_name) > 1:
            self.value.set(file_name)
            self.is_exit_value.set('✅')

    def update_label(self, P):
        if os.path.exists(P):
            self.is_exit_value.set('✅')
            return True
        else:
            return False
    
    def failure_update_label(self):
        self.is_exit_value.set('❌')
    
    @property
    def current_path(self):
        return self._current_path

    @current_path.setter
    def current_path(self, current):
        self._current_path = current

class TopRowFrame(ttk.Frame):
    def __init__(self, master=None, num=1):
        super().__init__(master)
        self.master = master
        self.num_entry = num
        self.max_entry = 6
        self.grid(row=0, column=0)
        self.create_top_row()

    def create_top_row(self):
        btn_frame = ttk.Frame(self.master)
        add_btn = ttk.Button(btn_frame, text='+', command=self.add_entry)
        sub_btn = ttk.Button(btn_frame, text='-', command=self.sub_entry)
        show_btn = ttk.Button(btn_frame, text='show', command='')
        show_window_btn = ttk.Button(btn_frame, text='show window', command='')
        save_btn = ttk.Button(btn_frame, text='save', command='')
        self.num_var = tk.StringVar(value=str(self.num_entry))
        num_label = tk.Label(btn_frame, textvariable=self.num_var)

        add_btn.pack(side='left')
        sub_btn.pack(side='left')
        num_label.pack(side='left')
        show_btn.pack(side='left')
        show_window_btn.pack(side='left')
        save_btn.pack(side='left')
        btn_frame.grid(row=0, columnspan=2, sticky=tk.EW)

    def add_entry(self):
        if self.num_entry < self.max_entry - 1:
            self.num_entry += 1
            self.num_var.set(str(self.num_entry))
            self.update()

    def sub_entry(self):
        if self.num_entry > 1:
            self.num_entry -= 1
            self.num_var.set(str(self.num_entry))
            self.update()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('800x600')
    root.title('Multi Simple Viewer')
    root.minsize(width=650, height=650)

    # search_file_frame = SearchFileFrame(master=root)
    # search_file_frame.pack()

    file_frame = ttk.Frame(master=root)
    top_row_frame = TopRowFrame(master=file_frame, num=2)
    file_frame1 = FileFrame(master=file_frame, row=1)
    file_frame2 = FileFrame(master=file_frame, row=2)
    file_frame.pack(fill='x')

    image_view_frame = ImageViewFrame(master=root)
    image_view_frame.pack()
    root.mainloop()