from PIL import Image
from PIL import ImageOps
from PIL import ImageChops
from random import shuffle
from random import randint
from random import choice
from nltk import FreqDist
import operator
import re
import os
from collections import defaultdict
from functools import reduce

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#https://hhsprings.bitbucket.io/docs/programming/examples/python/PIL/Image__Functions.html
def image_merge(in_file):
    img = Image.open(in_file).convert('RGB')
    size = img.size
    if size[0] > 1024 or size[1] > 512:
        img = ImageOps.scale(img, 0.75)
        print("size reduced")
    r, g, b = img.split()
    colours= []
    colours.extend([r,g,b])
    a = choice(colours)
    b = choice(colours)
    c = choice(colours)
    a = ImageChops.offset(a, randint(-20,20), randint(-10,10)) 
    #ImageChops.multiply(g, r).save(in_file+'_output.png')
    Image.merge("RGB", (a, b, c)).save(in_file+'_output.png')
    print("image_merge done\n")
    return in_file+'_output.png'

def colourize_image(in_file):
    img = Image.open(in_file)
    white = (246,114,128)
    black = (192,108,132)
    outfile = ImageOps.colorize(img, black, white)
    outfile.save(in_file+"_output.png")

def image_rgb_shift(in_file):
    img = Image.open(in_file).convert('RGB')
    r, g, b = img.split()
    Image.merge("RGB", (b,g,r)).save(in_file+'_output.png')
    print("image_rgb_shift done\n")
    return in_file+'_output.png'

def atkinson_dither(in_file):
    img = Image.open(in_file).convert('L')
    pix = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            old = pix[x, y]
            new = 0 if old < 127 else 255
            pix[x, y] = new
            quant_error = old - new
            if x < w - 1:
                pix[x + 1, y] += quant_error * 1 // 8
            if x < w - 2:
                pix[x + 2, y] += quant_error * 1 // 8
            if x > 0 and y < h - 1:
                pix[x - 1, y + 1] += quant_error * 1 // 8
            if y < h - 1:
                pix[x, y + 1] += quant_error * 1 // 8
            if y < h - 2:
                pix[x, y + 2] += quant_error * 1 // 8
            if x < w - 1 and y < h - 1:
                pix[x + 1, y + 1] += quant_error * 1 // 8
    
    if w > 1024 or h > 512:
        img = ImageOps.scale(img,0.75)
    img.save(in_file+"_output.png")
    return in_file+'_output.png'   

#https://stackoverflow.com/questions/30520666/pixelate-image-with-pillow/30527715
def generate_pixel_image(in_file):
    block_size = 16
    size = (block_size,block_size)
    im = Image.open(in_file).convert('RGB')
    img_data = list(im.getdata())
    length = len(list(im.getdata()))
    freq_dist = FreqDist(set(img_data))
    top_ten_colours = freq_dist.most_common(256)
    palette = [] 
    for colour in top_ten_colours:
        palette.append(colour[0])
    while len(palette)<256:
        palette.append((0,0,0))
    try:
        flat_palette = reduce(lambda a, b: a+b, palette)
        assert len(flat_palette)== 768
        palette_img = Image.new('P', (1, 1), 0)
        palette_img.putpalette(flat_palette)
        multiplier = 8
        scaled_img = im.resize((size[0] * multiplier, size[1] * multiplier), Image.ANTIALIAS)
        reduced_img = scaled_img.quantize(palette=palette_img)
        rgb_img = reduced_img.convert('RGB')
        out = Image.new('RGB', size)
        for x in range(size[0]):
            for y in range(size[1]):
            #sample and get average color in the corresponding square
                histogram = defaultdict(int)
                for x2 in range(x * multiplier, (x + 1) * multiplier):
                    for y2 in range(y * multiplier, (y + 1) * multiplier):
                        histogram[rgb_img.getpixel((x2,y2))] += 1
                color = max(histogram.items(), key=operator.itemgetter(1))[0]
                out.putpixel((x, y), color)

        new_file = ImageOps.scale(out, 50)
        out_file, ext = in_file, ext = os.path.splitext(in_file)
        new_file.save(out_file + "_output.png")
        print("pixe_image done")
        return(out_file+"_output.png")
    #https://docs.python.org/3/tutorial/errors.html
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        return(in_file)


def pixelate_image(filename):
    image = Image.open(filename)
    img_data = list(image.getdata())
    freq_dist_top_1 = FreqDist(img_data)
    top_1_colour = freq_dist_top_1.most_common(1)[0][0]
    backgroundColor = top_1_colour
    pixelSize = 9
    image = image.resize((int(image.size[0]/pixelSize), int(image.size[1]/pixelSize)), Image.ANTIALIAS)
    image = image.resize((image.size[0]*pixelSize, image.size[1]*pixelSize), Image.ANTIALIAS)
    pixel = image.load()

    for i in range(0,image.size[0],pixelSize):
        for j in range(0,image.size[1],pixelSize):
            for r in range(pixelSize):
                pixel[i+r,j] = backgroundColor
                pixel[i,j+r] = backgroundColor
    
    image.save('pixelated.png')

def colour_dither(in_file):
    img = Image.open(in_file).convert('RGB')
    print('hello')
    size = img.size
    if size[0] > 1024 or size[1] > 512:
        img = ImageOps.scale(img, 0.75)
        print("size reduced")
    img_data = list(img.getdata())
    length = len(list(img.getdata()))
    freq_dist = FreqDist(img_data)
    top_ten_colours = freq_dist.most_common(256)
    palette = []
    for colour in top_ten_colours:
        palette.append(colour[0])
    while len(palette)<256:
        palette.append((0,0,0))
    try:
        flat_palette = reduce(lambda a, b: a+b, palette)
        assert len(flat_palette)== 768
        palette_img = Image.new('P', (1, 1), 0)
        palette_img.putpalette(flat_palette)
        newimage = img.quantize(palette=palette_img)
        newimage.save(in_file+'_output.png')
        return in_file+'_output.png'
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        return in_file

