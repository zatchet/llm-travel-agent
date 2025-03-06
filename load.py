from typing import List
from datasets import load_dataset
from datetime import date, time, datetime
import dataclasses


@dataclasses.dataclass
class Flight:
    id: int
    date: date
    airline: str
    flight_number: str
    origin: str
    destination: str
    departure_time: time
    arrival_time: time
    available_seats: int


def parse_flight(flight):
    return Flight(
        id=flight["id"],
        date=datetime.strptime(flight["date"], "%Y-%m-%d").date(),
        airline=flight["airline"],
        flight_number=flight["flight_number"],
        origin=flight["origin"],
        destination=flight["destination"],
        departure_time=datetime.strptime(flight["departure_time"], "%H:%M").time(),
        arrival_time=datetime.strptime(flight["arrival_time"], "%H:%M").time(),
        available_seats=flight["available_seats"],
    )


def load_flights_dataset() -> List[Flight]:
    return [
        parse_flight(flight)
        for flight in load_dataset("nuprl/llm-systems-flights", split="train")
    ]
