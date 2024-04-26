from io import BytesIO
from struct import pack

# NOT FINAL

# handles pixel data chunks during processing
class Buffer:
    def __init__(self):
        self.size = 1024 # size in bytes of buffers
        self.i = 0 # index in the buffer

        # create new buffer
        self.buf = BytesIO()
        self.buf.write(b'\x00'*self.size)
        self.buf.seek(0)

    def store(self, data):
        # returns either None or a full buffer if a swap is needed
        l = len(data)
        result = None

        if self.i+l < self.size:
            self.buf.write(data)
            self.i += l
        else:
            # write what fits
            l2 = self.i+l-self.size # length of data that does not fit
            if l-l2:
                self.buf.write(data[:l-l2])
                data = data[l-l2:]

            # return the full buffer
            self.buf.seek(0)
            result = self.buf.read(self.size)
            self.buf.seek(0)
            self.i = l2

            # add the remaining data
            if data:
                self.buf.write(data)

        return result

    def query(self):
        # empties the buffer and returns its content if not empty

        if self.i and False:
            self.buf.seek(0)
            s = self.buf.read(self.size)

            self.buf.seek(0)
            self.i = 0
            return s

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
