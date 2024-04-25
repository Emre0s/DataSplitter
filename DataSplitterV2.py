import os
import shutil
import tkinter as tk
from tkinter import filedialog
import random

def count_files(directory):
    return len(os.listdir(directory))

def update_dataset_info():
    global dataset_dir, total_files
    dataset_dir = filedialog.askdirectory()
    if dataset_dir:
        total_files = count_files(os.path.join(dataset_dir, "images"))
        info_label.config(text=f"Toplam Dosya Sayısı: {total_files}")

def split_dataset():
    if not dataset_dir:
        return

    image_dir = os.path.join(dataset_dir, "images")
    label_dir = os.path.join(dataset_dir, "labels")
    train_dir = os.path.join(dataset_dir, "train")
    valid_dir = os.path.join(dataset_dir, "valid")

    if not os.path.exists(train_dir):
        os.makedirs(os.path.join(train_dir, "images"))
        os.makedirs(os.path.join(train_dir, "labels"))
    if not os.path.exists(valid_dir):
        os.makedirs(os.path.join(valid_dir, "images"))
        os.makedirs(os.path.join(valid_dir, "labels"))

    if split_option.get() == "Yüzde":
        train_ratio = int(split_value.get()) / 100.0
        train_size = int(total_files * train_ratio)
    else:
        train_size = int(split_value.get())

    image_files = os.listdir(image_dir)
    random.shuffle(image_files)

    train_data = random.sample(image_files, train_size)
    valid_data = [file for file in image_files if file not in train_data]

    for file in train_data:
        src_img = os.path.join(image_dir, file)
        dst_img = os.path.join(train_dir, "images", file)
        shutil.copy(src_img, dst_img)

        src_lbl = os.path.join(label_dir, os.path.splitext(file)[0] + ".txt")
        dst_lbl = os.path.join(train_dir, "labels", os.path.splitext(file)[0] + ".txt")
        shutil.copy(src_lbl, dst_lbl)

    for file in valid_data:
        src_img = os.path.join(image_dir, file)
        dst_img = os.path.join(valid_dir, "images", file)
        shutil.copy(src_img, dst_img)

        src_lbl = os.path.join(label_dir, os.path.splitext(file)[0] + ".txt")
        dst_lbl = os.path.join(valid_dir, "labels", os.path.splitext(file)[0] + ".txt")
        shutil.copy(src_lbl, dst_lbl)

    result_label.config(text="Veri seti başarıyla bölündü.")

root = tk.Tk()
root.title("Veri Seti Ayırıcı")

dataset_dir = ""
total_files = 0

dataset_label = tk.Label(root, text="Veri Seti Dizini:")
dataset_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

select_button = tk.Button(root, text="Dizin Seç", command=update_dataset_info)
select_button.grid(row=0, column=1, padx=5, pady=5)

info_label = tk.Label(root, text="")
info_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

split_option = tk.StringVar()
split_option.set("Yüzde")

split_option_label = tk.Label(root, text="Bölme Seçeneği:")
split_option_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

split_option_menu = tk.OptionMenu(root, split_option, "Yüzde", "Sayı")
split_option_menu.grid(row=2, column=1, padx=5, pady=5)

split_value_label = tk.Label(root, text="Train Değeri:")
split_value_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

split_value = tk.Entry(root)
split_value.grid(row=3, column=1, padx=5, pady=5)

split_button = tk.Button(root, text="Veri Setini Ayır", command=split_dataset)
split_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

result_label = tk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
