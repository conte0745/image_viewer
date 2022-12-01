import tkinter as tk
import tkinter.ttk as ttk

from Frame.TopRowFrame import TopRowFrame
from Frame.FileFrame import FileFrame
from Frame.ImageViewFrame import ImageViewFrame
from Frame.SearchFileFrame import SearchFileFrame
import Frame.config as cfg

def main():

    cfg.root = tk.Tk()

    cfg.root.title('Multi Simple Viewer')
    cfg.root.geometry(f'{cfg.size[0]}x{cfg.size[1]}')
    cfg.root.minsize(width=650, height=650)

    # search_file_frame = SearchFileFrame(master=root)
    # search_file_frame.pack()

    PATH = '/Users/takeuchiryouya/Code/image_viewer/canon.png'

    file_frames = ttk.Frame(master=cfg.root)
    image_frames = ttk.Frame(master=cfg.root)
    
    top_row_frame = TopRowFrame(master=file_frames, num=cfg.cnt_photos)

    file_frame = [FileFrame] * 6
    image_frame = [ImageViewFrame] * 6

    for i in range(cfg.cnt_photos):
        file_frame[i] = FileFrame(master=file_frames, row=i+1)
        image_frame[i] = ImageViewFrame(master=image_frames, path=PATH, photo_idx=i+1)

    file_frames.pack(fill='x')
    image_frames.pack(fill=tk.X, expand=True)

    cfg.root.bind('<KeyPress>', esc_pressed)

    cfg.root.mainloop()

    # Rfs5rkogtji54fiFRfGFAae

def esc_pressed(e : tk.Event):
    if e.keysym == 'Escape':
        cfg.root.destroy()

if __name__ == '__main__':
    main()
