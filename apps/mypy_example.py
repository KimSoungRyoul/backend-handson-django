from decimal import Decimal
from typing import List, TextIO,BinaryIO


def test_TypeHint_사용예시(self):
    num_list: List[int] = [1, 2, 3, 4, 5]
    num_list2: List[int | float] = [1, 1.2, 2, 2.8, 3, 3.3, 4, 5]

    def 함수에_타입명시_예시(a: str, b: str) -> bool:
        return a == b


def test_python_개발자를_괴롭히는_방법1(self):
    num_list: List[int] = [1, 2, "3", 4, "난숫자아님"]

    num_list2: List[int] = "1,2,3,4"

    a_str1: str = [11, 22, 33]

    b_str: str = "a,b,c,d,e,f"
    b_str: List[str] = b_str.split()  # 처음에는 타입이 맞았지만 누군가 수정해서 타입이 맞지 않는 경우






a: Decimal = Decimal("0.045")
b: Decimal = Decimal("0.01")
print(f"a-b: {a-b}")



txt_file: TextIO = open("./i_am_file.txt")

print(txt_file.read())