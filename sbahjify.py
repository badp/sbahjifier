#!/usr/bin/python2
from __future__ import print_function

import os.path
import sys

import PIL.Image
import PIL.ImageFilter
import PIL.ImageOps


def sbahjify(filename, outname):
    with open(filename, 'rb') as read_file:
        im = PIL.Image.open(read_file)
        # DO NOT USE CONTOUR, EMBOSS, FIND_EDGES

        for _ in xrange(2):
            im = PIL.ImageOps.equalize(im)  # Drab-ify, but embellish otherwise hidden artifacts
            im = PIL.ImageOps.solarize(im, 250)  # Create weird blotchy artifacts, but inverts huge swaths
            im = PIL.ImageOps.posterize(im, 2)  # Flatten colors
            for _ in xrange(2):
                im = im.filter(PIL.ImageFilter.SHARPEN)
                im = im.filter(PIL.ImageFilter.SMOOTH)
                im = im.filter(PIL.ImageFilter.SHARPEN)
        w, h = im.size
        im = im.resize((w, int(h * 0.7)))
        im = PIL.ImageOps.equalize(im)  # Drab-ify, but embellish otherwise hidden artifacts
        im = im.filter(PIL.ImageFilter.SHARPEN)
        im = im.filter(PIL.ImageFilter.SHARPEN)

        with open(outname, 'wb') as save_file:
            im.save(save_file, quality=0, optimize=False, progressive=False)


if __name__ == '__main__':
    if len(sys.argv) != 0: #some stuff takes first as "sbahjify.py ugh"
        for arg in sys.argv:
            sbahjify(arg, "sbah-"+arg)
    else:
        for filename in os.listdir('src'):
            if not (filename.endswith('.jpg') or filename.endswith('.jpeg')):
                continue
            print(filename, end=' ... ')
            sys.stdout.flush()
            sbahjify(os.path.join('src', filename), os.path.join('dest', filename))
            print('Done!')
