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
        self.old_x = None
        self.old_y = None
        self.init()

    def init(self):
        self.pil_img : Image
    
        if os.path.exists(self.image_path) \
            and self.image_path.lower().endswith(('.png', '.jpg', '.dng')):

            self.init_pil_img = Image.open(self.image_path)
            self.init_h = self.init_pil_img.height
            self.init_w = self.init_pil_img.width
            
            self.resize_canvas()
            self.draw(self.photo_idx)
            self.set_bind(self.photo_idx)

        else:
            fail_label = ttk.Label(self.master, text='not exist')
            if 0 < cfg.cnt_photos < 4:
                fail_label.grid(row=0, column=self.photo_idx-1)
            elif cfg.cnt_photos == 4:
                if 0 < self.photo_idx < 3:
                    fail_label.grid(row=0, column=self.photo_idx-1, padx=0, pady=0)
                elif 3 <= self.photo_idx < 5:
                    fail_label.grid(row=1, column=self.photo_idx-3, padx=0, pady=0) 

    def calc_size_percent(self, size_percent, delta):
        temp = size_percent + float(delta) / 100
        if temp < 0.01:
            return 0.01
        elif temp >= 3.0:
            return 3.0
        else:
            return temp

    def click_img(self, e : tk.Event):
        self.old_x = e.x
        self.old_y = e.y
        print(f'click {e.widget}')
            
    def drag_img(self, e : tk.Event):
        new_x = e.x
        new_y = e.y

        for i in range(cfg.cnt_photos):
            self.move_img(new_x, new_y, i)

        self.old_x = new_x
        self.old_y = new_y

    def move_img(self, new_x, new_y, idx):
        cfg.photo_canvases[idx].move(
            cfg.photo_ids[idx],
            new_x - self.old_x,
            new_y - self.old_y
        )

    def mouse_wheel(self, e : tk.Event):
        delta = e.delta
        cfg.size_percent = self.calc_size_percent(cfg.size_percent, delta)
        print(f'{cfg.size_percent} %')

        for idx in range(cfg.cnt_photos):
            self.draw(idx+1)
            self.set_bind(idx+1)
        
    def resize_all_frame(self, _):
        size_ = cfg.root.geometry().split('+')[0] # get_format(100x100+200x200)
        cfg.size = [int(size_.split('x')[0]), int(size_.split('x')[1])]

    def resize_canvas(self):
    
        # min_size = min(cfg.size[0], cfg.size[1])
        cfg.size_percent = int(cfg.size[0] / self.init_pil_img.width * 100) / 100
        if cfg.cnt_photos % 2 == 0:
            cfg.size_percent /= 2
        elif cfg.cnt_photos % 3 == 0:
            cfg.size_percent /= 3

        self.canvas_h = cfg.size_percent * self.init_h
        self.canvas_w = cfg.size_percent * self.init_w

        print(self.canvas_h, self.canvas_w)

    def set_bind(self, idx):
        temp_widget : tk.Widget = self.master.nametowidget(f'img_canvas_row{idx}')
        temp_widget.bind('<ButtonPress>', self.click_img)
        temp_widget.bind('<Button1-Motion>', self.drag_img)
        temp_widget.bind('<MouseWheel>', self.mouse_wheel)
        cfg.root.bind('<Configure>', self.resize_all_frame)

    def draw(self, idx):
        new_w = int(self.init_w*cfg.size_percent)
        new_h = int(self.init_h*cfg.size_percent)
        self.pil_img = self.init_pil_img.resize(
            size=(new_w, new_h)
        )
        cfg.photo_canvases[idx-1] = tk.Canvas(self.master,
            width=self.canvas_w,
            height=self.canvas_h,
            name=f'img_canvas_row{idx}',
        )
        cfg.photo_imgs[idx-1] = ImageTk.PhotoImage(image=self.pil_img)
        cfg.percent_label_strvar.set(str(int(cfg.size_percent*100)))

        cfg.photo_ids[idx-1] = cfg.photo_canvases[idx-1].create_image(
            self.canvas_w // 2,
            self.canvas_h // 2,
            image=cfg.photo_imgs[idx-1],
            anchor='center'
        ) 

        if 0 < cfg.cnt_photos < 4:
            cfg.photo_canvases[idx-1].grid(row=0, column=idx-1)
        elif cfg.cnt_photos == 4:
            if 0 < idx < 3:
                cfg.photo_canvases[idx-1].grid(row=0, column=idx-1, sticky=tk.W + tk.E + tk.N + tk.S)
            elif 3 <= idx < 5:
                cfg.photo_canvases[idx-1].grid(row=1, column=idx-3, sticky=tk.W + tk.E + tk.N + tk.S)

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, current_path):
        self._image_path = current_path