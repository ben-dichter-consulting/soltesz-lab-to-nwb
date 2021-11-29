"""Authors: Cesar Echavarria and Ben Dichter."""
from pynwb import NWBFile, TimeSeries
from nwb_conversion_tools.basedatainterface import BaseDataInterface
from nwb_conversion_tools.utils.json_schema import get_base_schema, get_schema_from_hdmf_class
from hdmf.backends.hdf5.h5_utils import H5DataIO
from utils import check_module
import numpy as np

class TreadmillBehaviorDataInterface(BaseDataInterface):
    """Conversion class for running speed behavioral data."""

    @classmethod
    def get_source_schema(cls):
        """Compile input schemas from each of the data interface classes."""
        return dict(
            required=['file_path'],
            properties=dict(
                file_path=dict(type='string')
            )
        )

    # def get_metadata_schema(self):
    #     """Compile metadata schemas from each of the data interface objects."""
    #     metadata_schema = super().get_metadata_schema()
    #     #metadata_schema = get_base_schema()
    #     metadata_schema['properties']['TimeSeries'] = get_schema_from_hdmf_class(TimeSeries)
    #     metadata_schema['required'].append('TimeSeries')
    #     return metadata_schema

    def run_conversion(self, nwbfile: NWBFile, metadata: dict):
        in_file= self.source_data['file_path']
        fs = 10000# hard-code here, for now. TODO: set as property to pass in
        sampling_period = 1.0/fs
        velocity = [i for i in np.load(in_file)] #treadmill velocity
        timestamps = np.arange(len(velocity))/fs
        time = TimeSeries(name='Time',
                              data=H5DataIO(timestamps, compression="gzip"),
                              unit='s',
                              resolution=sampling_period,
                              timestamps=H5DataIO(timestamps, compression="gzip"))
        velocity_ts = TimeSeries(name='Velocity',
                                data=H5DataIO(velocity, compression="gzip"),
                                unit='cm/s',
                                resolution=np.nan,
                                timestamps=H5DataIO(timestamps, compression="gzip")
        )
        behavioral_processing_module = check_module(nwbfile, 'behavior',
                                                            'contains processed behavioral data')
        behavioral_processing_module.add_data_interface(velocity_ts)
        behavioral_processing_module.add_data_interface(time)
    