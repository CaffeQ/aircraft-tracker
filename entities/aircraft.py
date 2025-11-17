from time import time
from dataclasses import dataclass

class Aircraft: # Det som ska skickas till databasen, med eller utan allt
    def __init__(self, icao: str = None, position: tuple[float, ...] = None, velocity: tuple[float] = None, altitude_ft: int = None,
     callsign: str = None):

        if not icao:
            raise RuntimeError("No ICAO provided")

        self.icao = icao

        if velocity:
            speed_kt, angle_degrees, vertical_rate, speed_type = velocity 
            self.speed_kt = speed_kt
            self.angle_degrees = angle_degrees
            self.vertical_rate = vertical_rate
            self.speed_type = speed_type 
        else:
            self.speed_kt = None
            self.angle_degrees = None
            self.vertical_rate = None
            self.speed_type = None 
        if position:
            latitude, longitude = position
            self.latitude = latitude
            self.longitude = longitude
        else:
            self.latitude = None
            self.longitude = None

        self.altitude_ft = altitude_ft
        self.callsign = callsign
        self.time_stamp = time()
        self.latest_update = time()

    def update(self, aircraft: "Aircraft"):
        print("Updating...")
        if aircraft.position:
            self.set_position(aircraft.position)
        if aircraft.velocity:
            self.set_velocity(aircraft.velocity)
        if aircraft.callsign:
            self.callsign = aircraft.callsign
        if aircraft.altitude_ft:
            self.altitude_ft = aircraft.altitude_ft
        self.latest_update = aircraft.latest_update

    def __str__(self):
        return f"ICAO: {self.icao}, POS: {self.position}, VEL: {self.velocity}, Callsign: {self.callsign}, Latest update: {self.latest_update}"

    @property
    def velocity(self):
        return self.speed_kt, self.angle_degrees, self.vertical_rate, self.speed_type
 

    def set_velocity(self, velocity: tuple):
        self.speed_kt, self.angle_degrees, self.vertical_rate, self.speed_type = velocity

    @property
    def position(self):
        return self.latitude, self.longitude

    def set_position(self, position: tuple):
        self.latitude, self.longitude = position

@dataclass
class Track: # Aggregerad men inte fullständigt komplett data
    icao: str
    position: tuple 
    airborne_velocity: tuple



"""
    Returns:
        int, float, int, string, [string], [string]:
            - Speed (kt)
            - Angle (degree), either ground track or heading
            - Vertical rate (ft/min)
            - Speed type ('GS' for ground speed, 'AS' for airspeed)
            - [Optional] Direction source ('TRUE_NORTH' or 'MAGNETIC_NORTH')
            - [Optional] Vertical rate source ('BARO' or 'GNSS')
    """