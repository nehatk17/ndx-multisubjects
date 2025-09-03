# ndx-multisubjects Extension for NWB

Allow for multiple subjects to be represented in a single NWB file. This is for experiments where subjects are being
recorded at the same time in the same session.

## Installation


## Usage

First import the neurodata types from this extension and a few core types that we will use in this example:

```python
from ndx_multisubjects import NdxMultiSubjectsNWBFile, SubjectsTable, SelectSubjectsContainer
from pynwb import TimeSeries, NWBHDF5IO
from hdmf.common import DynamicTableRegion
from uuid import uuid4
from datetime import datetime, timezone
import numpy as np
```

Next, create a simple NWB file. We use a custom extension of the core `NWBFile` neurodata type that allows adding a
`SubjectsTable` to hold data and metadata about multiple subjects.

```python
# Create NWB file that accepts multiple subjects
nwbfile = NdxMultiSubjectsNWBFile(
    session_description="test multi subjects",
    identifier=str(uuid4()),
    session_start_time=datetime.now(tz=timezone.utc)
)
```

Next, add the subjects table and populate the subjects' metadata by using `.add_row`. All fields in the core `Subject`
neurodata type are columns in this table. "individual_subj_link" is a new optional column that can be used to link a
subject to a separate NWB file containing data only for that subject.

```python
# Create a SubjectsTable with three subjects
subjects_table = SubjectsTable(
    description="Subjects in this session",
)

# Populate the SubjectsTable with metadata
subjects_table.add_row(
    age="P70D",
    subject_description="Test subject",
    genotype="WT",
    sex="M",
    species="Mus musculus",
    strain="C57BL/6",
    subject_id="subject_001",
    weight="20g",
    individual_subj_link="relfilepath/subj_001.nwb"
)

subjects_table.add_row(
    age="P30D",
    subject_description="Test subject2",
    genotype="WT",
    sex="F",
    species="Mus musculus",
    strain="C57BL/6",
    subject_id="subject_003",
    weight="25g",
    individual_subj_link="relfilepath/subj_003.nwb"
)

subjects_table.add_row(
    age="P42D",
    subject_description="Test subject5",
    genotype="WT",
    sex="F",
    species="Mus musculus",
    strain="C57BL/6",
    subject_id="subject_005",
    weight="25g",
    individual_subj_link="relfilepath/subj_005.nwb"
)
```

Add the `SubjectsTable` object to the NWB file with `nwbfile.add_acquisition(subjects_table)`. This adds the subjects
table to the `acquisition` group of the NWB file. In the future, this will be changed so that the table can be added
into the `general` group of the NWB file.

```python
nwbfile.add_acquisition(subjects_table)
```

To add data that is specific to a selection of the subjects (fewer than the total number of subjects), use a
`SelectSubjectsContainer` as shown below:

```python
# Create a TimeSeries with random data representing the interaction between subject_001 and subject_003
dummyTimeSeries = TimeSeries(
    name="interaction_subjects_001_and_003",
    data=np.random.rand(100),
    unit="mV",
    timestamps=np.arange(100) * 0.1,
)

# Create a DynamicTableRegion for the selected subjects
subjects = DynamicTableRegion(
    name="subjects",
    description="Reference to the first two subjects of the SubjectsTable.",
    table=subjects_table,
    data=[0, 1]  # Select the first two subjects by row index
)

# Create a SelectSubjectsContainer to hold data from the selected subjects and the DynamicTableRegion identifying
# which subjects the data are from
selected_subjects_container = SelectSubjectsContainer(
    name='selected_subjects_container_subjects_001_and_003',
    subjects=subjects,
)
selected_subjects_container.add_nwb_data_interfaces(dummyTimeSeries)

# Create a ProcessingModule to hold the SelectSubjectsContainer
module = nwbfile.create_processing_module(
    name='behavior',
    description='Processing module for behavioral data'
)
module.add(selected_subjects_container)

print(nwbfile)

# Write the NWB file to a file
with NWBHDF5IO('test_multi_subjects.nwb', 'w') as io:
    io.write(nwbfile)
```

To access the data for the selected subjects from the written NWB file:

```python
# Open the NWB file and read it
io = NWBHDF5IO('test_multi_subjects.nwb', 'r')
read_nwbfile = io.read()

# Get the SubjectsTable in this NWB file
read_subjects_table = read_nwbfile.get_acquisition('SubjectsTable')

# Get the SelectedSubjectsContainer
read_selected_subjects_container = read_nwbfile.processing['behavior']['selected_subjects_container_subjects_001_and_003']

# Get the TimeSeries from the SelectedSubjectsContainer by name
read_time_series = read_selected_subjects_container.nwb_data_interfaces["interaction_subjects_001_and_003"]

# Get the subset of the SubjectsTable for this SelectedSubjectsContainer as a pandas DataFrame
print(read_selected_subjects_container.subjects.to_dataframe())

# Close the NWB file
io.close()
```

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
