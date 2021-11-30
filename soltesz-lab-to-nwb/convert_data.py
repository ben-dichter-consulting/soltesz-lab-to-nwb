"""Authors: Cesar Echavarria and Ben Dichter."""
# load necessary modules
from pathlib import Path
import os
from isodate import duration_isoformat
from datetime import timedelta, datetime
from datanwbconverter import DataNWBConverter

from pprint import pprint

# Hard-coded parameters
sampling_rate = 10000  # sampling rate for ephys data

# # Point to the base folder path for data
base_path = Path("/Users/cesar/Documents/CatalystNeuro/Farrell_SuM_2021/SuM_2-Photon/")

# #change these for the file of interest
animal = "JF_141"
suffix = "_006"
animal_path = os.path.join(base_path, animal)

# Name the NWBFile and point to the desired save path
# nwbfile_path = os.path.join(animal_path ,'FullTesting.nwb')
nwbfile_path = os.path.join(animal_path, "FullTesting.nwb")

# Point to the various files for the conversion
speed_file_path = os.path.join(animal_path, "GRIN" + animal[2:] + suffix + ".speed.npy")
opto_file_path = os.path.join(animal_path, 'GRIN' + animal[2:] + suffix+ '.sbx')

# # Enter Session and Subject information here - uncomment any fields you want to include
session_description = "Enter session description here."
session_start = datetime(1970, 1, 1)  # (Year, Month, Day)
subject_info = dict(
    description="Enter optional subject description here",
    # weight="Enter subject weight here",
    # age=duration_isoformat(timedelta(days=0)),  # Enter the age of the subject in days
    # species="Mus musculus",
    # genotype="Enter subject genotype here",
    # sex="Enter subject sex here"
)

# # Input arguments for each data interface
source_data = dict(
    TreadmillData=dict(
        file_path=str(speed_file_path)
    ),
    OptophysData=dict(
        file_path=str(opto_file_path)
    )
)

# # # Initialize  converter
converter = DataNWBConverter(source_data=source_data)

# metadata_schema = converter.get_metadata_schema()
# pprint(metadata_schema, width=300)

# # # Get metadata from source data
# # # For actual data formats, this generally pulls informatin from the header files for each interface
metadata = converter.get_metadata()

# # # User-input metadata
metadata["NWBFile"].update(session_description=session_description)
metadata["NWBFile"].update(session_start_time=str(session_start))
metadata["Subject"] = subject_info
# these should be linked automatically(?) - validation suggests these should be strings..
metadata['Ophys']['ImagingPlane'][0]['device'] = metadata['Ophys']['Device'][0]['name']
metadata['Ophys']['TwoPhotonSeries'][0]['imaging_plane'] = metadata['Ophys']['ImagingPlane'][0]

# conversion_options_schema = converter.get_conversion_options_schema()
# print("Conversion options for each data interface: \n")
# pprint(conversion_options_schema["properties"], width=120)

# # # Conversion options for each interface
conversion_options = dict(
    TreadmillData=dict(
        sampling_rate=sampling_rate
    ),
    OptophysData=dict()
)

# # Run conversion
converter.run_conversion(
    metadata=metadata,
    nwbfile_path=str(nwbfile_path),
    conversion_options=conversion_options,
    save_to_file=True,  # If False, this instead returns the NWBFile object in memory
    overwrite=True,  # If False, this appends an existing file
)
