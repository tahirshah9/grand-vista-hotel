class Guest:
    def __init__(self, guest_id: str, name: str, email: str, phone: str, id_proof: str):
        self.__guest_id = guest_id
        self.__name = name
        self.__email = email
        self.__phone = phone
        self.__id_proof = id_proof
        self.__loyalty_points = 0

    @property
    def guest_id(self) -> str:
        return self.__guest_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email
        
    @property
    def phone(self) -> str:
        return self.__phone
        
    @property
    def id_proof(self) -> str:
        return self.__id_proof

    @property
    def loyalty_points(self) -> int:
        return self.__loyalty_points

    def earn_points(self, amount: float):
        self.__loyalty_points += int(amount // 10)

    def redeem_points(self, points: int):
        if points > self.__loyalty_points:
            raise ValueError("Insufficient loyalty points")
        self.__loyalty_points -= points

    def __eq__(self, other):
        return isinstance(other, Guest) and self.__guest_id == other.guest_id

    def __str__(self):
        return f"Guest({self.__name}, {self.__email}, Points: {self.__loyalty_points})"
