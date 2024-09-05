# it-u-intertotem

This is the software repo for a system running a non-standard seismograph, welcome!

**Run**: the setup depends on a virtual env called it-u, so to run, in the base it-u-intertotem directory, simply ...

```
source it-u/bin/activate
python main.py
```

**Project Structure**:

```
it-u-intertotem/
│
├── code_templates/ # sample scripts
├── it-u/ # venv scripts
├── main.py # main earthquake logic, calls communication script at the end
├── communication/
│   ├── __init__.py  # (empty file to make this directory a package)
│   └── communication.py  # communication script
└── output/  # directory where WAV files are stored
```

## 🌍 From the [Project Proposal](https://github.com/heseltime/it-u-intertotem/blob/main/project_proposal.pdf)

This project aims to engage how we experience seismic data by creating an experience (artistic) and non-standard seismograph that merges cultural artefact and elements of nature.

In many cultures, totems symbolize a deep connection between the natural world, spiritual beliefs, and community identity. Drawing on this notion, our project seeks to create a bridge between the science of seismology and the cultural and psychological, physiological experiences.

![image](https://github.com/user-attachments/assets/d5fbde86-16aa-4a73-8cec-b953ca6096df)


## 🛠️ Hardware 

The system should run on **raspberry pi** in either a monolithic or a distributed mode, interfacing with **multiple speakers** (mono) or one speaker at a time (distributed). The other hardware are **3D-printed pi and/or speaker casings** implementing the totemic theme, see below (section "Totems").

But first, establishing the communicative mode is the end-goal of project stage 1, as in ...

## 📅 Project Stages

- 1: Get components communicating - DONE ✔️
- 2: Fleshing it out (Prototype) - DONE ✔️
- 3: Wrap, Concept for Larger Scale Product - DONE, ready for installation September 6th, 2024 🏁

## 🪆 Totems

Totems are central to the project, representing the fusion of technology, art, and cultural symbolism. The totems are designed as 3D-printed casings for the Raspberry Pi and speakers, embodying natural and spiritual elements. These casings can take various forms, reflecting the cultural themes and aesthetic principles tied to the seismograph's outputs.

Each totem is intended to resonate with its environment, whether through its design, sound, or placement. The visual and auditory aspects of the totems are meant to create a holistic sensory experience that connects the viewer to the data in a meaningful way.

The totems not only serve as functional hardware components but also as artistic expressions, allowing the project to transcend traditional scientific boundaries and engage audiences on a more personal and emotional level.

## :computer: Algorithm Summary (for Installation September 6th, 2024)

### Import Libraries and Modules
- Imports various Python libraries and modules required for:
  - File handling
  - Time management
  - Seismological data retrieval
  - WAV file processing
  - Progress tracking
- Imports a custom module `communication` for copying files to Raspberry Pi devices.

### Define Parameters
- **Destination IPs**:  
  List of IP addresses for the Raspberry Pi devices where the WAV files will be copied.
  
- **NSLC Parameters**:  
  List of tuples specifying the Network, Station, Location, and Channel (NSLC) parameters to be used for retrieving seismogram data.

- **Directories**:  
  - `TARGET_DEVICE_INPUT_DIRECTORY`: Directory path on the destination Pi devices.  
  - `OUTPUT_DIR`: Local directory to store the output WAV files.

- **Configuration Parameters**:  
  - `CATALOG_REQUEST_FREQUENCY_IN_SECONDS`: Frequency for making earthquake catalog requests (in seconds).  
  - `MIN_MAGNITUDE_OF_INTEREST`: Minimum magnitude of earthquakes to be considered.  
  - `MAX_NUMBER_OF_EARTHQUAKES_RETRIEVED_PER_REQUEST`: Maximum number of earthquakes to retrieve per request.

### Define Auxiliary Functions
1. **`fetch_earthquake_data`**:  
   Fetches earthquake data within a specific time range and magnitude threshold using the ObsPy library.

2. **`fetch_seismogram_data`**:  
   Retrieves seismogram data for a given earthquake event and NSLC parameters.

3. **`calculate_distance_to_epicenter`**:  
   Calculates the distance between the earthquake's epicenter and the selected station using geographic coordinates.

4. **`seismogram_to_wav`**:  
   Converts the seismogram data into a WAV file format with specified speed-up and filtering options.

5. **`sanitize_filename`**:  
   Removes invalid characters from filenames to ensure compatibility across different file systems.

### Main Loop
- **Continuous Loop**:
  1. **Fetch Earthquake Data**:  
     Requests earthquake data for the last two hours.
  
  2. **Filter and Sort Earthquake Data**:  
     Checks if any earthquakes were found and sorts them by magnitude in descending order. Limits the number of processed earthquakes.
  
  3. **Process Earthquake Events**:  
     - Iterates over the limited set of earthquakes.
     - Randomly selects an NSLC parameter set to determine the perspective from which the event will be heard.
     - Retrieves the corresponding seismogram data.
     - Computes the distance to the epicenter.
     - Converts the seismogram data into a WAV file.
     - Copies the WAV file to the target Raspberry Pi devices.
  
  4. **Repeat**:  
     Waits for a specified interval before fetching new earthquake data.

### Execution
- The `main_loop()` function is called to start the continuous data retrieval and processing loop when the script is executed.

