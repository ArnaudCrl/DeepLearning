#!/usr/bin/python
from PIL import Image, ImageChops
import os, sys

raw_data_path = "../data_raw/"
output_path = "result/"


# dirs = os.listdir(raw_data_path)
# print(dirs)


def is_white(img):
    avg = img.resize((1, 1))
    color = avg.getpixel((0, 0))
    return color > 128


def resize():
    for item in dirs:
        if os.path.isfile(path + item):
            im = Image.open(path + item)
            f, e = os.path.splitext(path + item)
            imCorrected = im.resize((256, 256), Image.ANTIALIAS)
            imCorrected.save(f + '.jpg', 'JPEG', quality=100)



def convert_to_black_and_white(im):
    gray = im.convert('L')
    # bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
    return gray


def crop_white_image(im):
    width, height = im.size

    crop_check = im.crop((width / 3, height - 30, width, height))
    black_px_count = 0
    for x in range(crop_check.width):
        for y in range(crop_check.height):
            # for the given pixel at w,h, lets check its value against the threshold
            if crop_check.getpixel((x, y)) < 128:  # note that the first parameter is actually a tuple object
                # lets set this to zero
                black_px_count += 1
    if black_px_count < 850:
        im = im.crop((0, 0, width, height - 250))
    else:
        im = im.crop((0, 0, width, height - 160))
    return im


def crop_black_image(im):
    colorH = im.getpixel((im.size[0] / 2, 5))
    colorG = im.getpixel((5, im.size[1] / 2))
    colorD = im.getpixel((im.size[0] - 6, im.size[1] / 2))
    colorB = im.getpixel((im.size[0] / 2, im.size[1] - 6))

    # HAUT
    if colorH > 128:
        color = 255
        lines_to_remove = 0
        i = 1
        while color >= 128 and i < im.size[0] * 0.2:
            lines_to_remove += 1
            color = im.getpixel((im.size[0] / 2, 5 - i))
            i += 1
        # print("removed {} lines en haut".format(i))

        im = im.crop((5, 5 - i, im.size[0] - 5, im.size[1] - 5))

    # GAUCHE
    if colorG > 128:
        color = 255
        lines_to_remove = 0
        i = 1
        while color >= 128 and i < im.size[0] * 0.2:
            lines_to_remove += 1
            color = im.getpixel((5 - i, im.size[1] / 2))
            i += 1
        # print("removed {} lines a gauche".format(i))

        im = im.crop((5 - i, 5, im.size[0] - 5, im.size[1] - 5))

    # DROITE
    if colorD > 128:
        color = 255
        lines_to_remove = 0
        i = 1
        while color >= 128 and i < im.size[0] * 0.2:
            lines_to_remove += 1
            color = im.getpixel((im.size[0] - 6 - i, im.size[1] / 2))
            i += 1
        # print("removed {} lines à droite".format(i))

        im = im.crop((5, 5, im.size[0] - 5 - i, im.size[1] - 5))

    # BAS
    if colorB > 128:
        color = 255
        lines_to_remove = 0
        i = 1
        while color >= 128 and i < im.size[0] * 0.2:
            lines_to_remove += 1
            color = im.getpixel((im.size[0] / 2, im.size[1] - 5 - i))
            i += 1
        # print("removed {} lines en bas".format(i))

        im = im.crop((5, 5, im.size[0] - 5, im.size[1] - 5 - i))

    im = im.crop((5, 5, im.size[0] - 6, im.size[1] - 6))

    return (im)


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def make_square(im, desired_size=512):
    old_size = im.size  # old_size[0] is in (width, height) format

    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])

    im = im.resize(new_size, Image.ANTIALIAS)

    new_im = Image.new("L", (desired_size, desired_size))
    new_im.paste(im, ((desired_size - new_size[0]) // 2,
                      (desired_size - new_size[1]) // 2))

    return new_im



def apply_corresctions():
    for big_class in (os.listdir(raw_data_path)):
        os.mkdir(output_path + big_class)

        for sub_class in (os.listdir(raw_data_path + big_class)):
            os.mkdir((output_path + big_class + "/" + sub_class))

            for file in (os.listdir(raw_data_path + big_class + "/" + sub_class)):  # 9348 files, 9316 .jpg, le reste .JPG

                with Image.open(raw_data_path + big_class + "/" + sub_class + "/" + file) as image:
                    imCorrected = convert_to_black_and_white(image)
                    if is_white(imCorrected):
                        imCorrected = crop_white_image(imCorrected)
                    else:
                        imCorrected = crop_black_image(imCorrected)
                    imCorrected = make_square(imCorrected)
                    imCorrected.save(output_path + big_class + "/" + sub_class + "/" + file, 'JPEG', quality=90)


# import shutilss + "/" + sub_class + "/" + file, output_path + big_class + "/" + file)
#
# raw_data_path = output_path
# output_path = "result_no_sub_class/"
#
# for big_class in (os.listdir(raw_data_path)):
#     os.mkdir(output_path + big_class)
#
#     for sub_class in (os.listdir(raw_data_path + big_class)):
#
#         for file in (os.listdir(raw_data_path + big_class + "/" + sub_class)):  # 9348 files, 9316 .jpg, le reste .JPG
#             shutil.copyfile(raw_data_path + big_cla