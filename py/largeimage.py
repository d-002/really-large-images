class LargeImage:
    def __init__(self, w, h, filef='png', pixelf='rgba', malloc=1024, chunksize=1048576, bufsize=4096, chunk_errors=True):
        """Very large images handler, manages image chunks and memory usage.
        Constructor parameters:
        - w, h (long): image size
        - filef (str): file format. Either 'bmp' or 'png'. Defaults to 'png'
        - pixelf (str): pixel format. Either 'rgb' or 'rgba'. Color values are 8b integers. Defaults to 'rgba'
        - malloc (MiB): allowed memory space for this LargeImage. Check permissions before allowing too much space. Chunks will be created ad cache according to this setting. Defaults to 1024MiB
        - bufsize (byte): advanced setting, controls the size of the inner string buffers for file loading. Higher values mean less file write calls, but increased memory usage. Defaults to 4096B.
        - chunksize (pixel): advanced setting, controls the size of the chunks in pixels (size therefore depends on pixel format). Higher values mean less chunks load/unload, but increased memory usage. Defaults
        - chunk_errors (bool): whether to raise Exceptions on chunk allocation failures. If set to False, no exceptions will be thrown and the manager will try to find an alternative. Changing this setting can prevent crashes while merging, but is generally less stable. Defaults to True (raise exceptions)"""

        # check arguments
        if filef not in ('bmp', 'png'): raise NotImplementedError('File format not supported')
        if filef == 'png': raise NotImplementedError('stay tuned for updates, coming soon')
        if pixelf == 'rgb': self.psize = 3
        elif pixelf == 'rgba': self.psize = 4
        else: raise ValueError('incorrect pixel format')
        if ext = 'bmp' and (w > 65535 or h > 65535):
            raise ValueError('Image too large for bmp file format')
        if chunksize == 0: raise ValueError('chunksize cannot be null')
        if bufsize == 0: raise ValueError('bufsize cannot be null')
        if malloc < bufsize>>20: raise ValueError('malloc must be greater or equal to chunksize')

        self.w = w
        self.h = h
        self.filef = filef
        self.malloc = malloc
        self.n_chunks = int(malloc/chunksize)
        self.chunksize = chunksize
        self.bufsize = bufsize
        self.chunk_errors = chunk_errors
