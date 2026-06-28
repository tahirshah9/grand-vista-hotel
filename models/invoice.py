from models.reservation import Reservation

class Invoice:
    TAX_RATE = 0.10

    def __init__(self, invoice_id: str, reservation: Reservation):
        self.__invoice_id = invoice_id
        self.__reservation = reservation
        self.__extras = []
        
    @property
    def invoice_id(self) -> str:
        return self.__invoice_id
        
    @property
    def reservation(self) -> Reservation:
        return self.__reservation

    def add_extra(self, name: str, amount: float):
        self.__extras.append({"name": name, "amount": amount})

    def calculate_subtotal(self) -> float:
        return self.__reservation.calculate_total() + sum(e["amount"] for e in self.__extras)

    def calculate_tax(self) -> float:
        return self.calculate_subtotal() * self.TAX_RATE

    def calculate_total(self) -> float:
        return self.calculate_subtotal() + self.calculate_tax()

    def generate_summary(self) -> str:
        lines = [
            "=" * 40,
            "   GRAND VISTA HOTEL - INVOICE",
            "=" * 40,
            f"Invoice ID : {self.__invoice_id}",
            "-" * 40,
            f"Room Charge: ${self.__reservation.calculate_total():.2f}",
        ]
        for e in self.__extras:
            lines.append(f"{e['name']:<20}: ${e['amount']:.2f}")
        lines += [
            "-" * 40,
            f"Subtotal   : ${self.calculate_subtotal():.2f}",
            f"Tax (10%)  : ${self.calculate_tax():.2f}",
            "=" * 40,
            f"TOTAL      : ${self.calculate_total():.2f}",
            "=" * 40,
        ]
        return "\n".join(lines)
