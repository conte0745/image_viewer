import tkinter as tk
import tkinter.ttk as ttk
import logging as lg

from Frame.TopRowFrame import TopRowFrame
from Frame.FileFrame import FileFrame
from Frame.ImageViewFrame import ImageViewFrame
import Frame.config as cfg

class App(ttk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.root : tk.Tk = master
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

        self.root.title('Multi Simple Viewer')
        self.root.geometry(f'{cfg.size[0]}x{cfg.size[1]}+100+100')
        self.root.minsize(width=650, height=650)

        self.listbox_frame = tk.Frame(master=self.root)

        PATH = '/Users/takeuchiryouya/Code/image_viewer/tmp/canon.png'
        for i in range(cfg.cnt_photos):
            cfg.photo_path[i] = PATH
        cfg.photo_path[2] = "/Users/takeuchiryouya/Code/image_viewer/tmp/DSLR_00003.png"
        lg.info(cfg.photo_path)

        self.file_frames = ttk.Frame(master=self.root)
        self.image_frames = ttk.Frame(master=self.root)
        
        self.top_row_frame = TopRowFrame(master=self.file_frames, topapp=self, num=cfg.cnt_photos)

        self.file_frame = [FileFrame] * cfg.PHOTO_MAX_DHISPLAY
        self.image_frame = [ImageViewFrame] * cfg.PHOTO_MAX_DHISPLAY

        for i in range(cfg.cnt_photos):
            self.file_frame[i] = FileFrame(master=self.file_frames, listbox_frame=self.listbox_frame, path=cfg.photo_path[i], row=i+1)
            self.image_frame[i] = ImageViewFrame(master=self.image_frames, root=self.master, path=cfg.photo_path[i], photo_idx=i+1)

        self.file_frames.pack(fill=tk.X)
        self.listbox_frame.pack(fill=tk.X, padx=10)
        self.image_frames.pack(fill=tk.BOTH, pady=20, expand=True)

        self.root.bind('<KeyPress>', self.esc_pressed)

        self.root.mainloop()


    def update_image_frame(self, idx, path):
        self.image_frame[idx].image_path = path
        self.image_frame[idx].update_iamge(idx)

    def esc_pressed(self, e : tk.Event):
        if e.keysym == 'Escape':
            self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
