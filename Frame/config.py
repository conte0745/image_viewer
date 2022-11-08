import tkinter as tk
from PIL import Image

'''
Define global variable
'''
root : tk.Tk
size  = [650, 1000]
photo_img = [Image] * 6
photo_id = [int] * 6
cnt_photo : int = 4
size_percent : float = 0.5
percent_label_strvar : tk.StringVar