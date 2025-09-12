from hdmf.utils import docval, get_docval
from pynwb import NWBFile, get_class, register_class

SubjectsTable = get_class("SubjectsTable", "ndx-multisubjects")
SelectSubjectsContainer = get_class("SelectSubjectsContainer", "ndx-multisubjects")

AutoNdxMultiSubjectsNWBFile = get_class("NdxMultiSubjectsNWBFile", "ndx-multisubjects")


@register_class("NdxMultiSubjectsNWBFile", "ndx-multisubjects")
class NdxMultiSubjectsNWBFile(AutoNdxMultiSubjectsNWBFile):
    """An extension to the NWBFile to store multiple subjects data."""

    # NOTE: After integration of ndx-multisubjects with the core schema, the NWBFile schema should be updated to this
    # type.

    __nwbfields__ = ({"name": "subjects_table", "child": True},)

    @docval(
        *get_docval(NWBFile.__init__),
        {"name": "subjects_table", "type": SubjectsTable, "doc": "A SubjectsTable storing subjects", "default": None},
    )
    def __init__(self, **kwargs):
        subjects_table = kwargs.pop("subjects_table", None)
        super().__init__(**kwargs)
        self.subjects_table = subjects_table
