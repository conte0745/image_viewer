import os
import tkinter as tk
import tkinter.ttk as ttk
import logging as lg

from copy import deepcopy
from PIL import Image, ImageTk

from . import config as cfg

class ImageViewFrame(ttk.Frame):
    def __init__(self, master=None, root=None, path=None, photo_idx=1):
        super().__init__(master)
        self.master = master
        self.root = root
        self.photo_idx = photo_idx
        self.__image_path = path
        self.old_x = None
        self.old_y = None
        self.MAX_ZOOM = 3.0
        self.MIN_ZOOM = 0.01
        self.pil_img : list[Image.open, str, int] = [None, None, None]
        self.init_pil_img : list[Image.open, str, int] = [None, None, None]
        self.init()

    def init(self):
        is_exists_image = os.path.exists(self.__image_path)
        is_valid_ex = self.__image_path.lower().endswith(tuple(cfg.VALID_EX))
    
        if is_exists_image and is_valid_ex:
            self.init_pil_img[0] = Image.open(self.image_path)
            self.init_pil_img[1] = self.image_path
            self.init_pil_img[2] = self.photo_idx
            self.pil_img[1] = self.image_path
            self.pil_img[2] = self.photo_idx

            self.init_w = self.init_pil_img[0].width
            self.init_h = self.init_pil_img[0].height       
            self.resize_canvas()
            self.draw_image(self.photo_idx)
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
        if temp < self.MIN_ZOOM:
            return self.MIN_ZOOM
        elif temp >= self.MAX_ZOOM:
            return self.MAX_ZOOM
        return temp

    def click_img(self, e : tk.Event):
        self.old_x = e.x
        self.old_y = e.y
            
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

    def scale_img(self, e : tk.Event):
        delta = e.delta
        cfg.size_percent = self.calc_size_percent(cfg.size_percent, delta)
        cfg.percent_label_strvar.set(str(int(cfg.size_percent*100)))
        self.redraw_all_images()
        
    def update_all_frames(self, e:tk.Event):
        old_size = deepcopy(cfg.size)
        size_ = self.root.geometry().split('+') # get_format(100x100+200+200)
        cfg.size = [int(size_[0].split('x')[0]), int(size_[0].split('x')[1])]
        
        lg.info(" old : %s, new : %s", "x".join([str(i) for i in old_size]), "x".join([str(i) for i in cfg.size]))

        if old_size != cfg.size:
            lg.info("change")
            self.resize_canvas()
            self.redraw_all_images()
    
    def redraw_all_images(self):
        for idx in range(1, cfg.cnt_photos+1):
            self.image_path = cfg.photo_path[idx-1]
            self.draw_image(idx)
            self.set_bind(idx)

    def resize_canvas(self):
    
        # min_size = min(cfg.size[0], cfg.size[1])
        cfg.size_percent = int(cfg.size[0] / self.init_pil_img[0].width * 100) / 100
        cfg.percent_label_strvar.set(str(int(cfg.size_percent*100)))
        if cfg.cnt_photos % 2 == 0:
            cfg.size_percent /= 2
        elif cfg.cnt_photos % 3 == 0:
            cfg.size_percent /= 3

        self.canvas_h = cfg.size_percent * self.init_h
        self.canvas_w = cfg.size_percent * self.init_w

    def set_bind(self, idx):
        temp_widget : tk.Widget = self.master.nametowidget(f'img_canvas_row{idx}')
        temp_widget.bind('<ButtonPress>', self.click_img)
        temp_widget.bind('<Button1-Motion>', self.drag_img)
        temp_widget.bind('<MouseWheel>', self.scale_img)
        self.master.bind('<Configure>', self.update_all_frames)

    def draw_image(self, idx):
        lg.info("REDRAW")
        new_w = int(self.init_w*cfg.size_percent)
        new_h = int(self.init_h*cfg.size_percent)

        lg.info("index = %d", idx)
        lg.info(self.pil_img[1])
        lg.info(self.init_pil_img[1])
        lg.info(self.image_path)
        lg.info(cfg.photo_path[idx-1])

        if self.init_pil_img[1] != self.image_path:
            lg.info("diff")
            self.init_pil_img[0] = Image.open(self.image_path)
            self.init_pil_img[1] = self.image_path

        self.pil_img[0] = self.init_pil_img[0].resize(
            size=(new_w, new_h)
        )

        cfg.photo_canvases[idx-1] = tk.Canvas(self.master,
            width=self.canvas_w,
            height=self.canvas_h,
            name=f'img_canvas_row{idx}'
        )

        cfg.photo_canvases[idx-1].photo = ImageTk.PhotoImage(image=self.pil_img[0])
        cfg.photo_ids[idx-1] = cfg.photo_canvases[idx-1].create_image(
            self.canvas_w // 2,
            self.canvas_h // 2,
            image=cfg.photo_canvases[idx-1].photo,
            anchor='center',
        )

        if 0 < cfg.cnt_photos < 4:
            cfg.photo_canvases[idx-1].grid(row=0, column=idx-1)
        elif cfg.cnt_photos == 4:
            if 0 < idx < 3:
                cfg.photo_canvases[idx-1].grid(row=0, column=idx-1, sticky=tk.W + tk.E + tk.N + tk.S)
            elif 3 <= idx < 5:
                cfg.photo_canvases[idx-1].grid(row=1, column=idx-3, sticky=tk.W + tk.E + tk.N + tk.S)

    def update_iamge(self, idx):
        lg.info("--update--")
        self.init()

    @property
    def image_path(self):
        return self.__image_path

    @image_path.setter
    def image_path(self, current_path):
        self.__image_path = current_path