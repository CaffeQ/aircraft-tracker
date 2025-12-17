import pyModeS as pms
from pathlib import Path
from __init__ import ADS_B, LAT_REF, LON_REF
import subprocess
from subprocess import Popen
import re
import time
import queue
from threading import Thread
from entities.aircraft import Aircraft
from collections import deque
import schedule
import trackHandling
from db import *
import sys

AIRCRAFT_ID = range(1, 5)           # TC 1-4
SURFACE_POSITION = range(5, 9)      # TC 5-8
AIRBORNE_POSITION_BARO = range(9, 19)    # TC 9-18
AIRBORNE_VELOCITY = range(19, 20)   # TC 19
AIRBORNE_POSITION_GNSS = range(10, 23)   # TC 10-22
RESERVED = range(23, 28)            # TC  23-27
AIRCRAFT_STATUS = range(28, 29)     # TC 28
TARGET_STATE_STATUS = range(29, 30) # TC 29
OPERATIONAL_STATUS = range(31, 32)  # TC 31

MAX_TIMEOUT = 1_000_000


db_handler = DBHandler()

ACTIVE = True

def main():
    print("Starting...")
    start()

def start():
    q = queue.Queue()
    track_producer = Popen([Path(ADS_B)], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    track_consumer = Thread(target=consume, args=(q,))
    track_reader = Thread(target=read_db)
    track_consumer.start()
    track_reader.start()

    produce(track_producer, q)

    q.put(None)
    #track_consumer.join()
   # track_reader.join()

def read_db():
    import pdb
    pdb.set_trace()
    start_time = time.time()
    TIMEOUT = 15
    while time.time() - start_time < TIMEOUT:
        tracks = db_handler.get_all_tracks()
        if tracks:
            sys.stdout.write(f"\r{db_handler.get_all_tracks()}")
            sys.stdout.flush()
        time.sleep(0.1) 

def test_read_db():
    sys.stdout.write(f"\r1423DB 54.3 13.2 500 kt")
    sys.stdout.flush() 
    time.sleep(0.1) 


def create_aircraft(msg: str):
    df = pms.df(msg)
    if df != 17:
        return
    if pms.crc(msg) != 0:
        return
    a = _create_aircraft(msg)
    # print(f"Aircraft: {a}")/
    return a

def write_db(track: str):
    try:
        db_handler.write_track(track)
    except RuntimeError:
        print("Track was none, did not write to database")
        pass 

def consume(tracks: queue.Queue, timeout: int = 20):
    aircrafts = {}
    schedule.every(5).seconds.do(lambda: write(aircrafts))
    start_time = time.time()
    track = None

    while time.time() - start_time < MAX_TIMEOUT:
        try:
            track = tracks.get(timeout=timeout)
        except queue.Empty:
            print("Consumer thread timed out")
            break
        if tracks and not tracks.empty():
            if track:
                if aircrafts.__contains__(track.icao):
                    aircrafts[track.icao].update(track)
                else: 
                    aircrafts[track.icao] = track
            schedule.run_pending()

def write(aircrafts: dict):
    for icao, aircraft in aircrafts.items():
        print(f"writing ICAO: {icao}, aircraft: {aircraft}")
        write_db(aircraft)
    aircrafts = {}

def is_complete(track: Aircraft):
    return True

def produce(process: Popen, track_queue: queue.Queue):
    # Producerar delar av entiteter
    for raw_data in fetch_adsb_data(process):
        aircraft = create_aircraft(raw_data)
        if aircraft:
            track_queue.put(aircraft)

def fetch_adsb_data(process: Popen):
    p = process
    while p.poll() is None:
        out = p.stdout.readline().decode("ascii")
        out = re.sub(r'[;*\n\r]', "", out)
        if out: 
            yield out

def _create_aircraft(msg: str) -> Aircraft:
    icao = pms.adsb.icao(msg)
    type_code = pms.adsb.typecode(msg)
    match type_code:
        case tc if tc in AIRCRAFT_ID:
            return Aircraft(icao=icao, callsign=pms.adsb.callsign(msg))
        case tc if tc in SURFACE_POSITION:
            surface_position = pms.adsb.position_with_ref(msg, LAT_REF, LON_REF)
            return Aircraft(icao=icao, position=surface_position)
        case tc if tc in AIRBORNE_POSITION_BARO:
            altitude_ft = pms.adsb.altitude(msg)
            lat, lon = pms.adsb.position_with_ref(msg, LAT_REF, LON_REF)
            return Aircraft(icao=icao, altitude_ft=altitude_ft, position=(lat, lon))
        case tc if tc in AIRBORNE_VELOCITY:
            return trackHandling.get_airborne_velocity(icao, msg)
        case tc if tc in AIRBORNE_POSITION_GNSS:
            airborne_position_gnss = pms.adsb.position_with_ref(msg, LAT_REF, LON_REF)
            return Aircraft(icao=icao, position=airborne_position_gnss)
        case tc if tc in AIRCRAFT_STATUS:
            pass
            #print("HANDLE AIRCRAFT STATUS")
        case tc if tc in TARGET_STATE_STATUS:
            pass
            #print("HANDLE TARGET STATE STATUS")
        case tc if tc in OPERATIONAL_STATUS:
            pass
            #print("HANDLE OPERATIONAL STATUS")
        case _:
            pass
            #print(f"UNKNOWN TYPE CODE: {type_code}")


if __name__ == "__main__":
    main()

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
