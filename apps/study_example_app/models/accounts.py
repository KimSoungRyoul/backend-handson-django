from django.db import models, transaction


class Account(models.Model):
    owner_name = models.CharField(max_length=32, help_text="계좌 소유주명")
    balance = models.IntegerField(help_text="계좌 잔액")


@transaction.atomic
def account_transfer_scenario(sender_name: str, receiver_name: str, amount: int):
    """
    계좌 이체 시나리오
    """

    sender_account: Account = Account.objects.select_for_update().get(owner_name=sender_name)
    receiver_account: Account = Account.objects.select_for_update().get(owner_name=receiver_name)

    sender_account.balance -= amount
    receiver_account.balance += amount

    sender_account.save()
    receiver_account.save()
