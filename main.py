import tkinter as tk
import tkinter.ttk as ttk
import logging as lg

from Frame.TopRowFrame import TopRowFrame
from Frame.FileFrame import FileFrame
from Frame.ImageViewFrame import ImageViewFrame
import Frame.config as cfg

class App():

    def __init__(self):
        self.file_frames : ttk.Frame
        self.image_frames : ttk.Frame
        self.top_row_frame : TopRowFrame
        self.listbox_frame : tk.Frame
        self.file_frames : list
        self.image_frames : list


    def mainloop(self):
        # lg.basicConfig(filename="log/viewer.log", encoding="utf-8", level=lg.DEBUG)
        lg.basicConfig(level=lg.INFO)
        lg.info("start")

        cfg.root = tk.Tk()

        cfg.root.title('Multi Simple Viewer')
        cfg.root.geometry(f'{cfg.size[0]}x{cfg.size[1]}')
        cfg.root.minsize(width=650, height=650)

        self.listbox_frame = tk.Frame(master=cfg.root)

        PATH = '/Users/takeuchiryouya/Code/image_viewer/tmp/canon.png'
        for i in range(cfg.cnt_photos):
            cfg.photo_path[i] = PATH

        self.file_frames = ttk.Frame(master=cfg.root)
        self.image_frames = ttk.Frame(master=cfg.root)
        
        self.top_row_frame = TopRowFrame(master=self.file_frames, topapp=self, num=cfg.cnt_photos)

        self.file_frame = [FileFrame] * cfg.PHOTO_MAX_DHISPLAY
        self.image_frame = [ImageViewFrame] * cfg.PHOTO_MAX_DHISPLAY

        for i in range(cfg.cnt_photos):
            self.file_frame[i] = FileFrame(master=self.file_frames, listbox_frame=self.listbox_frame, row=i+1)
            self.image_frame[i] = ImageViewFrame(master=self.image_frames, path=cfg.photo_path[i], photo_idx=i+1)

        self.file_frames.pack(fill=tk.X)
        self.listbox_frame.pack(fill=tk.X, padx=10)
        self.image_frames.pack(fill=tk.BOTH, pady=20, expand=True)

        cfg.root.bind('<KeyPress>', self.esc_pressed)

        cfg.root.mainloop()


    def update_image_frame(self, idx, path):
        lg.info("update")
        self.image_frame[idx].image_path = path
        self.image_frame[idx].update_iamge()

    def esc_pressed(self, e : tk.Event):
        if e.keysym == 'Escape':
            cfg.root.destroy()

if __name__ == '__main__':
    app = App()
    app.mainloop()
