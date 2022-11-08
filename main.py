import tkinter as tk
import tkinter.ttk as ttk

from Frame.TopRowFrame import TopRowFrame
from Frame.FileFrame import FileFrame
from Frame.ImageViewFrame import ImageViewFrame
from Frame.SearchFileFrame import SearchFileFrame
import Frame.config as cfg

root : tk.Tk

def main():
    global root
    root = tk.Tk()

    root.title('Multi Simple Viewer')
    root.geometry(f'{cfg.size[0]}x{cfg.size[1]}')
    root.minsize(width=650, height=650)

    # search_file_frame = SearchFileFrame(master=root)
    # search_file_frame.pack()

    PATH = '/Users/takeuchiryouya/Code/image_viewer/canon.png'

    file_frames = ttk.Frame(master=root)
    image_frames = ttk.Frame(master=root)
    
    top_row_frame = TopRowFrame(master=file_frames, num=cfg.cnt_photo)

    file_frame = [FileFrame] * 6
    image_frame = [ImageViewFrame] * 6

    for i in range(cfg.cnt_photo):
        file_frame[i] = FileFrame(master=file_frames, row=i+1)
        image_frame[i] = ImageViewFrame(master=image_frames, path=PATH, photo_idx=i+1)

    file_frames.pack(fill='x')
    image_frames.pack(fill=tk.X, expand=True)

    root.bind('<KeyPress>', esc_pressed)
    root.bind('<Configure>', update_main_frame_size)

    root.mainloop()

    # Rfs5rkogtji54fiFRfGFAae

def esc_pressed(e : tk.Event):
    global root
    print(e.keysym)
    if e.keysym == 'Escape':
        root.destroy()

def update_main_frame_size(e : tk.Event):
    global root
    size_ = root.geometry().split('+')[0] # get(100x100+200x200)
    cfg.size = [int(size_.split('x')[0]), int(size_.split('x')[1])]

if __name__ == '__main__':
    main()
