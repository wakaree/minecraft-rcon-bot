from typing import TYPE_CHECKING, Annotated, NewType, TypeAlias

from pydantic import PlainValidator

if TYPE_CHECKING:
    ListStr: TypeAlias = list[str]
    ListInt: TypeAlias = list[int]
else:
    ListStr = NewType("ListStr", list[str])
    ListInt = NewType("ListInt", list[int])

StringList: TypeAlias = Annotated[ListStr, PlainValidator(func=lambda x: x.split(","))]
IntList: TypeAlias = Annotated[
    ListInt,
    PlainValidator(func=lambda x: [int(i) for i in x.split(",")]),
]
