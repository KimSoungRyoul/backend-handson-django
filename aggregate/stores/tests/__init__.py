import requests
from django.test import TestCase

from aggregate.orders.models import Order
from aggregate.stores.models import Store
from aggregate.stores.models import StoreRepository
from aggregate.stores.models import StoreText
from aggregate.stores.models.store import StoreActiveSwitch
from aggregate.stores.models.store import StoreAddress
from aggregate.users.models import StoreOwner
from aggregate.users.models import User
# Create your tests here.


class DomainException:
    pass


def create_payment_history(data):
    return 1


class Payment:
    pass


class PaymentHistory:
    pass


class StoreModelTest(TestCase):
    def test_asdf(self):
        store = StoreRepository.create(
            name="김가네 국밥",
            store_type=Store.StoreType.FOOD,
            store_owner=StoreOwner.objects.create_user(username="asdfasdf", password="1234"),
            address=StoreAddress.objects.create(
                si="서울시", gu="서초구", gun="서초동", detail="마제스타시티 15층", lat=32.222, lng=128.234234,
            ),
        )
        store = StoreRepository.prefetch_related("storeactiveswitch_set", "storetext_set").get(id=store.id)

        print(id(StoreRepository))
        print(id(StoreRepository.all()))
        print(id(StoreRepository.filter(id=1)))

        print(id(Store.objects))
        print(id(Store.objects.all()))
        print(id(Store.objects.filter(id=1)))

        StoreRepository.switch_off(store, StoreActiveSwitch.SwitchType.OPEN)
        self.assertFalse(store.is_open)

        StoreRepository.switch_on(store, StoreActiveSwitch.SwitchType.OPEN)
        self.assertTrue(store.is_open)

        print(store.text(StoreText.TextType.LEGAL))
        print(store.text(StoreText.TextType.ORIGIN))

        # store_list: list[Store] = list(Store.objects.only_food_store())
        # print(store_list)

        #
        # stroe_owner = StoreOwner.objects.create_user(username="asdfasdf", password="1234", email="aaa@gmail.com")
        #
        # new_store: Store = StoreRepository.create(name="김가네 든든 국밥", store_owner=stroe_owner)
        #
        # print(new_store)

    def test_sdfsdff(self):

        user = User.objects.filter(id=1).first()
        order = Order.objects.create_order(...)

        response = requests.post(url="https://PG사/결제", data={"...": "..."})
        if response.status_code != 200:
            raise DomainException("결제 실패...")

        payment_history = create_payment_history(data=response.data)  # MongoDB INSERT

    def test_sdfdfgrgeg(self):
        user = User.objects.filter(id=1).first()  # RDB SELECT
        order = Order.objects.create_order(...)  # RDB INSERT
        payment = Payment.objects.creaet_payment(...)  # https:~~~  POST //APICall
        payment_history = PaymentHistory.objects.create_paymenthistory(payment)  # MongoDB INSERT

        ph_list = list(PaymentHistory.objects.filter(user=user))  # https:~~~/payment-history/{user_pk}  GET //APICall
