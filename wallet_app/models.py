from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    # Indexed for filtering/searching
    label = models.CharField(max_length=255, db_index=True)
    balance = models.DecimalField(max_digits=36, decimal_places=18, default=0)

    def __str__(self):
        return self.label

    class JSONAPIMeta:
        resource_name = "wallets"

    def update_balance(self):
        """
        Automatically update the wallet balance
        by summing all associated transactions
        """
        total = (
            Transaction.objects.filter(wallet_id=self.id).aggregate(
                total_amount=Sum("amount")
            )["total_amount"]
            or 0
        )
        self.balance = total
        self.save()


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    # Index foreign key for faster JOIN operations
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions",
        db_index=True,
    )
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)

    class JSONAPIMeta:
        resource_name = "transactions"

    def clean(self):
        """
        Ensure wallet balance does not go negative
        """
        future_balance = (
            self.wallet.transactions.aggregate(Sum("amount"))["amount__sum"]
            or 0
        ) + self.amount
        if future_balance < 0:
            raise ValidationError(
                "Transaction would result in a negative wallet balance."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.wallet.update_balance()
