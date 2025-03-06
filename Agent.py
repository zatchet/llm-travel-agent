from typing import List, Optional
from openai import OpenAI
from load import Flight
import datetime
import dataclasses
import os

@dataclasses.dataclass
class AgentResponse:
    """
    The superclass for all agent responses.
    """
    text: str

@dataclasses.dataclass
class FindFlightsResponse(AgentResponse):
    """
    The agent used the `find_flights` tool and found the following flights.
    """
    available_flights: List[int]

@dataclasses.dataclass
class BookFlightResponse(AgentResponse):
    """
    The agent used the `book_flight` tool and booked the following flight.
    """
    booked_flight: Optional[int]

@dataclasses.dataclass
class TextResponse(AgentResponse):
    pass

class Agent:
    def __init__(self, flights: List[Flight]):
        self.flights = flights
        BASE_URL = os.getenv('CS4973_BASE_URL')
        API_KEY=api_key=os.getenv('CS4973_API_KEY')
        self.client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
        self.conversation = [{
            "role": "system", 
            "content": '''
            Today is January 1, 2023. You are a travel agent. 
            All origins and destinations should be airport acronyms.
            Given a user prompt, you should do one of three things. Don't say anything extra:
            1. Return "self.find_flights(origin: str, destination: str, date: datetime.date)".
            2. Return "self.book_flight(int)"
            3. Return "You're welcome!"
            '''}] 

    def find_flights(self, origin: str, destination: str, date: datetime.date) -> List[Flight]:
        result = []
        for flight in self.flights:
            if flight.origin == origin and flight.destination == destination and flight.date == date:
                result.append(flight.id)
        return result
        
    def book_flight(self, flight_id: int) -> Optional[int]:
        for flight in self.flights:
            if flight.id == flight_id and flight.available_seats > 0:
                flight.available_seats -= 1
                return flight.id
        return None

    def say(self, user_message: str) -> AgentResponse:
        self.conversation.append({"role": "user", "content": user_message})
        resp = self.client.chat.completions.create(
            messages = self.conversation,
            model = "meta-llama/Meta-Llama-3.1-8B-Instruct",
            temperature=0)
        model_response = resp.choices[0].message.content
        
        if model_response.startswith("self.find_flights"):
            flights = eval(model_response)
            self.conversation.append({"role": "assistant", "content": str(flights)})
            return FindFlightsResponse(text=f"Here are your flights: {flights}", available_flights=flights)
        elif model_response.startswith("self.book_flight"):
            flight_id = eval(model_response)
            self.conversation.append({"role": "assistant", "content": model_response})
            text=f"Flight ID {flight_id} was booked." if flight_id else 'No seats available.'
            return BookFlightResponse(text=text, booked_flight=flight_id)
        else:
            self.conversation.append({"role": "assistant", "content": "You're welcome!"})
            return TextResponse(text=model_response)