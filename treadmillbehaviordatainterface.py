"""Authors: Cesar Echavarria."""
from pynwb import NWBFile, TimeSeries
from nwb_conversion_tools.basedatainterface import BaseDataInterface
from nwb_conversion_tools.utils.json_schema import (
    get_base_schema,
    get_schema_from_hdmf_class,
)
from nwb_conversion_tools.utils.common_writer_tools import check_module
from hdmf.backends.hdf5.h5_utils import H5DataIO

import numpy as np


class TreadmillBehaviorDataInterface(BaseDataInterface):
    """Conversion class for running speed behavioral data."""

    @classmethod
    def get_source_schema(cls):
        """Compile input schemas from each of the data interface classes."""
        return dict(
            required=["file_path"], properties=dict(file_path=dict(type="string"))
        )

    def run_conversion(
        self,
        nwbfile: NWBFile,
        metadata: dict,
        sampling_rate: float,
    ):
        in_file = self.source_data["file_path"]
        sampling_period = 1.0 / sampling_rate
        velocity = np.load(in_file)  # treadmill velocity
        velocity_ts = TimeSeries(
            name="Velocity",
            data=H5DataIO(velocity, compression="gzip"),
            unit="cm/s",
            resolution=np.nan,
            rate=float(sampling_rate),
            starting_time=float(0),
        )
        behavioral_processing_module = check_module(
            nwbfile, "behavior", "contains processed behavioral data"
        )
        behavioral_processing_module.add_data_interface(velocity_ts)
