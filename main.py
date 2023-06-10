import tkinter as tk
import tkinter.ttk as ttk
import logging as lg

from Frame.TopRowFrame import TopRowFrame
from Frame.FileFrame import FileFrame
from Frame.ImageViewFrame import ImageViewFrame
# from Frame.SearchFileFrame import SearchFileFrame
import Frame.config as cfg

def main():
    # lg.basicConfig(filename="log/viewer.log", encoding="utf-8", level=lg.DEBUG)
    lg.basicConfig(level=lg.INFO)

    cfg.root = tk.Tk()

    cfg.root.title('Multi Simple Viewer')
    cfg.root.geometry(f'{cfg.size[0]}x{cfg.size[1]}')
    cfg.root.minsize(width=650, height=650)

    listbox_frame = tk.Frame(master=cfg.root)

    PATH = '/Users/takeuchiryouya/Code/image_viewer/tmp/canon.png'

    file_frames = ttk.Frame(master=cfg.root)
    image_frames = ttk.Frame(master=cfg.root)
    
    top_row_frame = TopRowFrame(master=file_frames, num=cfg.cnt_photos)

    file_frame = [FileFrame] * cfg.PHOTO_MAX_DHISPLAY
    image_frame = [ImageViewFrame] * cfg.PHOTO_MAX_DHISPLAY

    for i in range(cfg.cnt_photos):
        file_frame[i] = FileFrame(master=file_frames, listbox_frame=listbox_frame, row=i+1)
        image_frame[i] = ImageViewFrame(master=image_frames, path=PATH, photo_idx=i+1)

    file_frames.pack(fill=tk.X)
    listbox_frame.pack(fill=tk.X, padx=10)
    image_frames.pack(fill=tk.BOTH, pady=20, expand=True)

    cfg.root.bind('<KeyPress>', esc_pressed)

    cfg.root.mainloop()

    # Rfs5rkogtji54fiFRfGFAae

def esc_pressed(e : tk.Event):
    if e.keysym == 'Escape':
        cfg.root.destroy()

if __name__ == '__main__':
    main()
