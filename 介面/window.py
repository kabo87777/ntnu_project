from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("1572x947")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 947,
    width = 1572,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)


canvas.create_rectangle(
    231, 3, 231+1341, 3+947,
    fill = "#222831",
    outline = "")


canvas.create_rectangle(
    0, -1, 0+231, -1+947,
    fill = "#eeeeee",
    outline = "")


canvas.create_rectangle(
    1092, 669, 1092+460, 669+230,
    fill = "#c4c4c4",
    outline = "")


canvas.create_rectangle(
    1092, 297, 1092+460, 297+338,
    fill = "#c4c4c4",
    outline = "")


canvas.create_rectangle(
    388, 669, 388+681, 669+230,
    fill = "#c4c4c4",
    outline = "")

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    887.0, 42.0,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#eeeeee",
    highlightthickness = 0)

entry0.place(
    x = 750.0, y = 19,
    width = 274.0,
    height = 44)

canvas.create_text(
    726.5, 135.0,
    text = "2330",
    fill = "#fd7014",
    font = ("None", int(35.0)))

canvas.create_text(
    1358.5, 226.0,
    text = "score",
    fill = "#eeeeee",
    font = ("None", int(35.0)))

canvas.create_text(
    510.0, 789.5,
    text = "start	\n547.00\nhigh	\n547.00\nlow	\n535.00",
    fill = "#000000",
    font = ("None", int(26.0)))

canvas.create_text(
    721.0, 789.5,
    text = "value\n13.95\nP/E ratio	\n21.15\nyield\n2.04%",
    fill = "#000000",
    font = ("None", int(26.0)))

canvas.create_text(
    934.0, 789.5,
    text = "CDP	\nB\n52 wk high\n688.00\n52 wk low	\n518.00",
    fill = "#000000",
    font = ("None", int(26.0)))

canvas.create_text(
    1265.0, 355.0,
    text = "ma",
    fill = "#000000",
    font = ("None", int(35.0)))

canvas.create_text(
    1429.0, 454.0,
    text = "8",
    fill = "#000000",
    font = ("None", int(100.0)))

canvas.create_text(
    1497.0, 503.0,
    text = "/10",
    fill = "#000000",
    font = ("None", int(30.0)))

canvas.create_text(
    1263.5, 491.5,
    text = "ma Long \nma short\n3 day gold\n3 dat dead",
    fill = "#000000",
    font = ("None", int(25.0)))

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 60, y = 231,
    width = 115,
    height = 43)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b1.place(
    x = 60, y = 155,
    width = 115,
    height = 40)

img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b2.place(
    x = 60, y = 65,
    width = 115,
    height = 46)

img3 = PhotoImage(file = f"img3.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b3.place(
    x = 1057, y = 18,
    width = 64,
    height = 47)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    620.5, 166.0,
    image=background_img)

window.resizable(False, False)
window.mainloop()
