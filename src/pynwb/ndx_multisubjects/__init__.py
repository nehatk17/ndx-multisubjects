from importlib.resources import files
from pynwb import load_namespaces, get_class

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = files(__name__)
__spec_path = __location_of_this_file / "spec" / "ndx-multisubjects.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not __spec_path.exists():
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / "ndx-multisubjects.namespace.yaml"

# Load the namespace
load_namespaces(str(__spec_path))

# TODO: Define your classes here to make them accessible at the package level.
# Either have PyNWB generate a class from the spec using `get_class` as shown
# below or write a custom class and register it using the class decorator
# `@register_class("TetrodeSeries", "ndx-multisubjects")`
SubjectsTable = get_class("SubjectsTable", "ndx-multisubjects")

NdxMultiSubjectsNWBFile = get_class("NdxMultiSubjectsNWBFile", "ndx-multisubjects")

SelectSubjectsContainer = get_class("SelectSubjectsContainer", "ndx-multisubjects")
# TODO: Add all classes to __all__ to make them accessible at the package level
__all__ = [
    "SubjectsTable","NdxMultiSubjectsNWBFile","SelectSubjectsContainer"
]


#from .ndx_multisubjects_nwb_file_io import NdxMultiSubjectsNWBFileMap

# Remove these functions/modules from the package
del load_namespaces, get_class, files, __location_of_this_file, __spec_path
