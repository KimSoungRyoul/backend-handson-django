import boto3
import botocore
from django.test import TestCase

# Create your tests here.


class DjangoDynamoDBTestCase(TestCase):
    def test_asdf(self):
        client_config = botocore.config.Config(
            max_pool_connections=25,
        )
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("pycon2023_order_history_table")
        print(table.key_schema)
        print(table)
        print("asdf")
        item = {"order_number_pk": "202308121256_12344_qwefggwer3", "status": "ready_to_delivery"}
        resp = table.put_item(Item=item, ReturnValues="ALL_OLD")
        print(resp)

        res2 = table.get_item(
            Key={"order_number_pk": "202308121256_12344_qwefggwer3"},
            AttributesToGet=[
               "order_number_pk", "status",
            ],
        )
        print(res2)

        # with table.batch_writer() as batch:
        #     for _ in range(3):
        #         batch.put_item(
        #             Item={
        #                 'order_status': "ready_to_delivery",
        #             },
        #             Expected={
        #                 'order_status': {
        #                     'Value': 'string' | 123 | Binary(b'bytes') | True | None | set(['string']) | set(
        #                         [123]) | set([Binary(b'bytes')]) | [] | {},
        #                     'Exists': True | False,
        #                     'ComparisonOperator': 'EQ' | 'NE' | 'IN' | 'LE' | 'LT' | 'GE' | 'GT' | 'BETWEEN' | 'NOT_NULL' | 'NULL' | 'CONTAINS' | 'NOT_CONTAINS' | 'BEGINS_WITH',
        #                     'AttributeValueList': [
        #                         'string' | 123 | Binary(b'bytes') | True | None | set(['string']) | set([123]) | set(
        #                             [Binary(b'bytes')]) | [] | {},
        #                     ]
        #                 }
        #             },
        #
        #         )
