from tkinter import *
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
from random import randint
import draw
import copy
import math

brush_size = 3
brush_color = 'black'
pixel_list = None


class Editor(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.canvas = Canvas(self, bg="gray")

        self.canvas.bind('<B1-Motion>', self.paint_pen_line)
        self.canvas.bind("<Button-1>", self.set_previous_point)
        self.tools_brightness = 2
        self.tools_gaussian = 3
        self.paper_width = 960
        self.paper_height = 600
        self.pixelList = None
        self.defaultState = 0
        self.fOpenName = None
        self.gui()
        self.center_window()
        self.canvas.pack(expand=YES)
        self.img = Image.new("RGB", (960, 600), "white")
        self.use = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.use)

    def center_window(self):
        self.w = 960
        self.h = 600
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - self.w) / 2
        y = (sh - self.h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

    def gui(self):
        self.topFrame = Frame(self)
        self.topFrame.pack(side=TOP, fill=X)

        self.leftFrame = Frame(self)
        self.leftFrame.pack(side=LEFT, fill=Y)

        self.rightFrame = Frame(self)
        self.rightFrame.pack(side=RIGHT, fill=Y)

        self.parent.title("Editor")
        self.pack(side=RIGHT, fill=BOTH, expand=1)

        self.canvas.pack(fill=BOTH, expand=1)

        self.buttonDeleteAll = Button(self.leftFrame, text="Clear", width=4, height=2, bg='white', fg='black', relief=GROOVE, cursor="hand2",
                                      command=self.deleteAll)
        self.buttonDeleteAll.pack()

        labelB = Label(self.topFrame, width=10, text="brightness")
        self.myScaleB = Scale(
            self.topFrame, from_=1, to=5,
            orient=HORIZONTAL,
            command=self.set_brightness
        )
        self.myScaleB.set(1)

        labelB.pack(side=LEFT)
        self.myScaleB.pack(side=LEFT)

        labelG = Label(self.topFrame, width=10, text="gaussian")
        self.myScaleG = Scale(
            self.topFrame, from_=1, to=5,
            orient=HORIZONTAL,
            command=self.set_gaussian
        )
        self.myScaleG.set(1)

        labelG.pack(side=LEFT)
        self.myScaleG.pack(side=LEFT)

        width = StringVar()
        height = StringVar()
        entryw = Entry(self.rightFrame, width=5, textvariable=width)
        entryh = Entry(self.rightFrame, width=5, textvariable=height)
        labelw = Label(self.rightFrame, width=5, text="width")
        labelh = Label(self.rightFrame, width=5, text="height")
        labelw.pack()
        entryw.pack()
        labelh.pack()
        entryh.pack()

        btnApply = Button(self.rightFrame, width=5, height=1, text="apply", cursor="hand2",
                           command=lambda: self.change_canvas_size(int(entryw.get()), int(entryh.get())))
        btnApply.pack()

        btnBlack = Button(self, width=2, height=1, bg='black', fg='black',relief=GROOVE, activebackground='black', cursor="hand2",
                           command=lambda: self.color_change_btn("black"))
        btnBlack.pack(side="right")

        btnGray = Button(self, width=2, height=1, bg='gray', fg='black', relief=GROOVE, activebackground='gray', cursor="hand2",
                           command=lambda: self.color_change_btn("gray"))
        btnGray.pack(side="right")

        btnWhite = Button(self, width=2, height=1, bg='white', fg='black', relief=GROOVE, activebackground='white', cursor="hand2",
                           command=lambda: self.color_change_btn("white"))
        btnWhite.pack(side="right")

        btnPurple = Button(self, width=2, height=1, bg='purple', fg='black', relief=GROOVE, activebackground='purple', cursor="hand2",
                           command=lambda: self.color_change_btn("purple"))
        btnPurple.pack(side="right")

        btnDarkBlue = Button(self, width=2, height=1, bg='dark blue', fg='black', relief=GROOVE, activebackground='dark blue', cursor="hand2",
                           command=lambda: self.color_change_btn("darkblue"))
        btnDarkBlue.pack(side="right")

        btnBlue = Button(self, width=2, height=1, bg='blue', fg='black', relief=GROOVE, activebackground='blue', cursor="hand2",
                           command=lambda: self.color_change_btn("blue"))
        btnBlue.pack(side="right")

        btnGreen = Button(self, width=2, height=1, bg='green', fg='black', relief=GROOVE, activebackground='green', cursor="hand2",
                           command=lambda: self.color_change_btn("green"))
        btnGreen.pack(side="right")

        btnYellow = Button(self, width=2, height=1, bg='yellow', fg='black', relief=GROOVE, activebackground='yellow', cursor="hand2",
                           command=lambda: self.color_change_btn("yellow"))
        btnYellow.pack(side="right")

        btnOrange = Button(self, width=2, height=1, bg='orange', fg='black', relief=GROOVE, activebackground='orange', cursor="hand2",
                           command=lambda: self.color_change_btn("orange"))
        btnOrange.pack(side="right")

        btnRed = Button(self, width=2, height=1, bg='red', fg='black', relief=GROOVE, activebackground='red', cursor="hand2",
                        command=lambda: self.color_change_btn("red"))
        btnRed.pack(side="right")

        imagePalete = PhotoImage(file="images\palete.png")
        btnChoose = Button(self, bg='white', fg='black', relief=GROOVE, image=imagePalete, cursor="hand2",
                        command=lambda: self.color_change(brush_color))
        btnChoose.image = imagePalete
        btnChoose.pack(side="right")

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="New", command=self.deleteAll)
        fileMenu.add_command(label="Open", command=self.callOpenImage)
        fileMenu.add_command(label="Save", command=self.save_image)
        fileMenu.add_command(label="Save as...", command=self.save_as_image)
        fileMenu.add_command(label="Exit", command=self.onExit)

        edit = Menu(menubar)
        edit.add_command(label="Erase selected", command=self.erase_selected)
        edit.add_command(label="Change brightness", command=self.change_brightness)
        edit.add_command(label="Gaussian blur", command=self.gaussian_blur)
        edit.add_command(label="Fill selected", command=self.fill_selected)

        about = Menu(menubar)
        about.add_command(label="About", command=self.callAbout)

        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label='Edit', menu=edit)
        menubar.add_cascade(label="About", menu=about)

        imageSizes = PhotoImage(file="images\sizes.png")
        imageSize1 = PhotoImage(file="images\size1.png")
        imageSize2 = PhotoImage(file="images\size2.png")
        imageSize3 = PhotoImage(file="images\size3.png")
        imageSize4 = PhotoImage(file="images\size4.png")
        btnSizes = Menubutton(self.leftFrame, image=imageSizes, bg='white', fg='black', relief=GROOVE, cursor="hand2")
        btnSizes.menu = Menu(btnSizes, tearoff=0)
        btnSizes["menu"] = btnSizes.menu

        btnSizes.menu.add_checkbutton(image=imageSize1, command=lambda: self.brush_size_change(3))
        btnSizes.menu.add_checkbutton(image=imageSize2, command=lambda: self.brush_size_change(6))
        btnSizes.menu.add_checkbutton(image=imageSize3, command=lambda: self.brush_size_change(9))
        btnSizes.menu.add_checkbutton(image=imageSize4, command=lambda: self.brush_size_change(12))
        btnSizes.menu.imageSize1 = imageSize1
        btnSizes.menu.imageSize2 = imageSize2
        btnSizes.menu.imageSize3 = imageSize3
        btnSizes.menu.imageSize4 = imageSize4
        btnSizes.image = imageSizes
        btnSizes.pack(side="top")

        imageErase = PhotoImage(file="images\eraser.png")
        btnEraser = Button(self.leftFrame, image=imageErase, bg='white', fg='black', relief=GROOVE, cursor="hand2",
                           command=lambda: self.color_change_btn("white"))
        btnEraser.image = imageErase
        btnEraser.pack(side="top")

        imagePencil = PhotoImage(file="images\pencil.png")
        btnPencil = Button(self.leftFrame, bg='white', fg='black', relief=GROOVE, image=imagePencil, cursor="hand2",
                           command=lambda: self.draw_pencil_tool())
        btnPencil.image = imagePencil
        btnPencil.pack(side="top")

        imageBrushes = PhotoImage(file="images\\brush.png")
        imageBrush1 = PhotoImage(file="images\\brushd.png")
        imageBrush2 = PhotoImage(file="images\\flower.png")
        imageBrush3 = PhotoImage(file="images\spray.png")

        btnBrushes = Menubutton(self.leftFrame, image=imageBrushes, bg='white', fg='black', relief=GROOVE, cursor="hand2")
        btnBrushes.menu = Menu(btnBrushes, tearoff=0)
        btnBrushes["menu"] = btnBrushes.menu

        btnBrushes.menu.add_checkbutton(image=imageBrush1, command=lambda: self.draw_pen_tool())
        btnBrushes.menu.add_checkbutton(image=imageBrush2, command=lambda: self.draw_flower_tool())
        btnBrushes.menu.add_checkbutton(image=imageBrush3, command=lambda: self.draw_spray_tool())
        btnBrushes.menu.imageSize1 = imageBrush1
        btnBrushes.menu.imageSize2 = imageBrush2
        btnBrushes.menu.imageSize3 = imageBrush3
        btnBrushes.image = imageBrushes
        btnBrushes.pack(side="top")

        imageFill = PhotoImage(file="images\\fill.png")
        btnFill = Button(self.leftFrame, image=imageFill, bg='white', fg='black', relief=GROOVE, cursor="hand2",
                           command=lambda: self.fill_color())
        btnFill.image = imageFill
        btnFill.pack(side="top")

        imagePipet = PhotoImage(file="images\\pipet.png")
        btnPipet = Button(self.leftFrame, bg='white', fg='black', relief=GROOVE, image=imagePipet, cursor="hand2",
                        command=lambda: self.press_pipet())
        btnPipet.image = imagePipet
        btnPipet.pack(side="top")

        imageFigures = PhotoImage(file="images\\figures.png")
        imageFigure1 = PhotoImage(file="images\\rectangle.png")
        imageFigure2 = PhotoImage(file="images\\triangle.png")
        imageFigure3 = PhotoImage(file="images\\circle.png")
        imageFigure5 = PhotoImage(file="images\\line.png")
        imageFigure6 = PhotoImage(file="images\\star.png")

        btnFigures = Menubutton(self.leftFrame, image=imageFigures, bg='white', fg='black',
                                relief=GROOVE,  cursor="hand2")
        btnFigures.menu = Menu(btnFigures, tearoff=0)
        btnFigures["menu"] = btnFigures.menu

        btnFigures.menu.add_checkbutton(image=imageFigure1, command=lambda: self.draw_rectangle())
        btnFigures.menu.add_checkbutton(image=imageFigure2, command=lambda: self.draw_triangle())
        btnFigures.menu.add_checkbutton(image=imageFigure3, command=lambda: self.draw_circle())
        btnFigures.menu.add_checkbutton(image=imageFigure6, command=lambda: self.draw_star())
        btnFigures.menu.add_checkbutton(image=imageFigure5, command=lambda: self.draw_line())


        btnFigures.menu.imageFigure1 = imageFigure1
        btnFigures.menu.imageFigure2 = imageFigure2
        btnFigures.menu.imageFigure3 = imageFigure3
        btnFigures.menu.imageFigure5 = imageFigure5
        btnFigures.menu.imageFigure6 = imageFigure6

        btnFigures.image = imageFigures
        btnFigures.pack(side="top")

        imageAllocate = PhotoImage(file="images\\allocate.png")
        btnAllocate = Button(self.leftFrame, bg='white', fg='black', relief=GROOVE, image=imageAllocate, cursor="hand2",
                        command=lambda: self.transitionTool())
        btnAllocate.image = imageAllocate
        btnAllocate.pack(side="top")

        imageRotate = PhotoImage(file="images\\arrow.png")
        btnRotate = Button(self.leftFrame, bg='white', fg='black', relief=GROOVE, image=imageRotate, cursor="hand2",
                          command=lambda: self.rotationTool())
        btnRotate.image = imageRotate
        btnRotate.pack(side="top")

        imageFlip = PhotoImage(file="images\\flip.png")
        btnFlip = Button(self.leftFrame, bg='white', fg='black', relief=GROOVE, image=imageFlip, cursor="hand2",
                           command=lambda: self.flippingVerticalTool())
        btnFlip.image = imageFlip
        btnFlip.pack(side="top")

        imageFlip1 = PhotoImage(file="images\\fliph.png")
        btnFlip1 = Button(self.leftFrame, bg='white', fg='black', relief=GROOVE, image=imageFlip1, cursor="hand2",
                         command=lambda: self.flippingHorizontalTool())
        btnFlip1.image = imageFlip1
        btnFlip1.pack(side="top")

        imageScale = PhotoImage(file="images\\scale.png")
        btnScale = Button(self.leftFrame, bg='white', fg='black', relief=GROOVE, image=imageScale, cursor="hand2",
                          command=lambda: self.scalingTool())
        btnScale.image = imageScale
        btnScale.pack(side="top")

    def onExit(self):
        self.quit()

    def deleteAll(self):
        self.img = Image.new("RGB", (self.paper_width, self.paper_height), "white")
        self.use_img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.use_img)

    def save_image(self):
        image_name = filedialog.asksaveasfilename(defaultextension=".png")
        if not image_name:
            return
        self.img.save(image_name)

    def save_as_image(self):
        fname = filedialog.asksaveasfilename(defaultextension=".png")
        if not fname:
            return
        self.img.save(fname)

    def callAbout(self):
        messagebox.showinfo("About", "Graphic editor v2.0")

    def callOpenImage(self):
        self.fOpenName = filedialog.askopenfilename(
            filetypes=(("Supported Image Files", "*.jpg; *.jpeg; *.png; *.bmp; *.ico"),
                       ("All files", "*.*")))

        if not self.fOpenName:
            return
        self.canvas.delete("all")

        self.img = Image.open(self.fOpenName).resize((self.paper_width, self.paper_height))
        self.use_img = ImageTk.PhotoImage(self.img)

        self.canvas.img = self.use_img
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.canvas.img)

    def set_previous_point(self, event):
        self.previous_point = (event.x, event.y)

    def draw_pencil_tool(self):
        self.canvas.bind("<B1-Motion>", self.paint_pencil_line)
        self.canvas.bind("<ButtonRelease-1>", self.paint_pencil_line)
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)

    def draw_pen_tool(self):
        self.canvas.bind("<B1-Motion>", self.paint_pen_line)
        self.canvas.bind("<ButtonRelease-1>", self.paint_pen_line)
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)

    def draw_spray_tool(self):
        self.canvas.bind("<B1-Motion>", self.paint_spray_pen)
        self.canvas.bind("<ButtonRelease-1>", self.paint_spray_pen)
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)

    def draw_flower_tool(self):
        self.canvas.bind("<B1-Motion>", self.paint_flower_pen)
        self.canvas.bind("<ButtonRelease-1>", self.paint_flower_pen)
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)

    def press_pipet(self):
        self.canvas.bind("<ButtonRelease-1>", self.pipet)
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)

    def paint_pen_line(self, event):
        draw = ImageDraw.Draw(self.img)
        draw.line((self.previous_point, (event.x, event.y)), brush_color, brush_size)
        self.pencil_img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.pencil_img)
        self.previous_point = (event.x, event.y)

    def paint_pencil_line(self, event):
        draw = ImageDraw.Draw(self.img)
        draw.line((self.previous_point, (event.x, event.y)), brush_color, brush_size // 2)
        self.pencil_img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.pencil_img)
        self.previous_point = (event.x, event.y)

    def paint_spray_pen(self, event):
        if brush_size < 5:
            multiplier = 6
        else:
            multiplier = 2
        draw = ImageDraw.Draw(self.img)
        xrand = randint(-brush_size * multiplier,
                        +brush_size * multiplier)
        yrand = randint(-brush_size * multiplier,
                        +brush_size * multiplier)
        draw.ellipse([event.x + xrand, event.y + yrand,
                                event.x + xrand + brush_size, event.y + yrand + brush_size],
                                fill=brush_color)
        self.pencil_img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.pencil_img)
        self.previous_point = (event.x, event.y)

    def paint_flower_pen(self, event):
        draw = ImageDraw.Draw(self.img)
        draw.line((self.previous_point, (event.x, event.y)), brush_color, brush_size)
        self.pencil_img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.pencil_img)

    def brush_size_change(self, new):
        global brush_size
        brush_size = new

    def color_change_btn(self, new):
        global brush_color
        brush_color = new

    def color_change(self, current):
        global brush_color
        brush_color = colorchooser.askcolor()[1]
        if brush_color is None:
            brush_color = current

    def fill_color(self):
        self.canvas.bind("<ButtonRelease-1>", self.fill)

    def fill(self, event):
        self.filled = draw.fillColor(self.img, (event.x, event.y), brush_color)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.filled)

    def pipet(self, event):
        global brush_color
        brush_color = self.img.getpixel((event.x, event.y))

    def rectangle_release(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        self.rectangleImg = draw.rectangle((x0, y0), (x1, y1), brush_color, self.img, self.defaultState)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.rectangleImg)
        self.defaultState = 0

    def rectangle_motion(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        paper = copy.copy(self.img)
        self.rectangleImg = draw.rectangle((x0, y0), (x1, y1), brush_color, paper, self.defaultState)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.rectangleImg)
        self.defaultState = 0

    def draw_rectangle(self):
        self.canvas.bind("<ButtonRelease-1>", self.rectangle_release)
        self.canvas.bind("<B1-Motion>", self.rectangle_motion)

    def circle_motion(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        paper = copy.copy(self.img)
        rx = x1 - x0
        if self.defaultState == 1:
            ry = rx
        else:
            ry = y1 - y0
        self.circleImg = draw.eclipseMidPoint((x0, y0), rx, ry, brush_color, paper)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.circleImg)
        self.defaultState = 0

    def circle_release(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        rx = x1 - x0
        if self.defaultState == 1:
            ry = rx
        else:
            ry = y1 - y0
        self.circleImg = draw.eclipseMidPoint((x0, y0), rx, ry, brush_color, self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.circleImg)
        self.defaultState = 0

    def draw_circle(self):
        self.canvas.bind("<ButtonRelease-1>", self.circle_release)
        self.canvas.bind("<B1-Motion>", self.circle_motion)
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)

    def triangle_motion(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        paper = copy.copy(self.img)
        self.triangleImg = draw.triangle((x0, y0), (x1, y1), brush_color, paper, self.defaultState)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.triangleImg)
        self.defaultState = 0

    def triangle_release(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        self.triangleImg = draw.triangle((x0, y0), (x1, y1), brush_color, self.img, self.defaultState)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.triangleImg)
        self.defaultState = 0

    def draw_triangle(self):
        self.canvas.bind("<ButtonRelease-1>", self.triangle_release)
        self.canvas.bind("<B1-Motion>", self.triangle_motion)
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)

    def star_motion(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        paper = copy.copy(self.img)
        self.starImg = draw.star((x0, y0), (x1, y1), brush_color, paper, self.defaultState)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.starImg)
        self.defaultState = 0

    def star_release(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        self.starImg = draw.star((x0, y0), (x1, y1), brush_color, self.img, self.defaultState)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.starImg)
        self.defaultState = 0

    def draw_star(self):
        self.canvas.bind("<ButtonRelease-1>", self.star_release)
        self.canvas.bind("<B1-Motion>", self.star_motion)
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)

    def line_motion(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        paper = copy.copy(self.img)
        self.lineImg = draw.line((x0, y0), (x1, y1), brush_color, paper, self.defaultState)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.lineImg)
        self.defaultState = 0

    def line_release(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        self.lineImg = draw.line((x0, y0), (x1, y1), brush_color, self.img, self.defaultState)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.lineImg)
        self.defaultState = 0

    def draw_line(self):
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)
        self.canvas.bind("<B1-Motion>", self.line_motion)
        self.canvas.bind("<ButtonRelease-1>", self.line_release)

    def flippingVerticalTool(self):
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)
        self.canvas.bind("<B1-Motion>", self.on_button_choosing_place_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_choosing_place_flip_vertical)

    def flippingHorizontalTool(self):
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)
        self.canvas.bind("<B1-Motion>", self.on_button_choosing_place_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_choosing_place_flip_horizon)

    def rotationTool(self):
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)
        self.canvas.bind("<B1-Motion>", self.on_button_choosing_place_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_choosing_place_rotate)

    def transitionTool(self):
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)
        self.canvas.bind("<B1-Motion>", self.on_button_choosing_place_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_choosing_place)

    def scalingTool(self):
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)
        self.canvas.bind("<B1-Motion>", self.on_button_choosing_place_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_choosing_place_scale)

    def on_button_choosing_place_motion(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        paper = copy.copy(self.img)
        self.rectangleImg = draw.rectangle((x0, y0), (x1, y1), "blue", paper, self.defaultState)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.rectangleImg)
        self.defaultState = 0

    def on_button_release_choosing_place(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        self.transitionPlace = ((x0, y0), (x1, y1))
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)
        self.canvas.bind("<B1-Motion>", self.on_button_transition_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_transition)

    def on_button_transition_motion(self, event):
        x1, y1 = (event.x, event.y)
        paper = copy.copy(self.img)
        self.pixelList = draw.cropping(self.transitionPlace[0], self.transitionPlace[1], paper)
        self.transitImg = draw.moveTransition(self.pixelList, (x1, y1),  paper)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.transitImg)
        self.defaultState = 0

    def on_button_release_transition(self, event):
        x1, y1 = (event.x, event.y)
        if self.pixelList:
            draw.eraseSelectedCropping(self.pixelList,  self.img)
        self.transitImg = draw.moveTransition(self.pixelList, (x1, y1), self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.transitImg)
        self.pixelList = None
        self.transitionTool()
        self.defaultState = 0

    def on_button_release_choosing_place_flip_horizon(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        self.transitionPlace = ((x0, y0), (x1, y1))
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_flip_horizon)

    def on_button_release_choosing_place_flip_vertical(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        self.transitionPlace = ((x0, y0), (x1, y1))
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_flip_vertical)

    def on_button_release_choosing_place_rotate(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        self.transitionPlace = ((x0, y0), (x1, y1))
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)
        self.canvas.bind("<B1-Motion>", self.on_button_rotation_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_rotation)

    def on_button_release_choosing_place_scale(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        self.transitionPlace = ((x0, y0), (x1, y1))
        self.canvas.bind("<ButtonPress-1>", self.set_previous_point)
        self.canvas.bind("<B1-Motion>", self.on_button_scale_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_scale)

    def on_button_scale_motion(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        paper = copy.copy(self.img)
        if not self.pixelList:
            self.pixelList = draw.cropping(self.transitionPlace[0], self.transitionPlace[1], paper)
        self.scaleImg = draw.scalling(self.pixelList, (x0, y0), (x1, y1), paper)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.scaleImg)
        self.defaultState = 0

    def on_button_release_scale(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        scaleX = x1 / float(x0)
        scaleY = y1 / float(y0)
        if self.pixelList:
            draw.eraseSelectedCropping(self.pixelList,  self.img)
        self.scaleImg = draw.scalling(self.pixelList, (x0, y0), (scaleX, scaleY), self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.scaleImg)
        self.pixelList = None
        self.scalingTool()
        self.defaultState = 0

    def on_button_rotation_motion(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        paper = copy.copy(self.img)
        if x1 > x0:
            alpha = math.atan((y0 - y1) / float(x0 - x1))
        elif x1< x0:
            alpha = math.pi + math.atan((y0 - y1) / float(x0 - x1))
        if not self.pixelList:
           self.pixelList = draw.cropping(self.transitionPlace[0], self.transitionPlace[1], paper)
        self.rotateImg = draw.moveRotation(self.pixelList, (x0, y0), alpha, paper)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.rotateImg)
        self.defaultState = 0

    def on_button_release_rotation(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        alpha = math.atan(y1 / float(x1))
        if x1 > x0:
            alpha = math.atan((y0 - y1) / float(x0 - x1))
        else:
            alpha = math.pi + math.atan((y0 - y1) / float(x0 - x1))
        if self.pixelList:
            draw.eraseSelectedCropping(self.pixelList, self.img)
        self.rotateImg = draw.moveRotation(self.pixelList, (x0, y0), alpha, self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.rotateImg)
        self.rotationTool()
        self.pixelList = None
        self.defaultState = 0

    def on_button_release_flip_horizon(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        self.flipImg = draw.flipHorizontal(self.transitionPlace[0], self.transitionPlace[1], (x1, y1), "white",
                                           self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_width / 2, image=self.flipImg)
        self.flippingHorizontalTool()
        self.defaultState = 0

    def on_button_release_flip_vertical(self, event):
        x0, y0 = (self.previous_point[0], self.previous_point[1])
        x1, y1 = (event.x, event.y)
        self.flip1Img = draw.flipVertical(self.transitionPlace[0], self.transitionPlace[1], (x1, y1), "white",
                                         self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.flip1Img)
        self.flippingVerticalTool()
        self.defaultState = 0

    def erase_selected(self):
        self.eraserImg = draw.eraser(self.transitionPlace[0], self.transitionPlace[1], "white", self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.eraserImg)

    def fill_selected(self):
        self.fillImg = draw.eraser(self.transitionPlace[0], self.transitionPlace[1], brush_color, self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.fillImg)

    def gaussian_blur(self):
        paper = copy.copy(self.img)
        self.pixelList = draw.adding_pixels((0, 0), (self.paper_width - 1, self.paper_height - 1), paper)
        self.gaussImg = draw.gaussian_blur(self.paper_width, self.paper_height, self.img, self.tools_gaussian)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.gaussImg)

    def change_brightness(self):
        paper = copy.copy(self.img)
        self.pixelList = draw.adding_pixels((0, 0), (self.paper_width - 1, self.paper_height - 1), paper)
        self.brightImg = draw.brighter_brightness(self.pixelList, self.img, self.tools_brightness)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.brightImg)

    def change_canvas_size(self, newWidth, newHeight):
        self.paper_width = newWidth
        self.paper_height = newHeight
        self.img = Image.new("RGB", (newWidth, newHeight), "white")
        self.use = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.use)

    def set_brightness(self, event):
        self.tools_brightness = self.myScaleB.get()
        self.bimg = ImageEnhance.Brightness(self.img).enhance(self.tools_brightness)
        self.brightImg = ImageTk.PhotoImage(self.bimg)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.brightImg)

    def set_gaussian(self, event):
        self.tools_gaussian = self.myScaleG.get()
        self.gimg = self.img.filter(ImageFilter.GaussianBlur(radius=self.tools_gaussian))
        self.gaussImg = ImageTk.PhotoImage(self.gimg)
        self.canvas.create_image(self.paper_width / 2, self.paper_height / 2, image=self.gaussImg)


def main():
    window = Tk()
    Editor(window)
    window.mainloop()


if __name__ == '__main__':
    main()
