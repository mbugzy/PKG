from colorsys import rgb_to_hls, hls_to_rgb
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from tkinter import *
from tkinter import colorchooser
from tkinter.messagebox import showerror,showwarning

win = Tk()
win.title('rgb-hls-lab')
win.geometry('600x600+200+200')
win.minsize(320, 400)
for c in range(6): win.columnconfigure(index=c, weight=1)
win.rowconfigure(index=0, weight=4)
win.rowconfigure(index=1, weight=1)
for r in range(2, 6): win.rowconfigure(index=r, weight=2)

def rgb_to_lab(r, g, b):
    rgb = sRGBColor(r / 255, g / 255, b / 255)
    lab = convert_color(rgb, LabColor)
    slidersLAB[0].set(lab.lab_l)
    slidersLAB[1].set(lab.lab_a)
    slidersLAB[2].set(lab.lab_b)
    square.configure(bg='#{:02X}{:02X}{:02X}'.format(int(slidersRGB[0].get()), int(slidersRGB[1].get()),
                                                     int(slidersRGB[2].get())))
    setEntries()

def rgbChanges(q):
    if whichColors.get() == 'RGB' or q == 1000:
        h, l, s = rgb_to_hls(slidersRGB[0].get() / 255, slidersRGB[1].get() / 255, slidersRGB[2].get() / 255)
        slidersHLS[0].set(h * 360)
        slidersHLS[1].set(l * 100)
        slidersHLS[2].set(s * 100)
        rgb_to_lab(slidersRGB[0].get(), slidersRGB[1].get(), slidersRGB[2].get())


def hslChanges(q):
    if whichColors.get() == 'HSL':
        r, g, b = hls_to_rgb(slidersHLS[0].get() / 360, slidersHLS[1].get() / 100, slidersHLS[2].get() / 100)
        slidersRGB[0].set(r * 255)
        slidersRGB[1].set(g * 255)
        slidersRGB[2].set(b * 255)
        rgb_to_lab(slidersRGB[0].get(), slidersRGB[1].get(), slidersRGB[2].get())


def labChanges(q):
    if whichColors.get() == 'LAB':
        lab = LabColor(slidersLAB[0].get(), slidersLAB[1].get(), slidersLAB[2].get())
        rgb = convert_color(lab, sRGBColor)
        r, g, b = rgb.get_upscaled_value_tuple()
        slidersRGB[0].set(r)
        slidersRGB[1].set(g)
        slidersRGB[2].set(b)
        h, l, s = rgb_to_hls(r / 255, g / 255, b / 255)
        slidersHLS[0].set(h * 360)
        slidersHLS[1].set(l * 100)
        slidersHLS[2].set(s * 100)
        setEntries()
        square.configure(bg='#{:02X}{:02X}{:02X}'.format(int(slidersRGB[0].get()), int(slidersRGB[1].get()),
                                                         int(slidersRGB[2].get())))


def setEntries():
    values1 = [int(v.get()) for v in slidersRGB]
    values2 = [int(v.get()) for v in slidersHLS]
    values3 = [int(v.get()) for v in slidersLAB]
    for i in range(3):
        txtRGB[i].delete(0, END)
        txtHSL[i].delete(0, END)
        txtLAB[i].delete(0, END)
        txtRGB[i].insert(0, str(values1[i]))
        txtHSL[i].insert(0, str(values2[i]))
        txtLAB[i].insert(0, str(values3[i]))


def getNum(q):
    try:
        for i in range(3):
            for j in range(3):
                if int(txts[i][j].get()) > sliders[i][j]['to']:
                    showwarning('invalid','too much, it will set to max')
                    txts[i][j].delete(0, END)
                    txts[i][j].insert(0, str(int(sliders[i][j]['to'])))
        for i in range(3):
            slidersRGB[i].set(int(txtRGB[i].get()))
            slidersHLS[i].set(int(txtHSL[i].get()))
            slidersLAB[i].set(int(txtLAB[i].get()))
    except ValueError:
        showerror('invalid', 'only numbers')
        setEntries()


def sl(w=0, e=255, t=rgbChanges):
    return Scale(orient=HORIZONTAL, from_=w, to=e, length=100, command=t)


slidersRGB = [sl(), sl(), sl()]
slidersHLS = [sl(e=360, t=hslChanges), sl(e=100, t=hslChanges), sl(e=100, t=hslChanges)]
slidersLAB = [sl(e=100, t=labChanges), sl(-128, 127, labChanges), sl(-128, 127, labChanges)]
sliders = [slidersRGB, slidersHLS, slidersLAB]
for i in range(3):
    slidersRGB[i].grid(column=0, row=i + 3)
    slidersHLS[i].grid(column=2, row=i + 3)
    slidersLAB[i].grid(column=4, row=i + 3)

txtRGB = []
txtHSL = []
txtLAB = []
txts = [txtRGB, txtHSL, txtLAB]
for j, txt in enumerate(txts):
    for i in range(3):
        txt.append(Entry(width=10))
        txt[i].insert(0, '0')
        txt[i].grid(column=(j * 2) + 1, row=i + 3)
        txt[i].bind('<Return>', getNum)

square = Canvas(height=200, width=400, bg='black')
square.grid(columnspan=6, column=0, row=0)

whichColors = StringVar()
btns = ['RGB', 'HSL', 'LAB']

for i, btn in enumerate(btns):
    newbtn = Radiobutton(text=btn, value=btn, variable=whichColors)
    newbtn.grid(row=2, column=i * 2, columnspan=2)
    # newbtn.configure(command=choose)
    newbtn.select()
    # choose()


def colorPalette():
    square.configure(bg=colorchooser.askcolor(initialcolor=square['bg'])[1])
    r, g, b = square.winfo_rgb(square['bg'])
    slidersRGB[0].set(r / 256)
    slidersRGB[1].set(g / 256)
    slidersRGB[2].set(b / 256)
    rgbChanges(1000)


Button(text='Choose color', command=colorPalette, width=50).grid(column=0, row=1, columnspan=6)

win.mainloop()
