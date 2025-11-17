from time import time
from dataclasses import dataclass

class Aircraft: # Det som ska skickas till databasen, med eller utan allt
    def __init__(self, icao: str = None, position: tuple[float, ...] = None, velocity: tuple[...] = None, callsign: str = None):

        if not icao:
            raise RuntimeError("No ICAO provided")
        
        self.icao = icao
        self.position = position
        self.velocity = velocity 
        self.callsign = callsign
        self.time_stamp = time()
        self.latest_update = time()

    def update(self, aircraft: "Aircraft"):
        print("Updating...")
        if aircraft.position:
            self.position = aircraft.position
        if aircraft.velocity:
            self.velocity = aircraft.velocity
        if aircraft.callsign:
            self.callsign = aircraft.callsign
        self.latest_update = aircraft.latest_update

    def __str__(self):
        return f"ICAO: {self.icao}, POS: {self.position}, VEL: {self.velocity}, Callsign: {self.callsign}, Latest update: {self.latest_update}"


@dataclass
class Track: # Aggregerad men inte fullständigt komplett data
    icao: str
    position: tuple 
    airborne_velocity: tuple
