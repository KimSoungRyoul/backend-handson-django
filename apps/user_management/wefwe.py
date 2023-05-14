import typing as t
from typing import NotRequired, Required, TypedDict, get_type_hints

import pydantic
from pydantic import BaseModel


class NestedAsdf(TypedDict):
    tdtd444: NotRequired[t.Dict[str, int]]
    tt444: t.Tuple[int, str, bool]
    t_list11: t.List[bool]
    list11: list[bool]
    pydantic_union1: list[str, int]
    pydantic_union2: str | int
    pydantic_union3: t.List[str | int]
    union4: t.Union[str, int]


class Asdf(TypedDict):
    qwe_sdf: str
    trtrt: int
    nested_typ_dict: NestedAsdf


class IrisFeaturesTypedDict(TypedDict):
    sepal_len: float
    sepal_width: float
    petal_len: float
    petal_width: Required[float]
    asdf_qq: Asdf
    tdtd1: NotRequired[t.Dict[str, int]]
    tt22: t.Tuple[int, str, bool]
    ss22: t.Set[int]
    ll22: t.List[str]
    dd22: t.Dict[str, int]
    dd222: t.Dict[int, str]

    # Optional Field
    request_id: NotRequired[int]


class IrisFeaturesPydantic(BaseModel):
    sepal_len: float
    sepal_width: float
    petal_len: float
    petal_width: Required[float]
    asdf_qq: Asdf
    tdtd1: NotRequired[t.Dict[str, int]]
    tt22: t.Tuple[int, str, bool]
    ss22: t.Set[int]
    ll22: t.List[str]
    dd22: t.Dict[str, int]
    dd222: t.Dict[int, str]

    # Optional Field
    request_id: NotRequired[int]


# py3.11
aaa = get_type_hints(NestedAsdf, include_extras=True)  # no error

for kk in aaa.items():
    print(kk)

# {'tdtd444': typing.NotRequired[typing.Dict[str, int]], 'tt444': typing.Tuple[int, str, bool], 't_list11': typing.List[bool], 'list11': list[bool]}

print(pydantic.__version__)
