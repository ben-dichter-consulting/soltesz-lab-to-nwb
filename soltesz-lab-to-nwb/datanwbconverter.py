"""Authors: Cesar Echavarria and Ben Dichter."""

from nwb_conversion_tools import NWBConverter
from nwb_conversion_tools.datainterfaces.ophys.sbx.sbxdatainterface import SbxImagingInterface
from treadmillbehaviordatainterface import TreadmillBehaviorDataInterface


class DataNWBConverter(NWBConverter):
    """Primary conversion class for the Soltesz Lab processing pipeline."""

    data_interface_classes = dict(
        TreadmillData=TreadmillBehaviorDataInterface,
        OptophysData=SbxImagingInterface
        )

    def get_metadata(self):
        metadata = super().get_metadata()
        metadata["NWBFile"].update(
            institution="Stanford",
             lab="Soltesz"
        )
        return metadata
