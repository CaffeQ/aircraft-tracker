from time import time
from datetime import datetime
from dataclasses import dataclass

class Aircraft: # Det som ska skickas till databasen, med eller utan allt
    def __init__(self, icao: str = None, position: tuple[float, ...] = None, velocity: tuple[float] = None, altitude_ft: int = None,
     callsign: str = None):

        if not icao:
            raise RuntimeError("No ICAO provided")

        self._icao = icao

        self._speed_kt = None
        self._angle_degrees = None
        self._vertical_rate = None
        self._speed_type = None 
        self._latitude = None
        self._longitude = None
        self._altitude_ft = None
        self._callsign = None

        if velocity:
            speed_kt, angle_degrees, vertical_rate, speed_type = velocity 
            self._speed_kt = speed_kt
            self._angle_degrees = angle_degrees
            self._vertical_rate = vertical_rate
            self._speed_type = speed_type 

        if position:
            latitude, longitude = position
            self._latitude = latitude
            self._longitude = longitude

        if altitude_ft:
            self._altitude_ft = altitude_ft

        if callsign:
            self._callsign = callsign

        self._detected = datetime.now()
        self._latest_update = datetime.now()

    def update(self, aircraft: "Aircraft"):
        if aircraft.position:
            self.set_position(aircraft.position)
        if aircraft.velocity:
            self.set_velocity(aircraft.velocity)
        if aircraft.callsign:
            self._callsign = aircraft.callsign
        if aircraft.altitude_ft:
            self._altitude_ft = aircraft.altitude_ft
        self._latest_update = aircraft.latest_update

    def __str__(self):
        return f"ICAO: {self._icao}, POS: {self.position}, VEL: {self.velocity}, Callsign: {self._callsign}, Latest update: {self._latest_update}, Detected: {self._detected}"

    @property
    def json(self):
        pass

    @property
    def icao(self):
        if not self._icao:
            return "Empty"
        return self._icao
    
    @property
    def latitude(self):
        return self._value_or_empty(self._latitude)
    
    @property
    def longitude(self):
        return self._value_or_empty(self._longitude)
    
    @property
    def altitude_ft(self):
        return self._value_or_empty(self._altitude_ft)

    @property
    def speed_kt(self):
        return self._value_or_empty(self._speed_kt)

    @property
    def angle_degrees(self):
        return self._value_or_empty(self._angle_degrees)
    
    @property
    def vertical_rate(self):
        return self._value_or_empty(self._vertical_rate)

    @property
    def speed_type(self):
        return self._value_or_empty(self._speed_type)

    @property
    def latest_update(self):
        return self._value_or_empty(self._latest_update)

    @property
    def callsign(self):
        return self._value_or_empty(self._callsign)

    def _value_or_empty(self, value):
        return "Empty" if value is None else value

   #  f"'{track.icao}', {track.latitude}, {track.longitude}, {track.altitude_ft}, {track.speed_kt}, {track.angle_degrees}, {track.vertical_rate}, '{track.speed_type}', '{track.latest_update}', '{track.callsign}'"

    @property
    def velocity(self):
        return self._speed_kt, self._angle_degrees, self._vertical_rate, self._speed_type
 

    def set_velocity(self, velocity: tuple):
        self._speed_kt, self._angle_degrees, self._vertical_rate, self._speed_type = velocity

    @property
    def position(self):
        return self._latitude, self._longitude, self._altitude_ft

    def set_position(self, position: tuple):
        self._latitude, self._longitude, self._altitude_ft = position

    def set_altitude(self, altitude_ft: int):
        self._altitude_ft = altitude_ft

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