from io import BytesIO
from struct import pack

from .buffer import *

# NOT FINAL

buf = Buffer()

file = 'test.bmp'
w, h = 1024, 1024
psize = 3 # pixel size: 3 for RGB, 4 for RGBA
hoffset = 26 # header offset before data
fsize = hoffset+psize*w*h
csize = 1024 # size in bytes of the pixel data chunks during processing

pixels = [0]*w*h
for x in range(w):
    for y in range(h):
        pixels[y*w + x] = (int(x*255/w) << 16) + int(y*255/h)

BM = 19778 # bitmap signature
pformat = '<' + 'B'*psize

with open(file, 'wb') as f:
    # BITMAPFILEHEADER
    f.write(pack('<HLHHL', BM, fsize, 0, 0, hoffset))

    # BITMAPCOREHEADER
    f.write(pack('<LHHHH', 12, w, h, 1, psize<<3))

    # Image Data
    idata = b''
    for y in range(h-1, -1, -1): # reversed y order
        i = y*w
        if psize == 3: # separate pixel components and add them separately
            for _ in range(w):
                p = pixels[i]
                r = p&0xff
                g = p>>8&0xff
                b = p>>16
                add = buf.store(pack('<BBB', b, g, r))
                if add is not None: idata = b''.join((idata, add))
                i += 1
        elif psize == 4: # add the whole pixel as a double
            for _ in range(w):
                add = buf.store(pack('<Q', pixels[i]))
                if add is not None: idata = b''.join((idata, add))
                i += 1
        print('%d%%' %(100-y/h*100))

        # padding to a multiple of 4 bytes per row
        pad = (4 - w%4) % 4
        add = buf.store(b'\x00'*pad)
        if add is not None: idata += b''.join((idata, add))

    # add rest of buffer if not empty
    add = buf.query()
    if add is not None: data = b''.join((idata, add))

    f.write(idata)
