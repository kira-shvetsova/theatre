class ExternalPaymentClient:
    """Имитация внешнего API оплаты"""
    def make_charge(self, cents: int, card_token: str) -> dict:
        if cents <= 0:
            return {"status": "failed", "error": "Invalid amount"}
        return {"status": "ok", "transaction_id": "TXN123456"}


class PaymentResult:
    def __init__(self, success: bool, tx_id=None, error=None):
        self.success = success
        self.tx_id = tx_id
        self.error = error


class PaymentProcessor:
    """Наш интерфейс, который понимает остальная система"""
    def charge(self, amount: float, card_token: str) -> PaymentResult:
        raise NotImplementedError


class ExternalPaymentAdapter(PaymentProcessor):
    """Адаптер делает интерфейс внешнего клиента совместимым с нашим"""
    def __init__(self, client: ExternalPaymentClient):
        self.client = client

    def charge(self, amount: float, card_token: str) -> PaymentResult:
        cents = int(amount * 100)
        response = self.client.make_charge(cents, card_token)
        if response["status"] == "ok":
            return PaymentResult(True, tx_id=response["transaction_id"])
        return PaymentResult(False, error=response["error"])
