# ndx-multisubjects Extension for NWB

Allow for multiple subjects to be represented in a single nwb file. This is for experiments where subjects are being recorded at the same time in the same session.

## Installation


## Usage

First create an NWB file:

```python
# CREATE NWB FILE
nwbfile = NdxMultiSubjectsNWBFile(
    session_description = "test multi subjects",
    identifier = str(uuid4()), 
    session_start_time = datetime.now(tz=timezone.utc))
```


Next, add the subjects table and populate the subjects' metadata by using `.add_row`
```python
# ADD SUBJECTS TABLE

    subjects_table = SubjectsTable(
        
        description="description",
        
    )

subjects_table.add_row(
    age="P70D",

    subject_description="Test subject",
    genotype="WT",
    sex = "M",
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
    sex = "F",
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
    sex = "F",
    species="Mus musculus",
    strain="C57BL/6",
    subject_id="subject_005",
    weight="25g",
    individual_subj_link="relfilepath/subj_005.nwb"
)
```
Add the subjects table to the NWB file with  `nwbfile.add_acquisition(subjects_table)`
In the future,  this should be fixed so that the table can be added into the general section of the NWB file.

To add data that is specific to a selection of the subjects (less than the total number of subjects), use a SelectsSubjectsContainer as shown below:

```python
    # ADD SELECTSUBJECTSCONTAINER

    
    subjects = DynamicTableRegion(
        name="subjects",
        description="A DynamicTableRegion that selects the subjects from the SubjectsTable that are included in this container.",
        table=subjects_table,
        data=[0, 1]  # Select both subjects
    )

    dummyTimeSeries = TimeSeries(
        name="dummy_time_series",
        data=np.random.rand(100),  
        unit="mV",
        timestamps=np.arange(100) * 0.1,
    )
    subjects_container = SelectSubjectsContainer(
        subjects = subjects,
        name = 'Interaction Subjects'

        
        
    )

    subjects_container.add_nwb_data_interfaces(dummyTimeSeries)

    module = nwbfile.create_processing_module(
        name='Behavior',
        description='Processing module for subjects data'
    )

    module.add(subjects_container)

    nwbfile


```

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
