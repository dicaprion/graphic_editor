import pytest
import draw
from PIL import Image, ImageTk, ImageDraw, ImageColor
import math


class TestDraw:
    def test_erase_selected(self):
        pixel_list = [((0, 0), (255, 255, 200)), ((0, 1), (255, 205, 255))]
        img = Image.new("RGB", (960, 600), "blue")
        for i in pixel_list:
            img.putpixel(i[0], ImageColor.getrgb("white"))
        draw.eraseSelectedCropping(pixel_list, img)
        assert(img.getpixel((0, 1)) == (255, 255, 255))

    def test_cropping(self):
        img = Image.new("RGB", (960, 600), "blue")
        pixelList = []
        x0 = 0
        y0 = 0
        x1 = 0
        y1 = 2
        if y0 > y1:
            y0, y1 = y1, y0
        if x0 > x1:
            x0, x1 = x1, x0
        for j in range(y0, y1):
            for i in range(x0, x1):
                color = img.getpixel((i, j))
                pixelObj = ((i, j), color)
                pixelList.append(pixelObj)
                img.putpixel((i, j), ImageColor.getrgb("white"))
        assert(draw.cropping((0, 0), (0, 2), img) == pixelList)

    def test_draw_eclipse(self):
        img = Image.new("RGB", (960, 600), "blue")
        x = 0
        y = 1
        color = "red"
        centerPoint = (1, 1)
        img.putpixel((centerPoint[0] + x, centerPoint[1] + y), ImageColor.getrgb(color))
        img.putpixel((centerPoint[0] - x, centerPoint[1] + y), ImageColor.getrgb(color))
        img.putpixel((centerPoint[0] + x, centerPoint[1] - y), ImageColor.getrgb(color))
        img.putpixel((centerPoint[0] - x, centerPoint[1] - y), ImageColor.getrgb(color))
        draw.drawEclipse(centerPoint, x, y, color, img)
        assert(img.getpixel((0, 0)) == (0, 0, 255))

    def test_adding_pixels(self):
        img = Image.new("RGB", (960, 600), "blue")
        pixelList = []
        x0 = 0
        y0 = 0
        x1 = 0
        y1 = 2
        if y0 > y1:
            y0, y1 = y1, y0
        if x0 > x1:
            x0, x1 = x1, x0
        for j in range(y0, y1):
            for i in range(x0, x1):
                color = img.getpixel((i, j))
                pixelObj = ((i, j), color)
                pixelList.append(pixelObj)
        assert(draw.adding_pixels((0, 0), (0, 2), img) == pixelList)

