# from pynwb import register_map
# from pynwb.io.file import NWBFileMap
# from . import NdxMultiSubjectsNWBFile


# NOTE: When this extension is merged into the core NWB schema and software, this class will be merged
# with the core NWBFileMap class.
# @register_map(NdxMultiSubjectsNWBFile)
# class NdxMultiSubjectsNWBFileMap(NWBFileMap):

#     def __init__(self, spec):
#         super().__init__(spec)

# Map the "subjects_table" attribute on the NdxMultiSubjectsNWBFile class to the SubjectsTable class
# general_spec = self.spec.get_group("general")
# self.unmap(general_spec)
# self.unmap(general_spec.get_group("SubjectsTable"))
# self.map_spec("subjects_table", general_spec.get_group("SubjectsTable"))
