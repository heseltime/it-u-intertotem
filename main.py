import os
import time
import random
from obspy import UTCDateTime, geodetics
from obspy.clients.fdsn import Client
import numpy as np
from scipy.io.wavfile import write as write_wav
import re
from tqdm import tqdm  # For progress bar support

# Import communication module
from communication.communication import copy_file_to_pi

# List of destination IPs for multiple Raspberry Pis
destination_ips = ["192.168.1.129"]

TARGET_DEVICE_INPUT_DIRECTORY = '/home/totem/Desktop/intertotem/it-u-intertotem/input'  # Directory on the destination Pi where files should be copied

# DIRECTORY to store output WAV files
OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# PARAMETERS OF INTEREST
CATALOG_REQUEST_FREQUENCY_IN_SECONDS = 30  # 1/2 minute
MIN_MAGNITUDE_OF_INTEREST = 4.5
MAX_NUMBER_OF_EARTHQUAKES_RETRIEVED_PER_REQUEST = 10 

# Lists of available networks and stations for random selection
NETWORKS = ['IU', 'US', 'CI', 'GE', 'AK']  # Add or modify according to data of interest
STATIONS = ['ANMO', 'BHZ', 'BRK', 'COLA', 'DUG']  # Add or modify according to data of interest

CATALOG_REQUEST_WINDOW_ENDTIME = UTCDateTime()  # Current time
CATALOG_REQUEST_WINDOW_STARTTIME = CATALOG_REQUEST_WINDOW_ENDTIME - 24 * 3600  # 24 hours before

# AUX. FUNCTIONS
def fetch_earthquake_data(starttime, endtime, min_magnitude):
    client = Client("IRIS")
    try:
        cat = client.get_events(starttime=starttime, endtime=endtime, minmagnitude=min_magnitude)
        return cat
    except Exception as e:
        print(f"Error fetching earthquake data: {e}")
        return None

def fetch_seismogram_data(event, client, network, station, duration=600):
    origin_time = event.origins[0].time
    try:
        inventory = client.get_stations(network=network, station=station, starttime=origin_time, endtime=origin_time + duration, level="response")
        st = client.get_waveforms(network=network, station=station, location="00", channel="BHZ", starttime=origin_time, endtime=origin_time + duration)
        if len(st) == 0:
            raise ValueError("No seismogram data fetched.")
        return st, inventory
    except Exception as e:
        print(f"Error fetching seismogram data for network {network} and station {station}: {e}")
        return None, None

def calculate_distance_to_epicenter(event, inventory):
    # Get earthquake epicenter coordinates
    origin = event.origins[0]
    event_latitude = origin.latitude
    event_longitude = origin.longitude

    # Get station coordinates
    station = inventory[0][0][0]  # Assuming first network, first station
    station_latitude = station.latitude
    station_longitude = station.longitude

    # Calculate the distance using ObsPy's geodetics
    distance_km = geodetics.locations2degrees(event_latitude, event_longitude, station_latitude, station_longitude)
    distance_km = geodetics.degrees2kilometers(distance_km)  # Convert degrees to kilometers
    return distance_km

def seismogram_to_wav(stream, output_path, rate=100):
    # Trim, filter, and normalize the data
    stream.detrend('linear')
    stream.taper(max_percentage=0.05)
    # Adjust high corner frequency below Nyquist limit
    stream.filter("bandpass", freqmin=0.1, freqmax=19.9, corners=4, zerophase=True)
    
    # Extract data and convert to WAV format
    data = np.array(stream[0].data * 32767, dtype=np.int16)  # Scale to 16-bit integer
    write_wav(output_path, rate, data)

# Remove invalid characters
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def main_loop():
    while True:
        # Update time window for each request to get the latest data
        endtime = CATALOG_REQUEST_WINDOW_ENDTIME
        starttime = CATALOG_REQUEST_WINDOW_STARTTIME
        
        # Init client
        client = Client("IRIS")
        catalog = fetch_earthquake_data(starttime, endtime, MIN_MAGNITUDE_OF_INTEREST)
        
        # Check if catalog is valid and not empty
        if not catalog or len(catalog) == 0:
            print("No earthquakes found within the specified criteria.")
            time.sleep(CATALOG_REQUEST_FREQUENCY_IN_SECONDS)
            continue
        
        # Sort catalog by magnitude in descending order
        sorted_catalog = sorted(catalog, key=lambda event: event.magnitudes[0].mag, reverse=True)
        
        # Limit the number of earthquakes processed based on MAX_NUMBER_OF_EARTHQUAKES_RETRIEVED_PER_REQUEST
        limited_catalog = sorted_catalog[:MAX_NUMBER_OF_EARTHQUAKES_RETRIEVED_PER_REQUEST]

        # Initialize the progress bar with the correct total count
        with tqdm(total=len(limited_catalog), desc="Processing earthquakes") as pbar:
            for event in limited_catalog:
                magnitude = event.magnitudes[0].mag
                print(f"Processing earthquake with magnitude: {magnitude}")
                
                # Randomly select a network and station
                network = random.choice(NETWORKS)
                station = random.choice(STATIONS)
                print(f"Selected network: {network}, station: {station}")
                
                # Fetch seismogram data
                try:
                    stream, inventory = fetch_seismogram_data(event, client, network, station)
                    if stream:
                        # Calculate the distance to the epicenter
                        distance_km = calculate_distance_to_epicenter(event, inventory)
                        
                        # Create a sanitized filename based on event time and distance
                        event_time = event.origins[0].time
                        sanitized_filename = sanitize_filename(f"earthquake_{event_time}_{network}_{station}_{int(distance_km)}km.wav")
                        output_path = os.path.join(OUTPUT_DIR, sanitized_filename)
                        
                        # Convert to WAV file
                        seismogram_to_wav(stream, output_path)
                        print(f"WAV file created: {output_path}")

                        # Call the function to copy the file to tmultiple Pis
                        for ip in destination_ips:
                            copy_file_to_pi(output_path, os.path.join(TARGET_DEVICE_INPUT_DIRECTORY, sanitized_filename), ip)
                        
                    else:
                        print(f"No seismogram data available for earthquake with magnitude: {magnitude}.")
                except Exception as e:
                    print(f"Error fetching data for earthquake with magnitude: {magnitude}: {e}")

                # Update the progress bar after each processed earthquake
                pbar.update(1)

        # Wait before the next request
        time.sleep(CATALOG_REQUEST_FREQUENCY_IN_SECONDS)

if __name__ == "__main__":
    main_loop()
