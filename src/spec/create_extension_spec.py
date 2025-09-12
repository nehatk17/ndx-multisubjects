# -*- coding: utf-8 -*-
from pathlib import Path

from pynwb.spec import NWBAttributeSpec, NWBDatasetSpec, NWBGroupSpec, NWBNamespaceBuilder, NWBRefSpec, export_spec


def main():
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-multisubjects""",
        version="""0.1.1""",
        doc=(
            "Allow for multiple subjects to be represented in a single NWB file. "
            "This is for experiments where subjects are being recorded at the same time in the same session."
        ),
        author=[
            "Neha Thomas",
            "Ryan Ly",
            "Oliver Ruebel",
        ],
        contact=[
            "neha.thomas@jhuapl.edu",
            "rly@lbl.gov",
            "oruebel@lbl.gov",
        ],
    )
    ns_builder.include_namespace("core")

    subjects_table_spec = NWBGroupSpec(
        name="SubjectsTable",
        neurodata_type_def="SubjectsTable",
        neurodata_type_inc="DynamicTable",
        doc="An extension of DynamicTable to create a subjects table with relevant metadata.",
        datasets=[
            NWBDatasetSpec(
                name="age",
                neurodata_type_inc="VectorData",
                dtype="text",
                doc="Age of subject. Can be supplied instead of date_of_birth. Must be in ISO 8601 format, e.g., "
                "P70D for 70 days or if it is a range, must be [lower]/[upper], "
                "e.g., P10W/P12W which means between 10 and 12 weeks.",
                quantity="?",
                attributes=[
                    NWBAttributeSpec(
                        name="reference",
                        doc="Age is with reference to this event. "
                        "Can be birth or gestational. If reference is omitted, birth is implied.",
                        dtype="text",
                        required=False,
                        default_value="birth",
                    )
                ],
            ),
            NWBDatasetSpec(
                name="date_of_birth",
                neurodata_type_inc="VectorData",
                dtype="text",  # TODO: update to datetime
                doc="Date of birth of subject. Can be supplied instead of age.",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="subject_description",
                neurodata_type_inc="VectorData",
                dtype="text",
                doc="Description of subject and where subject came from (e.g., breeder, if animal).",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="genotype",
                neurodata_type_inc="VectorData",
                dtype="text",
                doc="Genetic strain. If absent, assume wild type (WT).",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="sex",
                neurodata_type_inc="VectorData",
                dtype="text",
                doc="Gender of subject. Must be M, F, O (other), or U (unknown).",
            ),
            NWBDatasetSpec(
                name="species",
                neurodata_type_inc="VectorData",
                dtype="text",
                doc="Species of subject. Can be Latin binomial e.g., Mus musculus or NCBI taxonomic identifier.",
            ),
            NWBDatasetSpec(
                name="strain",
                neurodata_type_inc="VectorData",
                dtype="text",
                doc="Strain of subject.",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="subject_id",
                neurodata_type_inc="VectorData",
                dtype="text",
                doc="ID of animal/person used/participating in experiment (lab convention).",
            ),
            NWBDatasetSpec(
                name="weight",
                neurodata_type_inc="VectorData",
                dtype="text",
                doc="Weight at time of experiment, at time of surgery and at other important times.",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="individual_subj_link",
                neurodata_type_inc="VectorData",
                dtype="text",
                doc="Link to individual subject nwb file, if any. Should be relative file paths or URI.",
                quantity="?",
            ),
        ],
    )

    ndx_multisubjects_nwbfile_spec = NWBGroupSpec(
        neurodata_type_def="NdxMultiSubjectsNWBFile",
        neurodata_type_inc="NWBFile",
        doc=(
            "An extension to the NWBFile to store multiple subjects data. "
            "After integration of ndx-multisubjects with the core schema, "
            "the NWBFile schema should be updated to this type."
        ),
        groups=[
            NWBGroupSpec(
                name="general",
                doc="Experimental metadata...",
                groups=[
                    NWBGroupSpec(
                        neurodata_type_inc="SubjectsTable",
                        name="SubjectsTable",
                        doc="Table to hold all metadata of subjects in an experiment.",
                        quantity="?",
                    ),
                ],
            ),
        ],
    )

    select_subjects_container_spec = NWBGroupSpec(
        neurodata_type_def="SelectSubjectsContainer",
        neurodata_type_inc="NWBDataInterface",
        doc="A container to hold data from a selection of subjects from the SubjectsTable.",
        groups=[
            NWBGroupSpec(
                neurodata_type_inc="NWBDataInterface",
                doc="Data objects recorded from the selected subjects",
                quantity="*",
            ),
            NWBGroupSpec(
                neurodata_type_inc="DynamicTable",
                doc="Data tables recorded from the selected subjects",
                quantity="*",
            ),
        ],
        datasets=[
            NWBDatasetSpec(
                name="subjects",
                neurodata_type_inc="DynamicTableRegion",
                doc="A DynamicTableRegion that selects the subjects from the SubjectsTable "
                "that are included in this container.",
                attributes=[
                    NWBAttributeSpec(
                        name="table",
                        dtype=NWBRefSpec("SubjectsTable", reftype="object"),
                        doc="The table that this region selects from.",
                        required=True,
                    )
                ],
            )
        ],
    )

    new_data_types = [
        subjects_table_spec,
        ndx_multisubjects_nwbfile_spec,
        select_subjects_container_spec,
    ]

    # export the spec to yaml files in the root spec folder
    output_dir = str((Path(__file__).parent.parent.parent / "spec").absolute())
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
