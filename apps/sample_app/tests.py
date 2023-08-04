from django.test import TestCase

from sample_app.models import OrderHistory


class SimpleObjectsTestCase(TestCase):

    def test_sdf23(self):
        order_history_list: list[OrderHistory] = OrderHistory.simple_objects.filter(
            pk__in=[
                "202308121256_12344_qwefggwer3",
                "202308121256_12344_qwefggwer2",
                "202308121256_12344_qwefggwer",
            ]
        )

        print(order_history_list)
