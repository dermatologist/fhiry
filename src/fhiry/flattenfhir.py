"""
Copyright (c) 2024 Bell Eapen

This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""

import datetime
import logging
from abc import ABC
import timeago
from prodict import Prodict

_logger = logging.getLogger(__name__)


class FlattenFhir(ABC):

    def __init__(self, fhirobject={}, config_json=None):
        self._flattened = ""
        self._fhirobject = Prodict.from_dict(fhirobject)
        if fhirobject:
            self.flatten()

    @property
    def flattened(self):
        return self._flattened

    @property
    def fhirobject(self):
        return self._fhirobject

    @fhirobject.setter
    def fhirobject(self, fhirobject):
        self._fhirobject = Prodict.from_dict(fhirobject)
        self.flatten()

    def flatten(self):
        if not self._fhirobject:
            _logger.info("FHIR object is not set.")
            raise ValueError("FHIR object is not set.")
        self._flattened = ""
        if self._fhirobject.resourceType == "Bundle":
            for entry in self._fhirobject.entry:
                _entry = Prodict.from_dict(entry)
                self.get_flattened_text(_entry.resource)
        else:
            self.get_flattened_text(self._fhirobject)
        return self._flattened

    def get_flattened_text(self, entry):
        if entry.resourceType == "Patient":
            self._flattened += self.flatten_patient(entry)
        elif entry.resourceType == "Observation":
            self._flattened += self.flatten_observation(entry)
        elif entry.resourceType == "Medication":
            self._flattened += self.flatten_medication(entry)
        elif entry.resourceType == "Procedure":
            self._flattened += self.flatten_procedure(entry)
        elif entry.resourceType == "Condition":
            self._flattened += self.flatten_condition(entry)
        elif entry.resourceType == "AllergyIntolerance":
            self._flattened += self.flatten_allergyintolerance(entry)
        elif entry.resourceType == "DocumentReference":
            self._flattened += self.flatten_documentreference(entry)
        else:
            _logger.info(f"Resource type not supported: {entry.resourceType}")
        return self._flattened

    def get_timeago(self, datestring) -> str:
        """
        Returns a string representing the time elapsed since the given date.

        :param datestring: The date to calculate the time ago from.
        :type datestring: datetime
        :return: A string representing the time elapsed since the given date.
        :rtype: str
        """
        datestring = datestring[0:10]
        return timeago.format(datestring, datetime.datetime.now())

    def flatten_patient(self, patient) -> str:
        """
        Flatten the patient object into a string representation.

        Args:
            patient (Patient): The patient object to be flattened.

        Returns:
            str: The flattened string representation of the patient object.
        """
        flat_patient = ""
        if "gender" in patient:
            flat_patient += f"Medical record of a {patient.gender} patient "
        else:
            _logger.info(f"Gender not found for patient {patient.id}")
            flat_patient += "Medical record of a patient "
        if "birthDate" in patient:
            flat_patient += f"born {self.get_timeago(patient.birthDate)}. "
        else:
            _logger.info(f"Birthdate not found for patient {patient.id}")
            flat_patient += "of unknown age. "
        return flat_patient

    def flatten_observation(self, observation) -> str:
        """
        Flatten the observation object into a string representation.

        Args:
            observation (Observation): The observation object to be flattened.

        Returns:
            str: The flattened string representation of the observation object.
        """
        flat_observation = ""
        if "code" in observation:
            _display = observation.code.coding[0]
            flat_observation += f"{_display['display']} "
        else:
            _logger.info(f"Code not found for observation {observation.id}")
            flat_observation += "Observation "
        if "effectiveDateTime" in observation:
            flat_observation += (
                f"recorded {self.get_timeago(observation.effectiveDateTime)} was "
            )
        else:
            _logger.info(f"Effective date not found for observation {observation.id}")
            flat_observation += "of unknown date was "
        if "valueQuantity" in observation and "value" in observation.valueQuantity:
            flat_observation += f"Value: {observation.valueQuantity.value} "
            if "unit" in observation.valueQuantity:
                flat_observation += f"{observation.valueQuantity.unit}. "
        elif "valueString" in observation:
            flat_observation += f"Value: {observation.valueString}. "
        elif "valueBoolean" in observation:
            flat_observation += f"Value: {observation.valueBoolean}. "
        elif (
            "valueRange" in observation
            and "low" in observation.valueRange
            and "high" in observation.valueRange
        ):
            flat_observation += f"Value: {observation.valueRange.low.value} - {observation.valueRange.high.value} {observation.valueRange.low.unit}. "
        elif (
            "valueRatio" in observation
            and "numerator" in observation.valueRatio
            and "denominator" in observation.valueRatio
        ):
            flat_observation += f"Value: {observation.valueRatio.numerator.value} {observation.valueRatio.numerator.unit} / {observation.valueRatio.denominator.value} {observation.valueRatio.denominator.unit}. "
        elif (
            "valuePeriod" in observation
            and "start" in observation.valuePeriod
            and "end" in observation.valuePeriod
        ):
            flat_observation += f"Value: {observation.valuePeriod.start} - {observation.valuePeriod.end}. "
        elif "valueDateTime" in observation and observation.valueDateTime != "":
            flat_observation += f"Value: {observation.valueDateTime}. "
        elif "valueTime" in observation and observation.valueTime != "":
            flat_observation += f"Value: {observation.valueTime}. "
        elif (
            "valueSampledData" in observation and "data" in observation.valueSampledData
        ):
            flat_observation += f"Value: {observation.valueSampledData.data}. "
        else:
            _logger.info(f"Value not found for observation {observation.id}")
            flat_observation += "Value: unknown. "
        try:
            if (
                "interpretation" in observation
                and "coding" in observation.interpretation[0]
            ):
                if "coding" in observation.interpretation[0]:
                    _text = observation.interpretation[0]["coding"][0]
                    flat_observation += f"Interpretation: {_text['display']}. "
        except:
            _logger.info(f"Interpretation not found for observation {observation.id}")
            flat_observation += "Interpretation: unknown. "
        return flat_observation

    def flatten_medication(self, medication) -> str:
        """
        Flatten the medication object into a string representation.

        Args:
            medication (Medication): The medication object to be flattened.

        Returns:
            str: The flattened string representation of the medication object.
        """
        flat_medication = ""
        if "code" in medication:
            flat_medication += f"{medication.code.coding[0]['display']} "
        else:
            _logger.info(f"Code not found for medication {medication.id}")
            flat_medication += "Medication "
        if "status" in medication:
            flat_medication += f"Status: {medication.status}. "
        else:
            _logger.info(f"Status not found for medication {medication.id}")
            flat_medication += "Status: unknown. "
        return flat_medication

    def flatten_procedure(self, procedure) -> str:
        """
        Flatten the procedure object into a string representation.

        Args:
            procedure (Procedure): The procedure object to be flattened.

        Returns:
            str: The flattened string representation of the procedure object.
        """
        flat_procedure = ""
        if (
            "code" in procedure
            and "coding" in procedure.code
            and "display" in procedure.code.coding[0]
        ):
            flat_procedure += f"{procedure.code.coding[0]['display']} was "
        else:
            _logger.info(f"Code not found for procedure {procedure.id}")
            flat_procedure += "Procedure was"
        if "occurrenceDateTime" in procedure:
            flat_procedure += (
                f"{procedure.status} {self.get_timeago(procedure.occurrenceDateTime)}. "
            )
        elif "occurrencePeriod" in procedure:
            flat_procedure += f"{procedure.status} {self.get_timeago(procedure.occurrencePeriod.start)}. "
        else:
            _logger.info(f"Performed date not found for procedure {procedure.id}")
            flat_procedure += "on unknown date. "
        return flat_procedure

    def flatten_condition(self, condition) -> str:
        """
        Flatten the condition object into a string representation.

        Args:
            condition (Condition): The condition object to be flattened.

        Returns:
            str: The flattened string representation of the condition object.
        """
        flat_condition = ""
        if "code" in condition:
            flat_condition += f"{condition.code.coding[0]['display']} "
        else:
            _logger.info(f"Code not found for condition {condition.id}")
            flat_condition += "Condition "
        if condition.onsetDateTime:
            flat_condition += (
                f"was diagnosed {self.get_timeago(condition.onsetDateTime)}. "
            )
        else:
            _logger.info(f"Onset date not found for condition {condition.id}")
            flat_condition += "was diagnosed. "
        return flat_condition

    def flatten_allergyintolerance(self, allergyintolerance) -> str:
        """
        Flatten the allergyintolerance object into a string representation.

        Args:
            allergyintolerance (AllergyIntolerance): The allergyintolerance object to be flattened.

        Returns:
            str: The flattened string representation of the allergyintolerance object.
        """
        flat_allergyintolerance = ""
        _display = allergyintolerance.code.coding[0]
        if "code" in allergyintolerance and "display" in _display:
            flat_allergyintolerance += f"{_display['display']} "
        else:
            _logger.info(
                f"Code not found for allergyintolerance {allergyintolerance.id}"
            )
            flat_allergyintolerance += "AllergyIntolerance "
        if "onsetDateTime" in allergyintolerance:
            flat_allergyintolerance += f" allergy was reported on {self.get_timeago(allergyintolerance.onsetDateTime)}. "
        else:
            _logger.info(
                f"Onset date not found for allergyintolerance {allergyintolerance.id}"
            )
            flat_allergyintolerance += "allergy reported. "
        return flat_allergyintolerance

    def flatten_documentreference(self, documentreference) -> str:
        """
        Flatten the documentreference object into a string representation.

        Args:
            documentreference (DocumentReference): The documentreference object to be flattened.

        Returns:
            str: The flattened string representation of the documentreference object.
        """
        flat_documentreference = ""
        for content in documentreference.content:
            content = Prodict.from_dict(content)
            if content.attachment.contentType == "text/plain":
                flat_documentreference += (
                    f"{content.attachment.title}: {content.attachment.data}"
                )
            else:
                _logger.info(
                    f"Attachment for documentreference {documentreference.id} is not text/plain."
                )
        if "date" in documentreference:
            flat_documentreference += (
                f" was created {self.get_timeago(documentreference.date)}. "
            )
        else:
            _logger.info(f"Date not found for documentreference {documentreference.id}")
            flat_documentreference += " was created. "
        return flat_documentreference
