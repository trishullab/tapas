from typing import Any, Text, TypeVar

ucd_3_2_0: UCD
ucnhash_CAPI: Any
unidata_version: str

_T = TypeVar("_T")

def bidirectional(__chr: Text) -> Text: ...
def category(__chr: Text) -> Text: ...
def combining(__chr: Text) -> int: ...
def decimal(__chr: Text, __default: _T = ...) -> int | _T: ...
def decomposition(__chr: Text) -> Text: ...
def digit(__chr: Text, __default: _T = ...) -> int | _T: ...
def east_asian_width(__chr: Text) -> Text: ...
def lookup(__name: Text | bytes) -> Text: ...
def mirrored(__chr: Text) -> int: ...
def name(__chr: Text, __default: _T = ...) -> Text | _T: ...
def normalize(__form: Text, __unistr: Text) -> Text: ...
def numeric(__chr: Text, __default: _T = ...) -> float | _T: ...

class UCD(object):
    # The methods below are constructed from the same array in C
    # (unicodedata_functions) and hence identical to the methods above.
    unidata_version: str
    def bidirectional(self, __chr: Text) -> str: ...
    def category(self, __chr: Text) -> str: ...
    def combining(self, __chr: Text) -> int: ...
    def decimal(self, __chr: Text, __default: _T = ...) -> int | _T: ...
    def decomposition(self, __chr: Text) -> str: ...
    def digit(self, __chr: Text, __default: _T = ...) -> int | _T: ...
    def east_asian_width(self, __chr: Text) -> str: ...
    def lookup(self, __name: Text | bytes) -> Text: ...
    def mirrored(self, __chr: Text) -> int: ...
    def name(self, __chr: Text, __default: _T = ...) -> Text | _T: ...
    def normalize(self, __form: Text, __unistr: Text) -> Text: ...
    def numeric(self, __chr: Text, __default: _T = ...) -> float | _T: ...