import tkinter as tk
from PIL import Image

'''
Define global variable
'''

root : tk.Tk
size  = [650, 1000]
PHOTO_MAX_DHISPLAY = 6
photo_canvases = [tk.Canvas] * PHOTO_MAX_DHISPLAY
photo_imgs = [Image] * PHOTO_MAX_DHISPLAY
photo_ids = [int] * PHOTO_MAX_DHISPLAY
photo_path = [str] * PHOTO_MAX_DHISPLAY
cnt_photos : int = 4
size_percent : float = 0.5
percent_label_strvar : tk.StringVar

VALID_EX = {".jpg", ".jpeg", ".png", ".dng"}
default_dir = "."
