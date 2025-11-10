from time import time
from dataclasses import dataclass

class Aircraft: # Det som ska skickas till databasen, med eller utan allt
    def __init__(icao: str = None, position: tuple[float, ...] = None, airborne_velocity: tuple[...] = None):

        if not icao:
            raise RuntimeError("No ICAO provided")
        
        self.icao = icao
        self.time_initialized = time()
    
    def 

    @property
    def creation_time():
        return self.time_initialized - time()


@dataclass
class Track: # Aggregerad men inte fullständigt komplett data
    icao: str
    position: tuple 
    airborne_velocity: tuple
    creation_time: float