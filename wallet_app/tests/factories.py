from decimal import Decimal

import factory

from wallet_app.models import Wallet, Transaction


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wallet

    label = factory.Faker("word")


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    wallet = factory.SubFactory(WalletFactory)
    txid = factory.Faker("uuid4")
    amount = Decimal("100.00")
