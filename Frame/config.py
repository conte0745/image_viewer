import tkinter as tk
from PIL import Image

'''
Define global variable
'''
root : tk.Tk
size  = [650, 1000]
photo_canvases = [tk.Canvas] * 6
photo_imgs = [Image] * 6
photo_ids = [int] * 6
cnt_photos : int = 4
size_percent : float = 0.5
percent_label_strvar : tk.StringVar