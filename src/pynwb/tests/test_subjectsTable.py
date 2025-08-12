"""Unit and integration tests for the example TetrodeSeries extension neurodata type.

TODO: Modify these tests to test your extension neurodata type.
"""

import numpy as np

from pynwb import NWBHDF5IO, NWBFile, TimeSeries
from pynwb.testing import TestCase, remove_test_file, NWBH5IOFlexMixin
from hdmf.common import DynamicTableRegion

from ndx_multisubjects import SubjectsTable, NdxMultiSubjectsNWBFile, SelectSubjectsContainer

from uuid import uuid4 
from datetime import datetime, timezone



class test_SubjectsTableConstructor(TestCase):
    """Simple unit test for creating a TetrodeSeries."""



    def test_constructor(self):
  

    
        subjects_table = SubjectsTable(
            
            description="description",
           
        )

        self.assertEqual(subjects_table.name, "SubjectsTable")
        self.assertEqual(subjects_table.description, "description")
       
    def test_addRow(self):
        """Test adding a row to the SubjectsTable."""
        subjects_table = SubjectsTable(
            description="description",
        )

        subjects_table.add_row(
            age="P70D",
            date_of_birth="2023-01-01T00:00:00",
            subject_description="Test subject",
            genotype="WT",
            sex = "M",
            species="Mus musculus",
            strain="C57BL/6",
            subject_id="subject_001",
            weight="20g",
            individual_subj_link=""
        )

        subjects_table.add_row(
            age="P30D",
            date_of_birth="2023-01-01T00:00:00",
            subject_description="Test subject2",
            genotype="WT",
            sex = "F",
            species="Mus musculus",
            strain="C57BL/6",
            subject_id="subject_003",
            weight="25g",
            individual_subj_link="relfilepath/subj_003.nwb"
        )

        self.assertEqual(len(subjects_table), 2)
        self.assertEqual(subjects_table['age'][0], "P70D")
        self.assertEqual(subjects_table['date_of_birth'][0], "2023-01-01T00:00:00")
        self.assertEqual(subjects_table['subject_description'][0], "Test subject")
        self.assertEqual(subjects_table['genotype'][0], "WT")
        self.assertEqual(subjects_table['sex'][0], "M")
        self.assertEqual(subjects_table['species'][0], "Mus musculus")
        self.assertEqual(subjects_table['strain'][0], "C57BL/6")
        self.assertEqual(subjects_table['subject_id'][0], "subject_001")
        self.assertEqual(subjects_table['weight'][0], "20g")
        self.assertEqual(subjects_table['individual_subj_link'][0], "")
        self.assertEqual(subjects_table['age'][1], "P30D")
        self.assertEqual(subjects_table['date_of_birth'][1], "2023-01-01T00:00:00")
        self.assertEqual(subjects_table['subject_description'][1], "Test subject2")
        self.assertEqual(subjects_table['genotype'][1], "WT")
        self.assertEqual(subjects_table['sex'][1], "F")
        self.assertEqual(subjects_table['species'][1], "Mus musculus")
        self.assertEqual(subjects_table['strain'][1], "C57BL/6")
        self.assertEqual(subjects_table['subject_id'][1], "subject_003")
        self.assertEqual(subjects_table['weight'][1], "25g")


class TestSubjectsTableSimpleRoundtrip(TestCase):
    """Simple roundtrip test for TetrodeSeries."""

    def setUp(self):
        self.nwbfile = NdxMultiSubjectsNWBFile(session_description = "test multi subjects",identifier = str(uuid4()), 
                                               session_start_time = datetime.now(tz=timezone.utc))
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Add a TetrodeSeries to an NWBFile, write it to file, read the file, and test that the TetrodeSeries from the
        file matches the original TetrodeSeries.
        """
        subjects_table = SubjectsTable(
            
            description="description",
           
        )

        # dateTime = datetime.now(tz=timezone.utc)

        subjects_table.add_row(
            age="P70D",
            date_of_birth="2023-01-01T00:00:00",
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
            date_of_birth="2023-01-01T00:00:00",
            subject_description="Test subject2",
            genotype="WT",
            sex = "F",
            species="Mus musculus",
            strain="C57BL/6",
            subject_id="subject_003",
            weight="25g",
            individual_subj_link="relfilepath/subj_003.nwb"
        )
        self.nwbfile.add_acquisition(subjects_table)

        # subjects_table.parent = self.nwbfile

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            print(read_nwbfile)
            self.assertContainerEqual(subjects_table, read_nwbfile.acquisition['SubjectsTable'])
            # self.assertEqual(len(subjects_table), read_nwbfile.acquisition['SubjectsTable'])
            # self.assertEqual(subjects_table['age'][0], "P70D")
            # self.assertEqual(subjects_table['date_of_birth'][0], dateTime)
            # self.assertEqual(subjects_table['subject_description'][0], "Test subject")
            # self.assertEqual(subjects_table['genotype'][0], "WT")
            # self.assertEqual(subjects_table['sex'][0], "M")
            # self.assertEqual(subjects_table['species'][0], "Mus musculus")
            # self.assertEqual(subjects_table['strain'][0], "C57BL/6")
            # self.assertEqual(subjects_table['subject_id'][0], "subject_001")
            # self.assertEqual(subjects_table['weight'][0], "20g")
            # self.assertEqual(subjects_table['age'][1], "P30D")
            # self.assertEqual(subjects_table['date_of_birth'][1], dateTime)
            # self.assertEqual(subjects_table['subject_description'][1], "Test subject2")
            # self.assertEqual(subjects_table['genotype'][1], "WT")
            # self.assertEqual(subjects_table['sex'][1], "F")
            # self.assertEqual(subjects_table['species'][1], "Mus musculus")
            # self.assertEqual(subjects_table['strain'][1], "C57BL/6")
            # self.assertEqual(subjects_table['subject_id'][1], "subject_003")
            # self.assertEqual(subjects_table['weight'][1], "25g")


class TestSelectSubjectsContainer(TestCase):
    """Test SelectSubjectsContainer functionality."""

    def test_constructor(self):
  
        subjects_table = SubjectsTable(
            description="description",
        )

        subjects_table.add_row(
            age="P70D",
            date_of_birth="2023-01-01T00:00:00",
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
            date_of_birth="2023-01-01T00:00:00",
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
            date_of_birth="2023-01-01T00:00:00",
            subject_description="Test subject2",
            genotype="WT",
            sex = "F",
            species="Mus musculus",
            strain="C57BL/6",
            subject_id="subject_005",
            weight="25g",
            individual_subj_link="relfilepath/subj_005.nwb"
        )
    
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
        self.assertEqual(subjects_container.name, "Interaction Subjects")
        self.assertIs(subjects_container.subjects, subjects)


class TestSelectSubjectsContainerSimpleRoundtrip(TestCase):
    """Simple roundtrip test for TetrodeSeries."""

    def setUp(self):
        self.nwbfile = NdxMultiSubjectsNWBFile(session_description = "test multi subjects",identifier = str(uuid4()), 
                                               session_start_time = datetime.now(tz=timezone.utc))
        self.path = "test.nwb"

    # def tearDown(self):
    #     remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Add a TetrodeSeries to an NWBFile, write it to file, read the file, and test that the TetrodeSeries from the
        file matches the original TetrodeSeries.
        """
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

        self.nwbfile.add_acquisition(subjects_table)

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

        module = self.nwbfile.create_processing_module(
            name='Behavior',
            description='Processing module for subjects data'
        )

        module.add(subjects_container)


        # subjects_table.parent = self.nwbfile

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            print(read_nwbfile)
            self.assertContainerEqual(subjects_container, read_nwbfile.processing['Behavior']['Interaction Subjects'])