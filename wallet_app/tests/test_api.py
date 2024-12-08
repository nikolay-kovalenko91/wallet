import pytest
from rest_framework.test import APIClient

from wallet_app.tests.factories import WalletFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


def test_json_api_create_wallet(api_client):
    response = api_client.post(
        "/api/wallets/",
        {"data": {"type": "wallets", "attributes": {"label": "My Wallet"}}},
        format="vnd.api+json",
    )
    assert response.status_code == 201
    assert response.data["label"] == "My Wallet"


def test_json_api_list_wallets(api_client):
    WalletFactory.create_batch(3)
    response = api_client.get(
        "/api/wallets/",
    )
    assert response.status_code == 200
    assert len(response.data["results"]) == 3


def test_json_api_create_transaction(api_client):
    wallet = WalletFactory()
    response = api_client.post(
        "/api/transactions/",
        {
            "data": {
                "type": "transactions",
                "attributes": {"txid": "unique_tx_123", "amount": "50.00"},
                "relationships": {
                    "wallet": {
                        "data": {"type": "wallets", "id": str(wallet.id)}
                    }
                },
            }
        },
        format="vnd.api+json",
    )
    assert response.status_code == 201, response.data
    assert response.data["txid"] == "unique_tx_123"
