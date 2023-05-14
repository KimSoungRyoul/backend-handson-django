from typing import Any, Dict, List

from aggregate.users.models import Department, Staff
from django.contrib.auth.models import User
from django.test import TestCase
from user_management.serializers import StaffSchema


class UserTest(TestCase):
    def test_django_set_password_example(self):
        # 절대 이렇게 django User를 생성하지 말것!!
        wrong_user: User = User.objects.create(username="i_am_user", password="init_password1!!")
        print(wrong_user.password)  # 단방향 암호화 처리가 되어있지 않다.

        # django User는 django가 만들어준 create_user() 또는 create_superuser() 메서드를 사용해서 생성할것
        user: User = User.objects.create_user(username="i_am_user", password="init_password1!!")
        print(user.password)  # create_user()로 생성된 User의 비밀번호는 단방향 암호화 되어있다.

        user.set_password("password1!")
        user.save()  # set_password() 는 수정만 할뿐 저장하지는 않기때문에 비밀번호 수정후 save()를 호출해줘야한다.
        print(user.password)  # set_password() 메서드로 비밀번호를 수정하면 단방향 암호화처라가 같이 처리된다.

        user.password = "password1!"  # 비밀번호를 수정할때는 절대 이렇게 하지말것!!

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

    def test_staff_serializer(self):
        department = Department.objects.create(
            parent1_name="BIZ",
            parent2_name="상점관리실",
            parent3_name="사장님관리팀",
        )
        staff = Staff.objects.create_user(
            username="staff123",
            password="1234",
            email="qwerty@naver.com",
            is_staff=True,
            department=department,
        )

        staff_schema = StaffSchema(instance=staff)

        serialized_staff: Dict[str, Any] = staff_schema.data

        self.assertEquals(
            serialized_staff["department"],
            "BIZ>상점관리실>사장님관리팀",
            msg=" serialized_staff['department']는 문자열 포맷으로 조회되어야합니다.",
        )

    def test_staff_serializer_update(self):
        dp1 = Department.objects.create(
            parent1_name="BIZ",
            parent2_name="상점관리실",
            parent3_name="사장님관리팀",
        )
        dp2: Department = Department.objects.create(
            parent1_name="BIZ",
            parent2_name="고객상담팀",
            parent3_name="문의통계팀",
        )
        staff = Staff.objects.create_user(
            username="staff123",
            password="1234",
            email="qwerty@naver.com",
            is_staff=True,
            department=dp1,
        )

        staff_schema = StaffSchema(
            data={
                "department": f"{dp2.parent1_name}>{dp2.parent2_name}>{dp2.parent3_name}",
                "name_kor": "김첨지",
            },
            instance=staff,
            partial=True,
        )
        staff_schema.is_valid(raise_exception=True)
        staff_schema.save()  # StaffSchema.update() 호출

        serialized_staff: Dict[str, Any] = staff_schema.data

        self.assertEquals(
            serialized_staff["department"],
            "BIZ>고객상담팀>문의통계팀",
            msg="serialized_staff의 department가 기대한결과와 다릅니다.",
        )

    def test_staff_serializer_create(self):
        Department.objects.create(
            parent1_name="BIZ",
            parent2_name="상점관리실",
            parent3_name="사장님관리팀",
        )

        staff_schema = StaffSchema(
            data={
                "username": "staff123",
                "password": "1234",
                "email": "qwerty@naver.com",
                "name_kor": "김성렬",
                "is_staff": True,
                "department": "BIZ>상점관리실>사장님관리팀",
            }
        )
        staff_schema.is_valid(raise_exception=True)
        staff_schema.save()  # StaffSchema.create() 호출

        serialized_staff: Dict[str, Any] = staff_schema.data

        self.assertEquals(
            serialized_staff["department"],
            "BIZ>상점관리실>사장님관리팀",
            msg="serialized_staff의 department가 기대한결과와 다릅니다.",
        )
        self.assertIsNone(serialized_staff.get("password"), msg="password는 write_only_field임으로 조회되어서는 안됩니다.")
