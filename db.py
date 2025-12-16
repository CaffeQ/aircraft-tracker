import sqlite3
from entities.aircraft import Aircraft


# class Aircraft: # Det som ska skickas till databasen, med eller utan allt
#     def __init__(self, icao: str = None, position: tuple[float, ...] = None, velocity: tuple[float] = None, altitude_ft: int = None,
#      callsign: str = None):

class DBHandler:


    TRACK_TABLE = """CREATE TABLE track(icao, latitude, longitude, altitude_ft, speed_kt, angle_degrees, vertical_rate, speed_type, latest_update, callsign)"""

    def __init__(self):
        self.con = sqlite3.connect("tracks.db")
        self.cursor = self.con.cursor()
        try:
            self.cursor = self.cursor.execute(self.TRACK_TABLE)
        except sqlite3.OperationalError:
            pass


        


    def write_track(self, track: Aircraft):
        print("Writing track")

        insert = f"'{track.icao}', {track.latitude}, {track.longitude}, {track.altitude_ft}, {track.speed_kt}, {track.angle_degrees}, {track.vertical_rate}, '{track.speed_type}', '{track.latest_update}', '{track.callsign}'"
        exe = f"INSERT INTO track VALUES ({insert})"
        self.cursor.execute(exe)


    def test_get_track(self):
        return self.cursor.execute("SELECT * FROM track").fetchone()

    def get_track_by_id(self, icao: str):
        return self.cursor.execute(f"SELECT * FROM track where icao = '{icao}'").fetchall()

    def get_all_tracks(self):
        return self.cursor.execute(f"SELECT * FROM track").fetchall()



def main():
    import pdb
    pdb.set_trace()
    db_handler = DBHandler()
    aircraft = Aircraft(
        icao="4CA123",
        position=(59.3293, 18.0686),   # lat, lon (Stockholm)
        velocity=(450.0, 30.1, 4.5, "GC"),             # t.ex. 450 knop
        altitude_ft=35000,             # 35 000 fot
        callsign="SAS123"
    )
    db_handler.write_track(aircraft)
    print(db_handler.test_get_track())
    print(db_handler.get_track_by_id(aircraft.icao))




if __name__ == "__main__":
    main()

