from PIL import Image

img_name = 'C:\\Users\\zglas\\PycharmProjects\\ASCIIArt\\venv\\ImageProcessing\\axelotl.JPG'
ascii_name = img_name[:-4] + "_ascii.txt"
ascii_file = open(ascii_name, 'w+')

shade_to_ascii_dict = {0 : " ", 1 : "`", 2 : "^", 3 : ";", 4 : "1", 5 : "?", 6 : "U", 7 : "@", 8 : "@"}

img = Image.open(img_name)
width, height = img.size

#chrs are 15 pixels tall, and 7 wide
for y in range(0, height, 8):
    new_line = ""
    for x in range(0, width, 4):
        pixel_colors = []
        j = 0
        while j < 8 and (y + j) < height:
            i = 0
            while i < 4 and (x + i) < width:
                r, g, b = img.getpixel((x + i, y + j))
                pixel_colors.append((r + g + b) / 3)
                i += 1
            j += 1
        avg_shade = sum(pixel_colors)/len(pixel_colors)
        key = (256 - avg_shade) // 32
        char = shade_to_ascii_dict[key]
        new_line += char
    ascii_file.write(new_line + "\n")


