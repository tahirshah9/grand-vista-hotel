from abc import ABC, abstractmethod

class Room(ABC):
    def __init__(self, room_number: str, floor: int, price_per_night: float):
        self.__room_number = room_number
        self.__floor = floor
        self.__price_per_night = price_per_night
        self.__status = "available"

    @property
    def room_number(self) -> str:
        return self.__room_number

    @property
    def floor(self) -> int:
        return self.__floor

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, value: str):
        if value not in ["available", "occupied", "maintenance"]:
            raise ValueError("Invalid status")
        self.__status = value

    @property
    def price_per_night(self) -> float:
        return self.__price_per_night

    @abstractmethod
    def calculate_price(self, nights: int) -> float:
        pass

    @abstractmethod
    def get_room_type(self) -> str:
        pass

    def __str__(self):
        return f"[{self.get_room_type()}] Room {self.room_number} - Floor {self.__floor} - ${self.__price_per_night}/night - {self.status}"

    def __repr__(self):
        return f"Room({self.room_number}, {self.get_room_type()}, {self.status})"


class SingleRoom(Room):
    def calculate_price(self, nights: int) -> float:
        return self.price_per_night * nights

    def get_room_type(self) -> str:
        return "SingleRoom"


class DoubleRoom(Room):
    def calculate_price(self, nights: int) -> float:
        return self.price_per_night * nights * 1.05

    def get_room_type(self) -> str:
        return "DoubleRoom"


class DeluxeRoom(Room):
    def calculate_price(self, nights: int) -> float:
        return self.price_per_night * nights * 1.15

    def get_room_type(self) -> str:
        return "DeluxeRoom"


class Suite(Room):
    def calculate_price(self, nights: int) -> float:
        return self.price_per_night * nights * 1.20

    def get_room_type(self) -> str:
        return "Suite"
