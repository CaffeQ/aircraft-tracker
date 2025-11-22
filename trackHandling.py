import pyModeS as pms
from typing import Union
from entities.aircraft import Aircraft


def get_airborne_velocity(icao, msg) -> Union[Aircraft, None]:
    try:
        speed_kt, angle_degrees, vertical_rate, speed_type = pms.adsb.airborne_velocity(msg)
        return Aircraft(icao=icao, velocity=(speed_kt, angle_degrees, vertical_rate, speed_type))
    except TypeError as e:
        print(f"Could unpack correctly, cause {e}")
        return None