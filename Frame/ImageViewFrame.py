import os
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

from . import config as cfg

class ImageViewFrame(ttk.Frame):
    def __init__(self, master=None, path=None, num=1):
        super().__init__(master)
        self.master = master
        self.num = num
        self._image_path = path
        self.init()

    def init(self):
        pil_img : Image
    
        if os.path.exists(self.image_path) \
            and self.image_path.lower().endswith(('.png','.jpg')):
            pil_img = Image.open(self.image_path)
            pil_img = pil_img.resize(
                size=(pil_img.width*cfg.size_percent//100, pil_img.height*cfg.size_percent//100),
            )
            self.canvas = tk.Canvas(self.master, 
                width=pil_img.width,
                height=pil_img.height,
                name=f'img_canvas_row{self.num}'
                )
            cfg.photo_img[self.num-1] = ImageTk.PhotoImage(image=pil_img)

            self.canvas.create_image(0, 
                0,
                image=cfg.photo_img[self.num-1],
                anchor='nw'
            ) 

            if 0 < cfg.cnt_photo < 4:
                self.canvas.grid(row=0, column=self.num-1)
            elif cfg.cnt_photo == 4:
                if 0 < self.num < 3:
                    self.canvas.grid(row=0, column=self.num-1, sticky=tk.W + tk.E + tk.N + tk.S)
                elif 3 <= self.num < 5:
                    self.canvas.grid(row=1, column=self.num-3, sticky=tk.W + tk.E + tk.N + tk.S) 
        else:
            fail_label = ttk.Label(self.master, text='not exist')
            if 0 < cfg.cnt_photo < 4:
                fail_label.grid(row=0, column=self.num-1)
            elif cfg.cnt_photo == 4:
                if 0 < self.num < 3:
                    fail_label.grid(row=0, column=self.num-1, padx=0, pady=0)
                elif 3 <= self.num < 5:
                    fail_label.grid(row=1, column=self.num-3, padx=0, pady=0) 

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, current_path):
        self._image_path = current_path