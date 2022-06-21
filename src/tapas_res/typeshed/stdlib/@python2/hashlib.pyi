_DataType = str | unicode | bytearray | buffer | memoryview

class _hash(object):  # This is not actually in the module namespace.
    @property
    def name(self) -> str: ...
    @property
    def block_size(self) -> int: ...
    @property
    def digest_size(self) -> int: ...
    @property
    def digestsize(self) -> int: ...
    def __init__(self, arg: _DataType = ...) -> None: ...
    def update(self, arg: _DataType) -> None: ...
    def digest(self) -> str: ...
    def hexdigest(self) -> str: ...
    def copy(self) -> _hash: ...

def new(name: str, data: str = ...) -> _hash: ...
def md5(s: _DataType = ...) -> _hash: ...
def sha1(s: _DataType = ...) -> _hash: ...
def sha224(s: _DataType = ...) -> _hash: ...
def sha256(s: _DataType = ...) -> _hash: ...
def sha384(s: _DataType = ...) -> _hash: ...
def sha512(s: _DataType = ...) -> _hash: ...

algorithms: tuple[str, ...]
algorithms_guaranteed: tuple[str, ...]
algorithms_available: tuple[str, ...]

def pbkdf2_hmac(name: str, password: str, salt: str, rounds: int, dklen: int = ...) -> str: ...