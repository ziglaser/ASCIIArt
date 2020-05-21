from PIL import Image, ImageDraw
import cv2
import os
import re
import subprocess as sp
import numpy as np
import importlib
import ffmpeg as fp


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split('(\d+)', text)]


def files_in_dir(dir, ext):
    files = []
    for file in os.listdir(dir): # os.listdir creates a list of all files and directories in a directory
        if file.endswith(ext): # we don't want other directories included in the file list
            files.append(file)
    return files


def image_to_ASCII_img(img_path, dest):
    shade_to_ascii_dict = {0: " ", 1: "`", 2: "^", 3: ";", 4: "1", 5: "?", 6: "U", 7: "@", 8: "@"}

    img = Image.open(img_path)
    width, height = img.size

    ascii_img = Image.new('RGB', (width, height), (255, 255, 255))
    d = ImageDraw.Draw(ascii_img)

    # chrs are 15 pixels tall, and 7 wide
    for y in range(0, height, 4):
        for x in range(0, width, 2):
            pixel_colors = []
            j = 0
            while j < 4 and (y + j) < height:
                i = 0
                while i < 2 and (x + i) < width:
                    r, g, b = img.getpixel((x + i, y + j))
                    pixel_colors.append((r + g + b) / 3)
                    i += 1
                j += 1
            avg_shade = sum(pixel_colors) / len(pixel_colors)
            key = (256 - avg_shade) // 32
            char = shade_to_ascii_dict[key]
            d.text((x, y), char, fill=(0, 0, 0))

    ascii_img.save(dest + "\\ascii_" + os.path.basename(img_path))


def convert_frames(dir, dest):
    pictures = files_in_dir(dir, "jpg")
    pictures.sort(key=natural_keys)
    for pic in pictures:
        image_to_ASCII_img(os.path.join(dir, pic), dest)
        print(pic)


def split_video(video_name):
    vidcap = cv2.VideoCapture(video_name)
    success, image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite("C:\\Users\\zglas\\PycharmProjects\\ASCIIArt\\venv\\Video_frames\\Original\\frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        #print('Read a new frame: ', success)
        count += 1


def stitch_video(video_name):
    image_folder = "C:\\Users\\zglas\\PycharmProjects\\ASCIIArt\\venv\\Video_frames\\ASCII"
    ascii_pictures = files_in_dir(image_folder, "jpg")
    print(ascii_pictures)

    frame = cv2.imread(os.path.join(image_folder, ascii_pictures[0]))
    width, height, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    #fourcc = cv2.VideoWriter_fourcc('F','M','P','4')

    video = cv2.VideoWriter(video_name, fourcc, 32.0, (width, height), False)

    for image in ascii_pictures:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

def stitch_video_2(video_name):
    FFMPEG_BIN = "C:\\Users\\zglas\\Downloads\\ffmpeg-20200515-b18fd2b-win64-static\\ffmpeg-20200515-b18fd2b-win64-static\\bin\\ffmpeg.exe"  # on Windows

    command = [FFMPEG_BIN,
               '-y',  # (optional) overwrite output file if it exists
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-s', '360x640',  # size of one frame
               '-pix_fmt', 'rgb24',
               '-r', '24',  # frames per second
               '-i', '-',  # The input comes from a pipe
               '-an',  # Tells FFMPEG not to expect any audio
               '-vcodec', 'mpeg', video_name]

    pipe = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)

    image_folder = "C:\\Users\\zglas\\PycharmProjects\\ASCIIArt\\venv\\Video_frames\\ASCII"
    ascii_pictures = files_in_dir(image_folder, "jpg")

    for image in ascii_pictures:
        to_write = Image.open(image_folder + "\\" + image)
        image_array = np.asarray(to_write)
        pipe.proc.stdin.write(image_array.tostring())

def stitch_video_3(video_name):
    (
        fp
        .input('C:\\Users\\zglas\\PycharmProjects\\ASCIIArt\\venv\\Video_frames\\ASCII\\*.jpg', pattern_type='glob', framerate=24)
        .output(video_name)
        .run()
    )


if __name__ == "__main__":
    #base_directory = "C:\\Users\\zglas\\PycharmProjects\\ASCIIArt\\venv\\Video_frames"
    #split_video("augie_swing.MOV")
    #convert_frames(base_directory + "\\Original", base_directory + "\\ASCII")
    stitch_video_3("ascii_augie_swing.avi")
