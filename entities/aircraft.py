class Aircraft:
    def __init__(icao: str = None, msg_even: str = None, msg_odd: str = None, 
        even_timestamp: float = None, odd_timestamp: float = None, position: tuple[float, ...] = None):

        if not icao:
            raise RuntimeError("No ICAO provided")
