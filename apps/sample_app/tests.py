from django.test import TestCase

from sample_app.models import OrderHistory


class SimpleObjectsTestCase(TestCase):

    def test_pynamodb_batch_get(self):
        # 미리 넣어놓은 데이터
        order_number_list = [
            "20230813-123234-00003459",
            "20230813-123234-00003458",
            "20230813-123234-00003457",
            "20230813-123234-00003456",
        ]

        orderhistory_list = list(OrderHistory.batch_get(items=order_number_list))

        self.assertEqual(len(orderhistory_list), 4)

# dummy_generator
# order_history = OrderHistory(
#         order_number=order_number,
#         store_id=123234,
#         current_status=Status.COMPLETE.value,
#         snapshots=[
#             OrderSnapshot(
#                 order_number=order_number,
#                 history_id=f"{order_number}-{uuid.uuid4()}",
#                 store_id=123234,
#                 status=Status.COOKING.value,
#                 address=default_address(),
#                 total_price=13_000,
#                 comment="주문이 사장님에 의해 수락되었습니다. 조리를 시작합니다.",
#             ),
#             OrderSnapshot(
#                 order_number=order_number,
#                 history_id=f"{order_number}-{uuid.uuid4()}",
#                 store_id=123234,
#                 status=Status.COOKING.value,
#                 address=default_address(),
#                 total_price=12_000,
#                 comment="주문 금액이 수정되었습니다.",
#             ),
#             OrderSnapshot(
#                 order_number=order_number,
#                 history_id=f"{order_number}-{uuid.uuid4()}",
#                 store_id=123234,
#                 status=Status.WAIT_FOR_ACCEPT.value,
#                 address=default_address(),
#                 total_price=12_000,
#                 comment="조리가 완료되었습니다. 배달기사가 음식을 수령할때까지 대기합니다.",
#             ),
#             OrderSnapshot(
#                 order_number=order_number,
#                 history_id=f"{order_number}-{uuid.uuid4()}",
#                 store_id=123234,
#                 status=Status.DELIVERY.value,
#                 address=default_address(),
#                 total_price=12_000,
#                 comment="배달기사가 음식을 수령했습니다. 배달중입니다.",
#             ),
#             OrderSnapshot(
#                 order_number=order_number,
#                 history_id=f"{order_number}-{uuid.uuid4()}",
#                 store_id=123234,
#                 status=Status.COMPLETE.value,
#                 address=default_address(),
#                 total_price=12_000,
#                 comment="배달이 완료되었습니다. 리뷰 서비스로 해당 이벤트를 전달합니다.",
#             )
#         ],
#     )
#     order_history.save()
