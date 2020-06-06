from PIL import Image, ImageDraw

im = Image.open("x.png")

N = 25
size = im.size[0] // 25

css = [[-1 for j in range(N)] for i in range(N)]

for i in range(N):
    for j in range(N):
        (y1, x1) = (i*size, j*size)
        (y1_2, x1_2) = (y1 + 1, x1)
        (y2, x2) = ((i + 1)*size - 1, (j + 1)*size - 1)
        (y2_2, x2_2) = (y2 - 1, x2)
        color1 = im.getpixel((x1, y1))
        color2 = im.getpixel((x1_2, y1_2))
        if color1 == color2 and color1[0] == color1[1] and color1[1] == color1[2] and (color1[0] == 0 or color1[0] == 255):
            css[i][j] = 1 if color1[0] == 0 else 0
        color1 = im.getpixel((x2, y1))
        color2 = im.getpixel((x2_2, y1_2))
        if color1 == color2 and color1[0] == color1[1] and color1[1] == color1[2] and (color1[0] == 0 or color1[0] == 255):
            css[i][j] = 1 if color1[0] == 0 else 0
        color1 = im.getpixel((x1, y2))
        color2 = im.getpixel((x1_2, y2_2))
        if color1 == color2 and color1[0] == color1[1] and color1[1] == color1[2] and (color1[0] == 0 or color1[0] == 255):
            css[i][j] = 1 if color1[0] == 0 else 0
        color1 = im.getpixel((x2, y2))
        color2 = im.getpixel((x2_2, y2_2))
        if color1 == color2 and color1[0] == color1[1] and color1[1] == color1[2] and (color1[0] == 0 or color1[0] == 255):
            css[i][j] = 1 if color1[0] == 0 else 0

new_im = Image.new("RGB", (N*size, N*size), (255, 0, 0))
draw = ImageDraw.Draw(new_im)
for i in range(N):
    for j in range(N):
        (y1, x1) = (i*size, j*size)
        (y2, x2) = ((i + 1)*size, (j + 1)*size)
        color = (0, 0, 0) if css[i][j] == 1 else (255, 255, 255) if css[i][j] == 0 else (100, 100, 100)
        draw.rectangle([(x1, y1), (x2 - 1, y2 - 1)], fill=color)
new_im.save("y.png", "PNG")

for i in range(N):
    for j in range(N):
        (y1, x1) = (i*size, j*size)
        (y2, x2) = ((i + 1)*size - 1, (j + 1)*size - 1)
        color = new_im.getpixel((x1, y1))
        if color[0] == color[1] and color[1] == color[2] and (color[0] == 0 or color[0] == 255):
            css[i][j] = 1 if color[0] == 0 else 0
        color = new_im.getpixel((x2, y1))
        if color[0] == color[1] and color[1] == color[2] and (color[0] == 0 or color[0] == 255):
            css[i][j] = 1 if color[0] == 0 else 0
        color = new_im.getpixel((x1, y2))
        if color[0] == color[1] and color[1] == color[2] and (color[0] == 0 or color[0] == 255):
            css[i][j] = 1 if color[0] == 0 else 0
        color = new_im.getpixel((x2, y2))
        if color[0] == color[1] and color[1] == color[2] and (color[0] == 0 or color[0] == 255):
            css[i][j] = 1 if color[0] == 0 else 0

with open("qr.txt", mode="w") as f:
    for cs in css:
        for c in cs:
            f.write("X" if c == 1 else "_" if c == 0 else "?")
        f.write("\n")
