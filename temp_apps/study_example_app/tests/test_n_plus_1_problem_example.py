from django.test import TestCase
from study_example_app.models.n_plus_1_example_models import Menu, Restaurant


class NPlus1ProblemTest(TestCase):
    def setUp(self) -> None:
        r1 = Restaurant.objects.create(name="고급 레스토랑 In Back 스테이크 하우스", tel_num="070-1111-2222")
        Menu.objects.create(name="토마토 치오피노 파스타", price=20500, restaurant=r1)
        Menu.objects.create(name="투움바 스테이크 파스타", price=28900, restaurant=r1)
        Menu.objects.create(name="베이비 백 립", price=37900, restaurant=r1)
        Menu.objects.create(name="슈림프 감바스 셀러드", price=19900, restaurant=r1)
        Menu.objects.create(name="카프레제", price=19900, restaurant=r1)

    def test_n_plus_1_example(self):
        menu_queryset = Menu.objects.all()

        # 이 반복문 속에서 발생하는 SQL의 갯수는 몇개일까?
        # 1 + N (for문에서 Menu의 갯수만큼 Restaurant이 N번 더 조회됨)
        with self.assertNumQueries(1 + Menu.objects.all().count()):
            for menu in menu_queryset:
                print("\n-----------------------")
                print(f"메뉴 이름: {menu.name}")
                print(f"메뉴 가격: {menu.price}")
                print(f"메뉴를 판매하는 음식점 이름: {menu.restaurant.name}")
                print("-----------------------\n")

    def test_resolve_n_plus_1_example(self):
        menu_queryset = Menu.objects.select_related("restaurant").all()
        # select_related("restaurant") 라는 EagerLoading 옵션이 붙었기 때문에 SQL에 JOIN문이 추가됨
        # SELECT "study_example_app_menu"."id",
        #        "study_example_app_menu"."name",
        #         "study_example_app_menu"."price",
        #         "study_example_app_menu"."restaurant_id",
        #         "study_example_app_restaurant"."id",
        #         "study_example_app_restaurant"."name",
        #         "study_example_app_restaurant"."tel_num"
        #  FROM "study_example_app_menu"
        #       INNER JOIN "study_example_app_restaurant" ON ("study_example_app_menu"."restaurant_id" = "study_example_app_restaurant"."id")

        # 이 반복문 속에서 발생하는 SQL의 갯수는 몇개일까?
        # select_related("restaurant")이 붙었기 때문에 SQL이 1개만 발생함
        with self.assertNumQueries(1):
            for menu in menu_queryset:
                print("\n-----------------------")
                print(f"메뉴 이름: {menu.name}")
                print(f"메뉴 가격: {menu.price}")
                print(f"메뉴를 판매하는 음식점 이름: {menu.restaurant.name}")
                print("-----------------------\n")
