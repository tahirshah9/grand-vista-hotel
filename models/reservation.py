from datetime import date
from models.room import Room
from models.guest import Guest

class Reservation:
    def __init__(self, reservation_id: str, guest: Guest, room: Room, check_in: date, check_out: date):
        self.__reservation_id = reservation_id
        self.__guest = guest
        self.__room = room
        self.__check_in = check_in
        self.__check_out = check_out
        self.__status = "confirmed"

    @property
    def reservation_id(self) -> str:
        return self.__reservation_id
        
    @property
    def guest(self) -> Guest:
        return self.__guest
        
    @property
    def room(self) -> Room:
        return self.__room
        
    @property
    def check_in(self) -> date:
        return self.__check_in
        
    @property
    def check_out(self) -> date:
        return self.__check_out

    @property
    def status(self) -> str:
        return self.__status
        
    @status.setter
    def status(self, value: str):
        self.__status = value

    @property
    def duration(self) -> int:
        return (self.__check_out - self.__check_in).days

    def calculate_nights(self) -> int:
        return self.duration

    def calculate_total(self) -> float:
        return self.__room.calculate_price(self.duration)

    def cancel(self):
        self.__status = "cancelled"
        self.__room.status = "available"

    def __str__(self):
        return f"Reservation({self.__reservation_id}, {self.__guest.name}, Room {self.__room.room_number}, {self.__status})"
