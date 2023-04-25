from typing import List


def test_TypeHint_사용예시(self):
    num_list: List[int] = [1, 2, 3, 4, 5]
    num_list2: List[int | float] = [1, 1.2, 2, 2.8, 3, 3.3, 4, 5]

    def 함수에_타입명시_예시(a: str, b: str) -> bool:
        return a == b


def test_python_개발자를_괴롭히는_방법1(self):
    num_list: List[int] = [1, 2, "3", 4, "난숫자아님"]

    num_list: List[int] = "1,2,3,4"

    a_str1: str = [11, 22, 33]

    def 함수에서_뭐가_반환될지_모르지(a: str, b: str) -> bool:
        return a == b
