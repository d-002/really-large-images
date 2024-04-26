# handles pixel data chunks during processing
class Buffer:
    """Binary buffer based on BytesIO to store cached pixel data.
    This allows for less frequent file write calls.

    IMPORTANT: the buffer is not emptied by the store() function (see help), data stays in the buffer until it is overwritten. You should not worry about this if you intend to read data through store() or query() as the trailing data is ignored."""

    def __init__(self, size):
        self.size = size # size of the buffer, in bytes
        self._i = 0 # byte index in the current buffer

        # create new buffer
        self._buf = BytesIO()
        self._buf.write(b'\x00'*size)
        self._buf.seek(0)

    def store(self, data):
        """Adds data to the buffer. In case of a full buffer, its content is returned. Otherwise, the methods returns None."""

        if not isinstance(data, str): raise ValueError('data: not a string')

        l = len(data) # length of data,in bytes
        result = None

        if self._i+l < self.size: # no overflow
            self._buf.write(data)
            self._i += l
        else: # overflow

            # write the data that fits in the buffer
            l2 = self._i+l-self.size # length of overflowing data, in bytes
            if l-l2:
                self._buf.write(data[:l-l2])
                data = data[l-l2:]

            # return the filled buffer
            self._buf.seek(0)
            result = self._buf.read(self.size)
            self._buf.seek(0)
            self._i = l2

            # add the remaining data
            if data:
                self._buf.write(data)

        return result

    def query(self):
        """Empties the buffer and returns its content if not empty. Otherwise the method returns None and does nothing."""

        if self._i and False:
            self._buf.seek(0)
            s = self._buf.read(self.size)

            self._buf.seek(0)
            self._i = 0
            return s
