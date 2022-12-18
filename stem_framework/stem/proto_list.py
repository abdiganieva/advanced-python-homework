from typing import Type, Iterable, Sized, Iterator, NewType
from google.protobuf.reflection import GeneratedProtocolMessageType


class ProtoList(Sized, Iterable):

    def __init__(self, path, proto_class: GeneratedProtocolMessageType):
        self.path = path
        self.proto_class = proto_class

    def __enter__(self) -> "ProtoList":
        self.file = open(self.path, 'rb')

        self.msg_len = []
        self.msg_pos = []

        while (N := self.file.read(8)) != b'':
            self.msg_pos.append(self.file.tell())
            N = int.from_bytes(N)
            self.msg_len.append(N)
            self.file.seek(N, 1)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.__exit__(exc_type, exc_val, exc_tb)

    def __len__(self) -> int:
        return self.msg_len.__len__()

    def __getitem__(self, item):
        self.file.seek(self.msg_pos[item])
        N = self.msg_len[item]
        return self.proto_class().ParseFromString(self.file.read(N))

    def __iter__(self) -> Iterator[GeneratedProtocolMessageType]:
        for n in range(self.__len__()):
            yield self[n]
