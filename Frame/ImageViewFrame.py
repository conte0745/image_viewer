import os
import tkinter as tk
import tkinter.ttk as ttk
import threading
from PIL import Image, ImageTk

from . import config as cfg

class ImageViewFrame(ttk.Frame):
    def __init__(self, master=None, path=None, photo_idx=1):
        super().__init__(master)
        self.master = master
        self.photo_idx = photo_idx
        self._image_path = path
        self.old_x = None
        self.old_y = None
        self.init()

    def init(self):
        pil_img : Image
    
        if os.path.exists(self.image_path) \
            and self.image_path.lower().endswith(('.png', '.jpg', '.dng')):

            pil_img = Image.open(self.image_path)
            
            # min_size = min(cfg.size[0], cfg.size[1])
            cfg.size_percent = int(cfg.size[0] / pil_img.width * 100) / 100
            if cfg.cnt_photos % 2 == 0:
                cfg.size_percent /= 2
            elif cfg.cnt_photos % 3 == 0:
                cfg.size_percent /= 3


            pil_img = pil_img.resize(
                size=(int(pil_img.width*cfg.size_percent), int(pil_img.height*cfg.size_percent)),
            )
            cfg.photo_canvases[self.photo_idx-1] = tk.Canvas(self.master,
                width=pil_img.width,
                height=pil_img.height,
                name=f'img_canvas_row{self.photo_idx}'
                )
            cfg.photo_imgs[self.photo_idx-1] = ImageTk.PhotoImage(image=pil_img)
            cfg.percent_label_strvar.set(str(int(cfg.size_percent*100)))

            cfg.photo_ids[self.photo_idx-1] = cfg.photo_canvases[self.photo_idx-1].create_image(0,
                0,
                image=cfg.photo_imgs[self.photo_idx-1],
                anchor='nw'
            ) 

            if 0 < cfg.cnt_photos < 4:
                cfg.photo_canvases[self.photo_idx-1].grid(row=0, column=self.photo_idx-1)
            elif cfg.cnt_photos == 4:
                if 0 < self.photo_idx < 3:
                    cfg.photo_canvases[self.photo_idx-1].grid(row=0, column=self.photo_idx-1, sticky=tk.W + tk.E + tk.N + tk.S)
                elif 3 <= self.photo_idx < 5:
                    cfg.photo_canvases[self.photo_idx-1].grid(row=1, column=self.photo_idx-3, sticky=tk.W + tk.E + tk.N + tk.S)
            

            def click_img(e : tk.Event):
                self.old_x = e.x
                self.old_y = e.y
                print(f'click {e.widget}')
            
            def drag_img(e : tk.Event):
                new_x = e.x
                new_y = e.y

                thread = [None] * 4
                for i in range(cfg.cnt_photos):
                    thread[i] = threading.Thread(target=move_img, args=(new_x, new_y, i))
                
                for i in range(cfg.cnt_photos):
                    thread[i].start()

                self.old_x = new_x
                self.old_y = new_y

            def move_img(new_x, new_y, idx):
                cfg.photo_canvases[idx].move(
                    cfg.photo_ids[idx],
                    new_x - self.old_x,
                    new_y - self.old_y
                )

            temp_widget : tk.Widget = self.master.nametowidget(f'img_canvas_row{self.photo_idx}')
            temp_widget.bind('<ButtonPress>', click_img)
            temp_widget.bind('<Button1-Motion>', drag_img)

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