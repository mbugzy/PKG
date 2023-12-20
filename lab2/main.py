import os
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import tkinter.ttk as ttk

win = Tk()
win.title('Выбор папки')
win.geometry('400x400')
win.resizable(width=False, height=False)


def show_table():
    # Создаем Treeview виджет для отображения таблицы
    global win2, df
    win2 = Tk()
    win2.title('Таблица с информацией')
    win2.geometry('1200x600')
    table = ttk.Treeview(win2,
                         columns=['Image name', 'Image size (px)', 'Resolution (dpi)', 'Depth of color', 'Compression'],
                         height=300)
    table.heading('#1', text='Image name')
    table.heading('#2', text='Image size (px)')
    table.heading('#3', text='Resolution (dpi)')
    table.heading('#4', text='Depth of color')
    table.heading('#5', text='Compression')
    table.column('#1', width=200, stretch=False)
    table.column('#2', width=200, stretch=False)
    table.column('#3', width=200, stretch=False)
    table.column('#4', width=200, stretch=False)
    table.column('#5', width=200, stretch=False)

    # Вставляем данные из DataFrame в таблицу
    for index, row in df.iterrows():
        values = row.tolist()
        table.insert('', 'end', values=values)

    table.pack()
    win2.protocol("WM_DELETE_WINDOW", ifSave)
    win2.mainloop()

def dict_ask():
    global folder_path, image_info_list, df
    folder_path = filedialog.askdirectory()
    image_info_list = find_images_in_directory(folder_path)
    df = pd.DataFrame(image_info_list)

    win.destroy()
    show_table()


def ifSave():
    close = messagebox.askyesno('Сохранить?', 'Желаете сохранить информацию?', )
    if close:
        ask_save()
    win2.destroy()


def ask_save():
    global df
    save_file = filedialog.asksaveasfile(defaultextension='.csv')
    df.to_csv(save_file, index=True, sep=';', encoding='utf-8')


Button(text='Выберите папку с изображениями', width=100, height=50, command=dict_ask).pack()


# Рекурсивная функция для поиска изображений в папке и подпапках
def find_images_in_directory(directory_path):
    global image_info_list
    for root, _, files in os.walk(directory_path):
        for filename in files:
            # Полный путь к файлу
            file_path = os.path.join(root, filename)

            # Проверяем, что это изображение
            if os.path.isfile(file_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                # Открываем изображение с помощью Pillow
                img = Image.open(file_path)

                # Создаем отдельные переменные для каждой информации
                image_name = filename
                image_size = img.size
                image_dpi = img.info.get('dpi')
                image_mode = img.mode
                image_compression = img.info.get('compression', 'N/A')

                # Добавляем информацию в список
                image_info_list.append({
                    'Image name': image_name,
                    'Image size (px)': image_size,
                    'Resolution (dpi)': image_dpi,
                    'Depth of color': image_mode,
                    'Compression': image_compression
                })

    return image_info_list


# Путь к папке с изображениями
# folder_path = 'D:/Programming/1.Python/DataSets/animals'
# folder_path = 'D:/Screenshots
folder_path = ''
# Получаем информацию об изображениях
image_info_list = []
df = None
win2 = None

win.mainloop()
