import os
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

from . import config as cfg

class ImageViewFrame(ttk.Frame):
    def __init__(self, master=None, path=None, photo_idx=1):
        super().__init__(master)
        self.master = master
        self.photo_idx = photo_idx
        self._image_path = path
        self.init()

    def init(self):
        pil_img : Image
    
        if os.path.exists(self.image_path) \
            and self.image_path.lower().endswith(('.png', '.jpg', '.dng')):

            pil_img = Image.open(self.image_path)
            
            # min_size = min(cfg.size[0], cfg.size[1])
            cfg.size_percent = int(cfg.size[0] / pil_img.width * 100) / 100
            if cfg.cnt_photo % 2 == 0:
                cfg.size_percent /= 2
            elif cfg.cnt_photo % 3 == 0:
                cfg.size_percent /= 3


            pil_img = pil_img.resize(
                size=(int(pil_img.width*cfg.size_percent), int(pil_img.height*cfg.size_percent)),
            )
            self.canvas = tk.Canvas(self.master,
                width=pil_img.width,
                height=pil_img.height,
                name=f'img_canvas_row{self.photo_idx}'
                )
            cfg.photo_img[self.photo_idx-1] = ImageTk.PhotoImage(image=pil_img)
            cfg.percent_label_strvar.set(str(int(cfg.size_percent*100)))

            cfg.photo_id[self.photo_idx-1] = self.canvas.create_image(0, 
                0,
                image=cfg.photo_img[self.photo_idx-1],
                anchor='nw'
            ) 

            if 0 < cfg.cnt_photo < 4:
                self.canvas.grid(row=0, column=self.photo_idx-1)
            elif cfg.cnt_photo == 4:
                if 0 < self.photo_idx < 3:
                    self.canvas.grid(row=0, column=self.photo_idx-1, sticky=tk.W + tk.E + tk.N + tk.S)
                elif 3 <= self.photo_idx < 5:
                    self.canvas.grid(row=1, column=self.photo_idx-3, sticky=tk.W + tk.E + tk.N + tk.S)
            

            def update_canvas_size(e : tk.Event):

                # size_ = (int(pil_img.width*cfg.size_percent), int(pil_img.height*cfg.size_percent)),
                # print(size_)
                # canvas : tk.Canvas = e.widget
                # canvas.coords(cfg.photo_id[self.photo_idx-1], 0, 0 , size_[0], size_[1])
                print('Enter', e.x , e.y, e.widget)

            self.master.nametowidget(f'img_canvas_row{self.photo_idx}').bind('<Motion>', update_canvas_size)


        else:
            fail_label = ttk.Label(self.master, text='not exist')
            if 0 < cfg.cnt_photo < 4:
                fail_label.grid(row=0, column=self.photo_idx-1)
            elif cfg.cnt_photo == 4:
                if 0 < self.photo_idx < 3:
                    fail_label.grid(row=0, column=self.photo_idx-1, padx=0, pady=0)
                elif 3 <= self.photo_idx < 5:
                    fail_label.grid(row=1, column=self.photo_idx-3, padx=0, pady=0) 

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, current_path):
        self._image_path = current_path