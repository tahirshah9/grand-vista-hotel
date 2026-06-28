from abc import ABC, abstractmethod

class Staff(ABC):
    def __init__(self, staff_id: str, name: str, shift: str):
        self._staff_id = staff_id
        self._name = name
        self._shift = shift

    @abstractmethod
    def get_role(self) -> str:
        pass

    def __str__(self):
        return f"{self.get_role()}: {self._name} ({self._shift} shift)"


class Receptionist(Staff):
    def get_role(self) -> str:
        return "Receptionist"

    def check_in_guest(self, reservation):
        reservation.status = "checked_in"


class HouseKeeper(Staff):
    def get_role(self) -> str:
        return "HouseKeeper"

    def mark_cleaned(self, room):
        room.status = "available"


class Manager(Staff):
    def get_role(self) -> str:
        return "Manager"

    def generate_report(self, db_manager) -> str:
        stats = db_manager.get_dashboard_stats()
        return f"Occupancy: {stats['occupied_rooms']}/{stats['total_rooms']} rooms | Revenue: ${stats['total_revenue']:.2f}"
