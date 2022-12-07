import array
import mmap
from asyncio import StreamReader, StreamWriter
from io import RawIOBase, BufferedReader
from json import JSONEncoder
from typing import Optional, Union, Any
from .meta import Meta


Binary = Union[bytes, bytearray, memoryview, array.array, mmap.mmap]


class MetaEncoder(JSONEncoder):

    def default(self, obj: Meta) -> Any:
        if is_dataclass(obj):
            return asdict(obj)
        elif isinstance(obj, dict):
            return obj
        else:
            raise TypeError


class Envelope:
    _MAX_SIZE = 128*1024*1024 # 128 Mb

    def __init__(self, meta: Meta, data : Optional[Binary] = None):
        self.meta = meta
        self.data = data

    def __str__(self):
        return str(self.meta)

    @staticmethod
    def read(input: BufferedReader | BytesIO) -> "Envelope":
    
        if isinstance(input, (bytes, bytearray)):
            stream = io.BytesIO(input)
        elif isinstance(input, io.BufferedReader):
            stream = input
        else:
            raise ValueError("data should be either bytearray or file 'rb' mode.")
            
        assert b'#~'   == stream.read(2), "Illegal beginning (not #~)"
        assert b'DF02' == stream.read(4), 'Illegal envelope format type'
        stream.read(2)

        metaLength = int.from_bytes(stream.read(4))
        data = int.from_bytes(stream.read(4))

        dataLength = json.loads(stream.read(metaLength))

        if dataLength < Envelope._MAX_SIZE:
            data = stream.read(dataLength)
        else:
            data = mmap.mmap(stream.fileno(), dataLength, offset = stream.tell())

        assert b'~#' == stream.read(2), "Envelope byte sequence doesn't end with b'~#'"

        return Envelope(meta, data)


    @staticmethod
    def from_bytes(buffer: bytes) -> "Envelope":
        return Envelope.read(BytesIO(buffer))


    def to_bytes(self) -> bytes:
        output = BytesIO()
        self.write_to(output)
        output.seek(0)
        return output.read()


    def write_to(self, output: RawIOBase | BytesIO):
        output.write(b'#~')
        output.write(b'DF02')
        output.write(b'..')
        meta_str = bytes(json.dumps(self.meta), 'utf8')

        output.write(len(meta_str ).to_bytes(4))
        output.write(len(self.data).to_bytes(4))
        output.write(meta_str)
        output.write(self.data)

        output.write(b'~#')