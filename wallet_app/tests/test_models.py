from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from wallet_app.models import Wallet, Transaction


@pytest.mark.django_db
def test_wallet_balance_update():
    wallet = Wallet.objects.create(label="Test Wallet")
    Transaction.objects.create(
        wallet=wallet, txid="tx1", amount=Decimal("50.00")
    )
    Transaction.objects.create(
        wallet=wallet, txid="tx2", amount=Decimal("-20.00")
    )
    wallet.refresh_from_db()
    assert wallet.balance == Decimal("30.00")


@pytest.mark.django_db
def test_transaction_negative_balance():
    wallet = Wallet.objects.create(label="Test Wallet")
    Transaction.objects.create(
        wallet=wallet, txid="tx1", amount=Decimal("50.00")
    )

    with pytest.raises(ValidationError):
        tx = Transaction(wallet=wallet, txid="tx2", amount=Decimal("-100.00"))
        tx.full_clean()
        tx.save()
