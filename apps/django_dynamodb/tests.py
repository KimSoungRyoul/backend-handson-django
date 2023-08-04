import boto3
from django.test import TestCase

from sample_app.models import OrderHistory


class ATestCase(TestCase):

    def test_sdf(self):

        order_history = OrderHistory.simple_objects.get(pk="202308121256_12344_qwefggwer3")

        client = boto3.client('dynamodb')
        res = client.get_item(
            Key={
                'order_number_pk': {
                    "S": "202308121256_12344_qwefggwer3",
                },
            },
            TableName='pycon2023_order_history_table',
        )
        #print(list(res["Item"].items()))

        #qs = OrderHistory.objects.filter(order_number_pk="202308121256_12344_qwefggwer3").only("order_number_pk", "status")

        qs = OrderHistory.objects.filter(status="ready_to_delivery").only("order_number_pk", "status")

        print(qs.query.sql_with_params()[0])

        res2 = client.execute_statement(
            Statement =OrderHistory.objects.filter(status__in=["ready_to_delivery"]).query.sql_with_params()[0],
            #Statement="SELECT * FROM pycon2023_order_history_table WHERE order_number_pk=?",
            Parameters=[
                {
                    "S": "ready_to_delivery"
                }
                # {
                #     "S": "202308121256_12344_qwefggwer3"
                # }
            ]

        )
        print(res2)

        for row in res2["Items"]:
            print(list(row.items()))