import tkinter as tk
import tkinter.ttk as ttk

from Frame.TopRowFrame import TopRowFrame
from Frame.FileFrame import FileFrame
from Frame.ImageViewFrame import ImageViewFrame
from Frame.SearchFileFrame import SearchFileFrame
import Frame.config as cfg

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(f'{cfg.SIZE[0]}x{cfg.SIZE[1]}')
    root.title('Multi Simple Viewer')
    root.minsize(width=650, height=650)

    # search_file_frame = SearchFileFrame(master=root)
    # search_file_frame.pack()

    PATH = '/Users/takeuchiryouya/Code/image_viewer/canon.png'

    file_frame = ttk.Frame(master=root)
    top_row_frame = TopRowFrame(master=file_frame, num=cfg.cnt_photo)
    file_frame1 = FileFrame(master=file_frame, row=1)
    file_frame2 = FileFrame(master=file_frame, row=2)
    file_frame3 = FileFrame(master=file_frame, row=3)
    file_frame4 = FileFrame(master=file_frame, row=4)
    file_frame.pack(fill='x')

    images_frame = ttk.Frame(master=root)
    image_view_frame = ImageViewFrame(master=images_frame, path=PATH, num=1)
    image_view_frame2 = ImageViewFrame(master=images_frame, path=PATH, num=2)

    image_view_frame3 = ImageViewFrame(master=images_frame, path=PATH, num=3)
    image_view_frame4 = ImageViewFrame(master=images_frame, path=PATH, num=4)
    images_frame.pack(fill=tk.X, expand=True)
    root.mainloop()