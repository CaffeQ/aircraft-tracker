import pyModeS as pms
from pathlib import Path
from __init__ import ADS_B, LAT_REF, LON_REF
import subprocess
from subprocess import Popen
import re
import time
from queue import Queue
from threading import Thread
from entities.aircraft import Aircraft
from collections import deque

AIRCRAFT_ID = range(1, 5)           # TC 1-4
SURFACE_POSITION = range(5, 9)      # TC 5-8
AIRBORNE_POSITION_BARO = range(9, 19)    # TC 9-18
AIRBORNE_VELOCITY = range(19, 20)   # TC 19
AIRBORNE_POSITION_GNSS = range(10, 23)   # TC 10-22
RESERVED = range(23, 28)            # TC  23-27
AIRCRAFT_STATUS = range(28, 29)     # TC 28
TARGET_STATE_STATUS = range(29, 30) # TC 29
OPERATIONAL_STATUS = range(31, 32)  # TC 31

def main():
    print("Starting...")
    start()

def start():
    import pdb
    pdb.set_trace()
    q = Queue()
    p = Popen([Path(ADS_B)], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    #adsb_gen = fetch_adsb_data(p)
    #producer = Thread(target=produce, args=(p, q,))
    consumer = Thread(target=consume, args=(q,))
    #producer.start()
    aircraft = Aircraft()
    produce(p, q)
    consumer.start()
    #sanitized_data = sanitize_data(d)
    #Thread(target=send, args=(sanitized_data,), daemon=True).start()
    #producer.join()
    consumer.join()

def create_aircraft(msg: str):
    print("Sanitizing: ", msg)
    df = pms.df(msg)
    if df != 17:
        print("Not ADSB")
        return
    if pms.crc(msg) != 0:
        return

    icao = pms.adsb.icao(msg)
    tc = pms.adsb.typecode(msg)

    payload = filter_by_type_code(msg, tc)
    return payload # Should be filtered information, probably full aircraft
    return Aircraft(icao=icao)

def write_db(track: str):
    print(f"sending track={track}....")

def consume(tracks: Queue):
    incomplete_tracks = deque()
    for track in tracks.get():
        if is_complete(track): # track.is_complete()
            write_db(Aircraft(track))
            incomplete_tracks.remove(track)
        else:
            incomplete_tracks.append(track)

def is_complete(track: Aircraft):
    return True

def produce(process: Popen, queue: Queue):
    # Producerar delar av entiteter
    for raw_data in fetch_adsb_data(process):
        msg = create_aircraft(raw_data)
        queue.put(msg)

def fetch_adsb_data(process: Popen):
    p = process
    while p.poll() is None:
        out = p.stdout.readline().decode("ascii")
        
        out = re.sub(r'[;*\n\r]', "", out)
        if out:
            yield out

def filter_by_type_code(msg: str, type_code: str) -> tuple[...]:
    tc = type_code
    match type_code:
        case tc if tc in AIRCRAFT_ID:
            return pms.adsb.callsign(msg)
            print("HANDLE AIRCRAFT ID")
        case tc if tc in SURFACE_POSITION:
            print("HANDLE SURFACE POSITION")
            return pms.adsb.position_with_ref(msg, LAT_REF, LON_REF)
        case tc if tc in AIRBORNE_POSITION_BARO:
            return pms.adsb.position_with_ref(msg, LAT_REF, LON_REF)
        case tc if tc in AIRBORNE_VELOCITY:
            airborne_velocity = pms.adsb.airborne_velocity(msg)
            print(f"Airborne velocity: {airborne_velocity}")
            return airborne_velocity
        case tc if tc in AIRBORNE_POSITION_GNSS:
            print("HANDLE AIRBORNE POSITION")
        case tc if tc in AIRCRAFT_STATUS:
            print("HANDLE AIRCRAFT STATUS")
        case tc if tc in TARGET_STATE_STATUS:
            print("HANDLE TARGET STATE STATUS")
        case tc if tc in OPERATIONAL_STATUS:
            print("HANDLE OPERATIONAL STATUS")
        case _:
            print(f"UNKNOWN TYPE CODE: {type_code}")


if __name__ == "__main__":
    main()
