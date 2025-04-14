import os
import shutil
import glob
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

default_x = 1600
default_y = 900
destination_directory = os.path.abspath('./tmp/')
defer_directory = os.path.abspath('./to_prc/')
initial_directory = 'E:/stable-diffusion-webui/outputs/txt2img-images/'
current_directory = ''
image_list = []
index = 0

def accept_image():
    global image_list
    global index
    if len(image_list) == 0:
        return
    shutil.copy(image_list[index], destination_directory)
    index = (index + 1) % len(image_list)
    display_image(root.winfo_width(), root.winfo_height())

def accept_handler(event):
    accept_image()

def defer_image():
    global image_list
    global index
    if len(image_list) == 0:
        return
    shutil.copy(image_list[index], defer_directory)
    index = (index + 1) % len(image_list)
    display_image(root.winfo_width(), root.winfo_height())

def defer_handler(event):
    defer_image()

def reject_image():
    global image_list
    global index
    if len(image_list) == 0:
        return
    index = (index + 1) % len(image_list)
    display_image(root.winfo_width(), root.winfo_height())

def reject_handler(event):
    reject_image()

def go_back(event):
    global image_list
    global index
    if len(image_list) == 0:
        return
    index = (index - 1) % len(image_list)
    display_image(root.winfo_width(), root.winfo_height())
    file_to_remove = os.path.join(destination_directory, os.path.basename(image_list[index]) )
    if os.path.isfile(file_to_remove):
        os.remove( file_to_remove )

def goto_end(event):
    global image_list
    global index
    if len(image_list) == 0:
        return
    index = -1 % len(image_list)
    display_image(root.winfo_width(), root.winfo_height())

def advance_10(event):
    global image_list
    global index
    if len(image_list) == 0:
        return
    index = (index + 10) % len(image_list)
    display_image(root.winfo_width(), root.winfo_height())

def retreat_10(event):
    global image_list
    global index
    if len(image_list) == 0:
        return
    index = (index - 10) % len(image_list)
    display_image(root.winfo_width(), root.winfo_height())

def resize_image(new_dims):
    global index
    global image_list
    with Image.open(image_list[index]) as im:
        im.thumbnail( new_dims, Image.Resampling.LANCZOS )
        return ImageTk.PhotoImage(im)

def display_image(newx, newy):
    nim = resize_image((newx, newy))
    image_frame.config(image=nim)
    image_frame.image = nim
    generate_image_list(current_directory, reset_index=False)

def update_image(event):
    global image_list
    if len(image_list) == 0:
        return
    display_image(root.winfo_width(), root.winfo_height())

def generate_image_list(fpath, reset_index=True):
    global image_list
    global index

    image_list = [ x for x in glob.glob( os.path.join(fpath, '*.png') ) ]
    if reset_index:
        index = 0
    selected_file_label.config(text=f'Current Image: {index} / {len(image_list) - 1}')

def reload_images_handler(event):
    reload_images()

def reload_images():
    global image_list
    if len(image_list) != 0:
        generate_image_list(current_directory, reset_index=False)

def open_file_dialog():
    global current_directory
    file_path = filedialog.askdirectory(title="Select a Folder", initialdir=initial_directory)
    if os.path.isdir(file_path):
        current_directory = file_path
        selected_folder_label.config(text=f"Selected Folder: {file_path}")
        generate_image_list(file_path)
        display_image(root.winfo_width(), root.winfo_height())

root = tk.Tk()
root.configure( background = '#1f1f1f' )
left = tk.Frame(root)
right = tk.Frame(root)
left.configure( background = '#1f1f1f' )
right.configure( background = '#1f1f1f' )
tl = tk.Frame(left)
bl = tk.Frame(left)
blr = tk.Frame(bl)
tl.configure( background = '#1f1f1f' )
bl.configure( background = '#1f1f1f' )
blr.configure( background = '#1f1f1f' )

left.pack(side=tk.LEFT)
tl.pack(side=tk.TOP)
bl.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
blr.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

root.title('Fuckass')
root.geometry(f'{default_x}x{default_y}')

root.bind("<Left>", reject_handler)
root.bind("<Right>", accept_handler)
root.bind("a", reject_handler)
root.bind("A", goto_end)
root.bind("d", accept_handler)
root.bind("D", defer_handler)
root.bind("<Up>", advance_10)
root.bind("<Down>", retreat_10)
root.bind("W", advance_10)
root.bind("S", retreat_10)
root.bind("<space>", go_back)
root.bind('<Configure>', update_image)
root.bind("r", reload_images_handler)

image_frame = tk.Label(right, image=None)
image_frame.configure( background = '#1f1f1f' )
image_frame.pack(fill=tk.BOTH, expand=True)

accept_button = tk.Button(blr, text='Accept ->', width=20, height=2, bg='green', fg='white', command=accept_image)
defer_button = tk.Button(blr, text='Defer ->', width=20, height=2, bg='orange', fg='white', command=defer_image)
reject_button = tk.Button(bl, text='<- Reject', width=20, height=2, bg='red', fg='white', command=reject_image)
open_button = tk.Button(tl, text="Open Folder", width=20, height=2, bg='antique white', command=open_file_dialog)
reload_button = tk.Button(tl, text="Reload", width=20, height=2, bg='antique white', command=reload_images)

accept_button.pack(side='top')
defer_button.pack(side='bottom')
reject_button.pack(side='left')
open_button.pack(padx=20, pady=20)
selected_folder_label = tk.Label(tl, text="Selected Folder:", bg='antique white')
selected_folder_label.pack()
selected_file_label = tk.Label(tl, text="Current Image:", bg='antique white')
selected_file_label.pack()
reload_button.pack(padx=20, pady=20)

with Image.open( os.path.abspath('./py/assets/icon.png') ) as icon_image:
    ico = ImageTk.PhotoImage(icon_image)
root.wm_iconphoto(False, ico)

root.mainloop()