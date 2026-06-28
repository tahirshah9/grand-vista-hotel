from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def process(self, amount: float) -> dict:
        pass


class CashPayment(Payment):
    def process(self, amount: float) -> dict:
        return {
            "method": "Cash",
            "amount": amount,
            "status": "success",
            "receipt": f"CASH-{int(amount)}"
        }


class CardPayment(Payment):
    def __init__(self, last4: str):
        self.__last4 = last4

    def process(self, amount: float) -> dict:
        return {
            "method": "Card",
            "last4": self.__last4,
            "amount": amount,
            "status": "success",
            "receipt": f"CARD-{self.__last4}-{int(amount)}"
        }


class UPIPayment(Payment):
    def __init__(self, upi_id: str):
        self.__upi_id = upi_id

    def process(self, amount: float) -> dict:
        return {
            "method": "UPI",
            "upi_id": self.__upi_id,
            "amount": amount,
            "status": "success",
            "receipt": f"UPI-{int(amount)}"
        }
