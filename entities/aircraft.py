from time import time
from dataclasses import dataclass

class Aircraft: # Det som ska skickas till databasen, med eller utan allt
    def __init__(self, icao: str = None, position: tuple[float, ...] = None, velocity: tuple[...] = None, callsign: str = None):

        if not icao:
            raise RuntimeError("No ICAO provided")
        
        self.icao = icao
        self.position = position
        self.velocity = velocity 
        self.time_stamp = time()

    def update(self, aircraft: "Aircraft"):
        if aircraft.position:
            self.position = aircraft.position
        if aircraft.velocity:
            self.velocity = aircraft.velocity
        if aircraft.callsign:
            self.callsign = aircraft.callsign

@dataclass
class Track: # Aggregerad men inte fullständigt komplett data
    icao: str
    position: tuple 
    airborne_velocity: tuple
