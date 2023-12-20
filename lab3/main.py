from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import ttk
from tkinter.messagebox import showerror

import cv2
import numpy as np
from PIL import Image as Img
from PIL import ImageTk as ImgTk
#C:/Users/Lenovo/Pictures/Screenshots/Screenshot 2023-12-06 114051.png

def sharpness(img):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img = cv2.filter2D(img, -1, kernel)
    return img


def global_thresholdingOtsu(img):
    blur = cv2.GaussianBlur(img, (5, 5), 0)

    hist = cv2.calcHist([blur], [0], None, [256], [0, 256])
    hist_norm = hist.ravel() / hist.sum()
    Q = hist_norm.cumsum()

    bins = np.arange(256)

    fn_min = np.inf
    thresh = -1

    for i in range(1, 256):
        p1, p2 = np.hsplit(hist_norm, [i])
        q1, q2 = Q[i], Q[255] - Q[i]
        if q1 < 1.e-6 or q2 < 1.e-6:
            continue
        b1, b2 = np.hsplit(bins, [i])

        m1, m2 = np.sum(p1 * b1) / q1, np.sum(p2 * b2) / q2
        v1, v2 = np.sum(((b1 - m1) ** 2) * p1) / q1, np.sum(((b2 - m2) ** 2) * p2) / q2

        fn = v1 * q1 + v2 * q2
        if fn < fn_min:
            fn_min = fn
    thresh = i

    return thresh


def global_thresholding_Otsu(img):
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def adaptive1(img):
    mean_img = Img.fromarray(img).convert('L')
    arr2 = cv2.adaptiveThreshold(np.array(mean_img), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10)
    return arr2.astype(np.uint8)


def adaptive2(img):
    mean_img = Img.fromarray(img).convert('L')
    arr2 = cv2.adaptiveThreshold(np.array(mean_img), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 5)
    return arr2.astype(np.uint8)


filepath = ''


def get_image():
    global filepath
    filepath = ''
    filepath = filedialog.askopenfilename()
    if filepath == '':
        return
    file_path.delete(0, END)
    file_path.insert(INSERT, filepath)
    image = Img.open(filepath)
    global photo
    photo = ImgTk.PhotoImage(image.resize((500, 500)))
    image = canvas.create_image(0, 0, anchor='nw', image=photo)


def apply_filter():
    if filepath == '':
        showerror(title='Error', message='No file selected:(')
        return

    selected_filters = filter_listbox.curselection()
    if not selected_filters:
        showerror(title='Error', message='No filter selected:(')
        return

    selected_filter = filter_listbox.get(selected_filters[0])

    if selected_filter == "Original":
        image = canvas.create_image(0, 0, anchor='nw', image=photo)
    else:
        img = cv2.imread(filepath)
        if selected_filter == "Sharpening filter":
            sharpened_img = sharpness(img)
            sharpened_image = Img.fromarray(sharpened_img)
            global final1
            final1 = ImgTk.PhotoImage(sharpened_image.resize((500, 500)))
            image = canvas.create_image(0, 0, anchor='nw', image=final1)
        elif selected_filter == "Global thresholding 1":
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            user_threshold = simpledialog.askinteger('Input', 'Input threshold value', parent=root, initialvalue=0)
            ret, thresh1 = cv2.threshold(gray_img, user_threshold, 255, cv2.THRESH_BINARY)
            new_img = thresh1
            new_image = Img.fromarray(new_img)
            global final2
            final2 = ImgTk.PhotoImage(new_image.resize((500, 500)))
            image = canvas.create_image(0, 0, anchor='nw', image=final2)
        elif selected_filter == "Global thresholding 2":
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            user_threshold = simpledialog.askinteger('Input', 'Input threshold value', parent=root, initialvalue=0)
            ret, thresh1 = cv2.threshold(gray_img, user_threshold, 255, cv2.THRESH_TRUNC)
            new_img = thresh1
            new_image = Img.fromarray(new_img)
            global final3
            final3 = ImgTk.PhotoImage(new_image.resize((500, 500)))
            image = canvas.create_image(0, 0, anchor='nw', image=final3)
        elif selected_filter == "Adaptive thresholding 1":
            sharpened_img = adaptive1(img)
            sharpened_image = Img.fromarray(sharpened_img)
            global final5
            final5 = ImgTk.PhotoImage(sharpened_image.resize((500, 500)))
            image = canvas.create_image(0, 0, anchor='nw', image=final5)
        elif selected_filter == "Adaptive thresholding 2":
            sharpened_img = adaptive2(img)
            sharpened_image = Img.fromarray(sharpened_img)
            global final6
            final6 = ImgTk.PhotoImage(sharpened_image.resize((500, 500)))
            image = canvas.create_image(0, 0, anchor='nw', image=final6)
        elif selected_filter == "Otsu":
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            new_img = global_thresholding_Otsu(gray_img)
            new_image = Img.fromarray(new_img)
            global final7
            final7 = ImgTk.PhotoImage(new_image.resize((500, 500)))
            image = canvas.create_image(0, 0, anchor='nw', image=final7)


root = Tk()
root.title("Digital image processing")
root.geometry('800x600')
root.configure(bg='#0000FF')

# Кнопка выбора папки
btn_file_path = Button(root, text="Browse", command=get_image, width=10, bg='#FF0000', font=('Arial', 12, 'bold'),
                       foreground='#FFFFFF')  # Цвета Barbie
btn_file_path.grid(row=0, column=0, padx=20, pady=20, sticky=(W, E))

# Поле ввода папки
file_path = Entry(root, width=70, bg='#FF0000', font=('Arial', 12, 'bold'),
                  foreground='#FFFFFF')  # Белый текст и цвет фона как у кнопки
file_path.grid(row=0, column=1, padx=20, pady=20, sticky=(W, E))
file_path.insert(INSERT, "Select an image...")

# Меню слева
menu_frame = Frame(root, bg='#FFFF00')
menu_frame.grid(row=1, column=0, padx=15, pady=30, sticky=(N, S))

# Список фильтров
filter_listbox = Listbox(menu_frame, selectmode=SINGLE, font=('Arial', 10, 'bold'), foreground='#FFFFFF', bg='#00FF00',
                         selectbackground='#FF69B4', selectforeground='#FFFFFF')  # Голубой список
filter_listbox.pack(padx=20)

filters = ["Original", "Sharpening filter", "Global thresholding 1", "Global thresholding 2", "Adaptive thresholding 1",
           "Adaptive thresholding 2", "Otsu"]
for filter_name in filters:
    filter_listbox.insert(END, filter_name)

# Кнопка для применения фильтра
apply_button = Button(menu_frame, text="Apply Filter", command=apply_filter, width=15, bg='#FF0000',
                      font=('Arial', 12, 'bold'), foreground='#FFFFFF')  # Розовая кнопка
apply_button.pack(pady=20)

style = ttk.Style()
style.theme_use("default")

root.grid_rowconfigure(1, weight=1)

root.grid_columnconfigure(1, weight=1)

canvas = Canvas(root, height=500, width=500)
canvas.grid(row=1, column=1)

root.resizable(False, False)
root.mainloop()
