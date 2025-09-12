from pynwb.io.file import NWBFileMap
from pynwb import register_map

from . import NdxMultiSubjectsNWBFile


# NOTE: When this extension is merged into the core NWB schema and software, this class should be merged
# with the core NWBFileMap class.
@register_map(NdxMultiSubjectsNWBFile)
class NdxMultiSubjectsNWBFileMap(NWBFileMap):

    def __init__(self, spec):
        super().__init__(spec)

        # Map the "subjects_table" attribute on the NdxMultiSubjectsNWBFile class to the SubjectsTable spec
        general_spec = self.spec.get_group("general")
        subjects_table_spec = general_spec.get_group("SubjectsTable")
        self.unmap(subjects_table_spec)
        self.map_spec("subjects_table", subjects_table_spec)
