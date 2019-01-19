import math
from PIL import ImageTk, ImageDraw, ImageColor


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def eraseSelectedCropping(pixelList, img):
    for i in pixelList:
        img.putpixel(i[0], ImageColor.getrgb("white"))


def cropping(startPoint, endPoint, img):
    pixelList = []
    x0 = startPoint[0]
    y0 = startPoint[1]
    x1 = endPoint[0]
    y1 = endPoint[1]
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
    return pixelList


def scalling(pixelList, center, scale, img):
  centerX = center[0]
  centerY = center[1]
  for i in range(0, len(pixelList) - 1):
    pixel = pixelList[i]

    x = centerX + int(round((pixel[0][0] - centerX) * scale[0]))
    y = centerY + int(round((pixel[0][1] - centerY) * scale[1]))

    img.putpixel((x, y), pixel[1])

  scaleImg = ImageTk.PhotoImage(img)
  return scaleImg


def eraser(previousPoint, pointNow, color, img):
    draw = ImageDraw.Draw(img)
    draw.rectangle([previousPoint, pointNow], fill=color)
    eraserImg = ImageTk.PhotoImage(img)
    return eraserImg


def flipHorizontal(startPoint, endPoint, center, bc, img):
    pixelList = []
    x0 = startPoint[0]
    y0 = startPoint[1]
    x1 = endPoint[0]
    y1 = endPoint[1]
    if y0 > y1:
        y0, y1 = y1, y0
    if x0 > x1:
        x0, x1 = x1, x0
    for j in range(y0, y1):
        for i in range(x0, x1):
            if img.getpixel((i, j)) != bc:
                color = img.getpixel((i, j))
                pixelObj = ((i, j), color)
                pixelList.append(pixelObj)
                img.putpixel((i, j), ImageColor.getrgb(bc))
    for i in range(0, len(pixelList) - 1):
        pixel = pixelList[i]
        x = pixel[0][0]
        y = 2 * center[1] - pixel[0][1]
        img.putpixel((x, y), pixel[1])
    flipHorizonImg = ImageTk.PhotoImage(img)
    return flipHorizonImg


def flipVertical(startPoint, endPoint, center, bc, img):
    pixelList = []
    x0 = startPoint[0]
    y0 = startPoint[1]
    x1 = endPoint[0]
    y1 = endPoint[1]
    if y0 > y1:
        y0, y1 = y1, y0
    if x0 > x1:
        x0, x1 = x1, x0
    for j in range(y0, y1):
        for i in range(x0, x1):
            if img.getpixel((i, j)) != bc:
                color = img.getpixel((i, j))
                pixelObj = ((i, j), color)
                pixelList.append(pixelObj)
                img.putpixel((i, j), ImageColor.getrgb(bc))
    for i in range(0, len(pixelList) - 1):
        pixel = pixelList[i]
        x = 2 * center[0] - pixel[0][0]
        y = pixel[0][1]
        img.putpixel((x, y), pixel[1])
    flipVerticalImg = ImageTk.PhotoImage(img)
    return flipVerticalImg


def moveRotation(pixelList, center, alpha,  img):
    for i in range(0, len(pixelList) - 1):
        pixel = pixelList[i]

        centerX = center[0]
        centerY = center[1]

        x = centerX + int(math.cos(alpha) * (pixel[0][0] - centerX) - math.sin(alpha) * (pixel[0][1] - centerY))
        y = centerY + int(math.sin(alpha) * (pixel[0][0] - centerX) + math.cos(alpha) * (pixel[0][1] - centerY))

        img.putpixel((x, y), pixel[1])
    roateImg = ImageTk.PhotoImage(img)
    return roateImg


def moveTransition(pixelList, newPoint, img):
    deltaX = newPoint[0] - pixelList[0][0][0]
    deltaY = newPoint[1] - pixelList[0][0][1]

    for i in range(0, len(pixelList) - 1):
        pixel = pixelList[i]
        img.putpixel((pixel[0][0] + deltaX, pixel[0][1] + deltaY), pixel[1])

    transitImg = ImageTk.PhotoImage(img)
    return transitImg


def drawEclipse(centerPoint, x, y, color, img):
    img.putpixel((centerPoint[0] + x, centerPoint[1] + y), ImageColor.getrgb(color))
    img.putpixel((centerPoint[0] - x, centerPoint[1] + y), ImageColor.getrgb(color))
    img.putpixel((centerPoint[0] + x, centerPoint[1] - y), ImageColor.getrgb(color))
    img.putpixel((centerPoint[0] - x, centerPoint[1] - y), ImageColor.getrgb(color))


def eclipseMidPoint(centerPoint, rx, ry, color, img):
  rxSq = rx ** 2
  rySq = ry ** 2
  x = 0
  y = ry
  px = 0
  py = 2 * rxSq * y
  drawEclipse(centerPoint, x, y, color, img)
  p = rySq - (rxSq * ry) + (0.25 * rxSq)
  while px < py:
    x = x + 1
    px = px + 2*rySq
    if p < 0:
      p = p + rySq + px
    else:
      y = y - 1
      py = py - 2*rxSq
      p = p + rySq + px - py
    drawEclipse(centerPoint, x, y, color, img)

  p = rySq*(x+0.5)*(x+0.5) + rxSq*(y-1)*(y-1) - rxSq*rySq
  while y > 0:
    y = y - 1
    py = py - 2 * rxSq
    if p > 0:
      p = p + rxSq - py
    else:
      x = x + 1
      px = px + 2 * rySq
      p = p + rxSq - py + px
    drawEclipse(centerPoint, x, y, color, img)

  eclipseImg = ImageTk.PhotoImage(img)
  return eclipseImg


def triangle(startPoint, endPoint, color, img, defaultState):
    a = (endPoint[1] - startPoint[1]) / float(2)
    b = (endPoint[0] - startPoint[0]) / float(2)

    A = (int(startPoint[0]), int(endPoint[1]))
    B = (int(endPoint[0]), int(endPoint[1]))
    C = (int(startPoint[0] + b), int(startPoint[1]))

    draw = ImageDraw.Draw(img)

    draw.line((A, B), color)
    draw.line((B, C), color)
    draw.line((C, A), color)

    triangleImg = ImageTk.PhotoImage(img)
    return triangleImg


def star(startPoint, endPoint, color, img, defaultState):
    a = (endPoint[1] - startPoint[1]) / float(2)
    b = (endPoint[0] - startPoint[0]) / float(2)

    A = (int(startPoint[0] + b), int(startPoint[1]))
    A1 = (int(startPoint[0] + 3 * b / 4), int(startPoint[1] + 3 * a / 4))
    A2 = (int(startPoint[0]), int(a + startPoint[1]))
    A3 = (int(startPoint[0] + b * 0.65), int(startPoint[1] + 1.25 * a))
    A4 = (int(startPoint[0] + b / 2), int(startPoint[1] + 2 * a))

    B = (int(startPoint[0] + b), int(1.4 * a + startPoint[1]))
    B1 = (int(startPoint[0] + 1.5 * b), int(2 * a + startPoint[1]))
    B2 = (int(startPoint[0] + 1.35 * b), int(1.25 * a + startPoint[1]))
    B3 = (int(startPoint[0] + 2 * b), int(a + startPoint[1]))
    B4 = (int(startPoint[0] + 1.25 * b), int(3 * a / 4 + startPoint[1]))

    draw = ImageDraw.Draw(img)

    draw.line((A, A1), color)
    draw.line((A1, A2), color)
    draw.line((A2, A3), color)
    draw.line((A3, A4), color)
    draw.line((A4, B), color)
    draw.line((B, B1), color)

    draw.line((A, B4), color)
    draw.line((B4, B3), color)
    draw.line((B3, B2), color)
    draw.line((B1, B2), color)

    starImg = ImageTk.PhotoImage(img)
    return starImg


def rectangle(pointA, pointB, color, img, defaultState):
    draw = ImageDraw.Draw(img)
    if defaultState:
        edge = abs(pointB[0] - pointA[0])
        if pointB[1] > pointA[1]:
            pointB = (pointB[0], edge + pointA[1])
        else:
            pointB = (pointB[0], abs(pointA[1] - edge))
        draw.rectangle([pointA, pointB], None, color)
    else:
        draw.rectangle([pointA, pointB], None, color)

    rectangleImg = ImageTk.PhotoImage(img)
    return rectangleImg


def fillColor(img, center, newColor):
    oldColor = img.getpixel(center)
    if oldColor == newColor:
      return
    listSeed = []
    listSeed.append(center)
    while listSeed and listSeed[-1][0] >= 0 and listSeed[-1][1] >= 0:
        seed = listSeed.pop(0)
        seedColor = img.getpixel(seed)
        if seedColor == oldColor:
            img.putpixel(seed, ImageColor.getrgb(newColor))
            x, y = seed[0], seed[1]
            listSeed.append((x+1, y))
            listSeed.append((x-1, y))
            listSeed.append((x, y+1))
            listSeed.append((x, y-1))
    filledImg = ImageTk.PhotoImage(img)
    return filledImg


def line(startPoint, endPoint, color, img, defaultState):
    draw = ImageDraw.Draw(img)
    draw.line((startPoint, endPoint), color)
    lineImg = ImageTk.PhotoImage(img)
    return lineImg


def adding_pixels(startPoint, endPoint, img):
    pixelList = []
    x0 = startPoint[0]
    y0 = startPoint[1]
    x1 = endPoint[0]
    y1 = endPoint[1]
    if y0 > y1:
        y0, y1 = y1, y0
    if x0 > x1:
        x0, x1 = x1, x0
    for j in range(y0, y1):
        for i in range(x0, x1):
            color = img.getpixel((i, j))
            pixelObj = ((i, j), color)
            pixelList.append(pixelObj)
    return pixelList


def brighter_brightness(pixelList, img, tool):
    for i in pixelList:
        color = i[1]
        if tool >= 1:
            img.putpixel(i[0], (color[0]*tool, color[1]*tool, color[2]*tool))
        elif tool == 0:
            img.putpixel(i[0], (color[0], color[1], color[2]))
        else:
            img.putpixel(i[0], (color[0] // abs(tool), color[1] // abs(tool), color[2] // abs(tool)))
    brightImg = ImageTk.PhotoImage(img)
    return brightImg


def gaussian_blur(width, height, img, tool):
    for i in range(1, width - 1):
        for j in range(1, height - 1):
            c1 = img.getpixel((i - 1, j))
            c2 = img.getpixel((i, j))
            c3 = img.getpixel((i + 1, j))

            bR = ((c1[0] + c2[0] + c3[0]) // 3)
            bG = ((c1[1] + c2[1] + c3[1]) // 3)
            bB = ((c1[2] + c2[2] + c3[2]) // 3)

            img.putpixel((i, j), (bR, bG, bB))
    gaussImg = ImageTk.PhotoImage(img)
    return gaussImg