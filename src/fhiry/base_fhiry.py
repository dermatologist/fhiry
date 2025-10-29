"""
Copyright (c) 2020 Bell Eapen

This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""

import json
import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


class BaseFhiry(object):
    """Base class providing common dataframe processing utilities for FHIR.

    This class encapsulates common logic for transforming FHIR bundle data into
    a pandas DataFrame, including column cleanup, code extraction, and patient
    ID derivation.

    Args:
        config_json: Either a JSON string or a path to a JSON file specifying
            transformations with keys:
            - "REMOVE": list[str] of column prefixes to remove
            - "RENAME": dict[str, str] mapping old->new column names
            If None, a sensible default is used.
    """

    def __init__(self, config_json=None):
        self._df = None

        # Codes from the FHIR datatype "coding"
        # (f.e. element resource.code.coding or element resource.clinicalStatus.coding)
        # are extracted to a col "codingcodes"
        # (f.e. col resource.code.codingcodes or col resource.clinicalStatus.codingcodes)
        # without other for analysis often not needed metadata like f.e. codesystem URI
        # or FHIR extensions for coding entries.
        # The full / raw object in col "coding" is deleted after this extraction.
        # If you want to analyze more than the content of code and display from codings
        # (like f.e. different codesystem URIs or further codes in extensions
        # in the raw data/object), you can disable deletion of the raw source object "coding"
        # (f.e. col "resource.code.coding") by setting property delete_col_raw_coding to False
        self._delete_col_raw_coding = True
        if config_json is not None:
            try:
                with open(config_json, "r") as f:  # config_json is a file path
                    self.config = json.load(f)
            except:
                self.config = json.loads(config_json)  # config_json is a json string
        else:
            self.config = json.loads(
                '{ "REMOVE": ["resource.text.div"], "RENAME": { "resource.id": "id" } }'
            )

    @property
    def df(self):
        """pd.DataFrame | None: The current working dataframe, if any."""
        return self._df

    @property
    def delete_col_raw_coding(self):
        """bool: Whether to drop raw coding/display columns after extraction."""
        return self._delete_col_raw_coding

    @delete_col_raw_coding.setter
    def delete_col_raw_coding(self, delete_col_raw_coding):
        """Set whether to drop raw coding/display columns after extraction.

        Args:
            delete_col_raw_coding (bool): True to delete raw columns after creating
                derived columns, False to keep them.
        """
        self._delete_col_raw_coding = delete_col_raw_coding

    def read_bundle_from_bundle_dict(self, bundle_dict):
        """Normalize a FHIR Bundle dict to a dataframe of entries.

        Args:
            bundle_dict (dict): A FHIR Bundle object with an "entry" list.

        Returns:
            pd.DataFrame: Dataframe where each row corresponds to a Bundle entry.
        """
        return pd.json_normalize(bundle_dict["entry"])

    def delete_unwanted_cols(self):
        """Delete unwanted columns from the dataframe.

        Uses the "REMOVE" list from the configuration. Any column that equals a
        listed value or starts with that value followed by a dot will be removed.
        Safely no-ops if the dataframe or configuration is missing.
        """
        if self._df is None:
            logger.warning("Dataframe is empty, nothing to delete")
            return
        if "REMOVE" not in self.config:
            logger.warning("No columns to remove defined in config")
            return
        if not isinstance(self.config["REMOVE"], list):
            logger.warning(
                "REMOVE in config is not a list, expected a list of column names to remove"
            )
            return
        if len(self.config["REMOVE"]) == 0:
            logger.warning("No columns to remove defined in config")
            return
        
        # Collect all columns to remove first, then drop once for better performance
        cols_to_remove = []
        for col in self.config["REMOVE"]:
            cols_to_remove.extend([
                c for c in self._df.columns if c == col or c.startswith(f"{col}.")
            ])
        
        # Single drop operation for better performance
        if cols_to_remove:
            self._df.drop(columns=cols_to_remove, inplace=True)

    def rename_cols(self):
        """Rename dataframe columns according to the configuration.

        Uses the "RENAME" mapping from the configuration. Safely no-ops if the
        dataframe is empty.
        """
        if self._df is not None:
            self._df.rename(columns=self.config["RENAME"], inplace=True)
        else:
            logger.warning("Dataframe is empty, nothing to rename")

    def remove_string_from_columns(self, string_to_remove="resource."):
        """Remove a literal substring from all column names.

        Args:
            string_to_remove: Substring to remove from column names.

        Returns:
            pd.DataFrame | None: The updated dataframe or None if unset.
        """
        if self._df is not None:
            self._df.columns = self._df.columns.str.replace(
                string_to_remove, "", regex=False
            )
        else:
            logger.warning("Dataframe is empty, cannot remove string from columns")
        return self._df

    def process_df(self):
        """Run the standard transformation pipeline on the dataframe.

        Steps include:
        - Extracting codes from coding/display objects to flat columns
        - Adding a patientId column
        - Removing common prefix from column names
        - Converting empty lists to NaN
        - Dropping empty columns
        - Deleting unwanted columns
        - Renaming columns per config

        Returns:
            pd.DataFrame | None: The processed dataframe, or None if unset.
        """
        self.convert_object_to_list()
        self.add_patient_id()
        self.remove_string_from_columns(string_to_remove="resource.")
        self.empty_list_to_nan()
        self.drop_empty_cols()
        self.delete_unwanted_cols()
        self.rename_cols()
        return self._df

    def empty_list_to_nan(self):
        """Convert empty list values in object columns to NaN."""
        if self._df is None:
            logger.warning("Dataframe is empty, nothing to convert")
            return
        for col in self._df.columns:
            if self._df[col].dtype == "object":
                # Use vectorized operation with where() for better performance
                is_empty_list = self._df[col].apply(lambda x: isinstance(x, list) and len(x) == 0)
                self._df[col] = self._df[col].where(~is_empty_list, float("nan"))

    def drop_empty_cols(self):
        """Drop columns that are completely empty (all NaN values)."""
        if self._df is None:
            logger.warning("Dataframe is empty, nothing to drop")
            return
        self._df.dropna(axis=1, how="all", inplace=True)
        if self._df is not None and self._df.empty:
            logger.warning("Dataframe is empty after dropping empty columns")
        return self._df

    def process_bundle_dict(self, bundle_dict):
        """Load and process a FHIR Bundle dictionary.

        Args:
            bundle_dict (dict): A FHIR Bundle object.

        Returns:
            pd.DataFrame | None: The processed dataframe, or None if empty.
        """
        self._df = self.read_bundle_from_bundle_dict(bundle_dict)
        if self._df is None or self._df.empty:
            logger.warning("Dataframe is empty, nothing to process")
            return None
        self._df = self.process_df()
        return self._df

    def convert_object_to_list(self):
        """Extract codes/display from nested objects into flat list columns.

        For columns containing "coding" or "display" in their names, extract a
        list of codes or display texts into new columns with ".codes" or
        ".display" suffixes. Optionally drops raw source columns.
        """
        if self._df is None:
            logger.warning("Dataframe is empty, nothing to convert")
            return

        def _codes_comma_series(src_col: str) -> pd.Series:
            """Return a Series with comma-separated strings from list-like values.

            Args:
                src_col: Column name to extract and stringify.

            Returns:
                pd.Series: Comma-separated strings (or empty string when None).
            """
            codes = self._df[src_col].apply(self.process_list)
            return codes.apply(
                lambda x: (
                    ", ".join(x)
                    if isinstance(x, list) and x is not None
                    else (x if x is not None else "")
                )
            )

        # Collect all new columns first, then concat once for better performance
        new_columns = {}
        cols_to_drop = []
        
        for col in self._df.columns:
            if "coding" in col:
                codes_as_comma_separated = _codes_comma_series(col)
                new_columns[col + ".codes"] = codes_as_comma_separated
                if self._delete_col_raw_coding:
                    cols_to_drop.append(col)
            if "display" in col:
                codes_as_comma_separated = _codes_comma_series(col)
                new_columns[col + ".display"] = codes_as_comma_separated
                cols_to_drop.append(col)
        
        # Single concat operation for all new columns
        if new_columns:
            self._df = pd.concat([self._df, pd.DataFrame(new_columns)], axis=1)
        
        # Drop columns after concat
        if cols_to_drop:
            self._df.drop(columns=cols_to_drop, inplace=True)

    def add_patient_id(self):
        """Add a patientId column inferred from resource fields.

        If the resource type is Patient, uses the resource id; otherwise attempts
        to derive the patient identifier from known subject/patient reference fields.
        """
        if self._df is None:
            logger.warning("Dataframe is empty, cannot add patientId")
            return
        try:
            # Use vectorized operations for better performance
            # Check if resource type is Patient
            is_patient = self._df["resource.resourceType"] == "Patient"
            
            # For Patient resources, use resource.id
            patient_ids = self._df["resource.id"].where(is_patient, "")
            
            # For non-Patient resources, check subject/patient references
            # Try each possible reference field in order
            ref_keys = [
                "resource.subject.reference",
                "resource.patient.reference",
            ]
            
            for key in ref_keys:
                if key in self._df.columns:
                    # Get reference values where not already set
                    ref_values = self._df[key].fillna("")
                    # Clean the reference (remove Patient/ and urn:uuid: prefixes)
                    cleaned_refs = ref_values.str.replace("Patient/", "", regex=False).str.replace("urn:uuid:", "", regex=False)
                    # Update patient_ids where empty and reference exists
                    mask = (patient_ids == "") & (cleaned_refs != "")
                    patient_ids = patient_ids.where(~mask, cleaned_refs)
            
            self._df["patientId"] = patient_ids
            
        except:
            try:
                # Fallback for resources without "resource." prefix
                is_patient = self._df["resourceType"] == "Patient"
                patient_ids = self._df["id"].where(is_patient, "")
                
                ref_keys = [
                    "subject.reference",
                    "patient.reference",
                ]
                
                for key in ref_keys:
                    if key in self._df.columns:
                        ref_values = self._df[key].fillna("")
                        cleaned_refs = ref_values.str.replace("Patient/", "", regex=False).str.replace("urn:uuid:", "", regex=False)
                        mask = (patient_ids == "") & (cleaned_refs != "")
                        patient_ids = patient_ids.where(~mask, cleaned_refs)
                
                self._df["patientId"] = patient_ids
            except:
                pass

    def check_subject_reference(self, row):
        """Extract patient id from subject/patient reference fields.

        Args:
            row (Mapping[str, Any]): A dataframe row as a mapping.

        Returns:
            str: The patient id (without "Patient/" or "urn:uuid:" prefix) or
            an empty string if not found.
        """
        keys = [
            "resource.subject.reference",
            "resource.patient.reference",
            "subject.reference",
            "patient.reference",
        ]

        def _clean(ref):
            if not isinstance(ref, str):
                return ""
            return ref.replace("Patient/", "").replace("urn:uuid:", "")

        for key in keys:
            ref = row.get(key, None)
            if pd.notna(ref):
                return _clean(ref)

        return ""

    def get_info(self):
        """Return a concise info string for the current dataframe.

        Returns:
            str: Dataframe info text or a message if no dataframe is set.
        """
        if self._df is None:
            return "Dataframe is empty"
        return self._df.info()

    def process_list(self, myList):
        """Extract code or display strings from a list of coding-like dicts.

        Args:
            myList (list): A list of dictionaries that may contain "code" or
                "display" keys.

        Returns:
            list[str]: A list of extracted codes/display texts.
        """
        myCodes = []
        if isinstance(myList, list):
            for entry in myList:
                if "code" in entry:
                    myCodes.append(entry["code"])
                elif "display" in entry:
                    myCodes.append(entry["display"])
        return myCodes

    def llm_query(self, query, llm, embed_model=None, verbose=True):
        """Execute a natural language query against the dataframe using LLM tools.

        Args:
            query (str): The natural language question.
            llm (Any): The language model instance usable by llama_index.
            embed_model (str | None): Optional HuggingFace embedding model name.
            verbose (bool): Whether to enable verbose output from the query engine.

        Raises:
            Exception: If required libraries are not installed.
            Exception: If the dataframe is empty.

        Returns:
            Any: The query result from the underlying engine.
        """
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            from llama_index.core import Settings
            from llama_index.experimental.query_engine import PandasQueryEngine
        except Exception:
            raise Exception("llama_index or HuggingFaceEmbeddings not installed")
        if self._df is None:
            raise Exception("Dataframe is empty")
        if embed_model is None:
            embed_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        else:
            embed_model = HuggingFaceEmbeddings(model_name=embed_model)
        Settings.llm = llm
        Settings.embed_model = embed_model
        query_engine = PandasQueryEngine(
            df=self._df,
            verbose=verbose,
        )
        return query_engine.query(query)
