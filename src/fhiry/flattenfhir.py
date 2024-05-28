


from abc import ABC
from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.medication import Medication
from fhir.resources.procedure import Procedure
from fhir.resources.condition import Condition
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.documentreference import DocumentReference
import timeago, datetime
import logging
_logger = logging.getLogger(__name__)

class FlattenFhir(ABC):

    def __init__(self, fhir_object=None, config_json=None):
        self._flattened = ""
        self._fhirobject = fhir_object
        if fhir_object:
            self.flatten()

    @property
    def flattened(self):
        return self._flattened

    @property
    def fhirobject(self):
        return self._fhirobject

    @fhirobject.setter
    def fhir_object(self, fhirobject):
        self._fhirobject = fhirobject
        self.flatten()

    def flatten(self):
        if not self._fhirobject:
            _logger.info("FHIR object is not set.")
            raise ValueError("FHIR object is not set.")
        if isinstance(self._fhirobject, Bundle):
            self._flattened = ""
            for entry in self._fhirobject.entry:
                if entry.resource.resource_type == "Patient":
                    self._flattened += self.flatten_patient(entry.resource)
                elif entry.resource.resource_type == "Observation":
                    self._flattened += self.flatten_observation(entry.resource)
                elif entry.resource.resource_type == "Medication":
                    self._flattened += self.flatten_medication(entry.resource)
                elif entry.resource.resource_type == "Procedure":
                    self._flattened += self.flatten_procedure(entry.resource)
                elif entry.resource.resource_type == "Condition":
                    self._flattened += self.flatten_condition(entry.resource)
                elif entry.resource.resource_type == "AllergyIntolerance":
                    self._flattened += self.flatten_allergyintolerance(entry.resource)
                elif entry.resource.resource_type == "DocumentReference":
                    self._flattened += self.flatten_documentreference(entry.resource)
                else:
                    _logger.info(f"Resource type not supported: {entry.resource.resource_type}")
        elif isinstance(self._fhirobject, Patient):
            self._flattened = self.flatten_patient(self._fhirobject)
        elif isinstance(self._fhirobject, Observation):
            self._flattened = self.flatten_observation(self._fhirobject)
        elif isinstance(self._fhirobject, Medication):
            self._flattened = self.flatten_medication(self._fhirobject)
        elif isinstance(self._fhirobject, Procedure):
            self._flattened = self.flatten_procedure(self._fhirobject)
        elif isinstance(self._fhirobject, Condition):
            self._flattened = self.flatten_condition(self._fhirobject)
        elif isinstance(self._fhirobject, AllergyIntolerance):
            self._flattened = self.flatten_allergyintolerance(self._fhirobject)
        elif isinstance(self._fhirobject, DocumentReference):
            self._flattened = self.flatten_documentreference(self._fhirobject)
        else:
            _logger.info(f"Resource type not supported: {type(self._fhirobject)}")
        return self._flattened

    def get_timeago(self, datestring: datetime) -> str:
        """
        Returns a string representing the time elapsed since the given date.

        :param datestring: The date to calculate the time ago from.
        :type datestring: datetime
        :return: A string representing the time elapsed since the given date.
        :rtype: str
        """
        try:
            datestring = datestring.replace(tzinfo=None)
        except:
            pass
        return timeago.format(datestring, datetime.datetime.now())

    def flatten_patient(self, patient: Patient) -> str:
        """
        Flatten the patient object into a string representation.

        Args:
            patient (Patient): The patient object to be flattened.

        Returns:
            str: The flattened string representation of the patient object.
        """
        flat_patient = ""
        if patient.gender:
            flat_patient += f"Medical record of a {patient.gender} patient "
        else:
            _logger.info(f"Gender not found for patient {patient.id}")
            flat_patient += "Medical record of a patient "
        if patient.birthDate:
            flat_patient += f"born {self.get_timeago(patient.birthDate)}. "
        else:
            _logger.info(f"Birthdate not found for patient {patient.id}")
            flat_patient += "of unknown age. "
        return flat_patient

    def flatten_observation(self, observation: Observation) -> str:
        """
        Flatten the observation object into a string representation.

        Args:
            observation (Observation): The observation object to be flattened.

        Returns:
            str: The flattened string representation of the observation object.
        """
        flat_observation = ""
        if observation.code:
            flat_observation += f"{observation.code.coding[0].display} "
        else:
            _logger.info(f"Code not found for observation {observation.id}")
            flat_observation += "Observation "
        if observation.effectiveDateTime:
            flat_observation += f"recorded {self.get_timeago(observation.effectiveDateTime)} was "
        else:
            _logger.info(f"Effective date not found for observation {observation.id}")
            flat_observation += "of unknown date was "
        if observation.valueQuantity:
            flat_observation += f"Value: {observation.valueQuantity.value} {observation.valueQuantity.unit}. "
        elif observation.valueString:
            flat_observation += f"Value: {observation.valueString}. "
        elif observation.valueBoolean:
            flat_observation += f"Value: {observation.valueBoolean}. "
        elif observation.valueRange:
            flat_observation += f"Value: {observation.valueRange.low.value} - {observation.valueRange.high.value} {observation.valueRange.low.unit}. "
        elif observation.valueRatio:
            flat_observation += f"Value: {observation.valueRatio.numerator.value} {observation.valueRatio.numerator.unit} / {observation.valueRatio.denominator.value} {observation.valueRatio.denominator.unit}. "
        elif observation.valuePeriod:
            flat_observation += f"Value: {observation.valuePeriod.start} - {observation.valuePeriod.end}. "
        elif observation.valueDateTime:
            flat_observation += f"Value: {observation.valueDateTime}. "
        elif observation.valueTime:
            flat_observation += f"Value: {observation.valueTime}. "
        elif observation.valueSampledData:
            flat_observation += f"Value: {observation.valueSampledData.data}. "
        else:
            _logger.info(f"Value not found for observation {observation.id}")
            flat_observation += "Value: unknown. "
        if observation.interpretation[0].text:
            flat_observation += f"Interpretation: {observation.interpretation[0].text}. "
        return flat_observation

    def flatten_medication(self, medication: Medication) -> str:
        """
        Flatten the medication object into a string representation.

        Args:
            medication (Medication): The medication object to be flattened.

        Returns:
            str: The flattened string representation of the medication object.
        """
        flat_medication = ""
        if medication.code:
            flat_medication += f"{medication.code.coding[0].display} "
        else:
            _logger.info(f"Code not found for medication {medication.id}")
            flat_medication += "Medication "
        if medication.status:
            flat_medication += f"Status: {medication.status}. "
        else:
            _logger.info(f"Status not found for medication {medication.id}")
            flat_medication += "Status: unknown. "
        return flat_medication

    def flatten_procedure(self, procedure: Procedure) -> str:
        """
        Flatten the procedure object into a string representation.

        Args:
            procedure (Procedure): The procedure object to be flattened.

        Returns:
            str: The flattened string representation of the procedure object.
        """
        flat_procedure = ""
        if procedure.code:
            flat_procedure += f"{procedure.code.coding[0].display} was "
        else:
            _logger.info(f"Code not found for procedure {procedure.id}")
            flat_procedure += "Procedure was"
        if procedure.occurrenceDateTime:
            flat_procedure += f"{procedure.status} {self.get_timeago(procedure.occurrenceDateTime)}. "
        elif procedure.occurrencePeriod:
            flat_procedure += f"{procedure.status} {self.get_timeago(procedure.occurrencePeriod.start)}. "
        else:
            _logger.info(f"Performed date not found for procedure {procedure.id}")
            flat_procedure += "on unknown date. "
        return flat_procedure

    def flatten_condition(self, condition: Condition) -> str:
        """
        Flatten the condition object into a string representation.

        Args:
            condition (Condition): The condition object to be flattened.

        Returns:
            str: The flattened string representation of the condition object.
        """
        flat_condition = ""
        if condition.code:
            flat_condition += f"{condition.code.coding[0].display} "
        else:
            _logger.info(f"Code not found for condition {condition.id}")
            flat_condition += "Condition "
        if condition.onsetDateTime:
            flat_condition += f"was diagnosed {self.get_timeago(condition.onsetDateTime)}. "
        else:
            _logger.info(f"Onset date not found for condition {condition.id}")
            flat_condition += "was diagnosed. "
        return flat_condition

    def flatten_allergyintolerance(self, allergyintolerance: AllergyIntolerance) -> str:
        """
        Flatten the allergyintolerance object into a string representation.

        Args:
            allergyintolerance (AllergyIntolerance): The allergyintolerance object to be flattened.

        Returns:
            str: The flattened string representation of the allergyintolerance object.
        """
        flat_allergyintolerance = ""
        if allergyintolerance.code:
            flat_allergyintolerance += f"{allergyintolerance.code.coding[0].display} "
        else:
            _logger.info(f"Code not found for allergyintolerance {allergyintolerance.id}")
            flat_allergyintolerance += "AllergyIntolerance "
        if allergyintolerance.onsetDateTime:
            flat_allergyintolerance += f" allergy was reported on {self.get_timeago(allergyintolerance.onsetDateTime)}. "
        else:
            _logger.info(f"Onset date not found for allergyintolerance {allergyintolerance.id}")
            flat_allergyintolerance += "allergy reported. "
        return flat_allergyintolerance

    def flatten_documentreference(self, documentreference: DocumentReference) -> str:
        """
        Flatten the documentreference object into a string representation.

        Args:
            documentreference (DocumentReference): The documentreference object to be flattened.

        Returns:
            str: The flattened string representation of the documentreference object.
        """
        flat_documentreference = ""
        for content in documentreference.content:
            if content.attachment.contentType == "text/plain":
                flat_documentreference += f"{content.attachment.title}: {content.attachment.data}"
            else:
                _logger.info(f"Attachment for documentreference {documentreference.id} is not text/plain.")
        if documentreference.date:
            flat_documentreference += f" was created {self.get_timeago(documentreference.date)}. "
        else:
            _logger.info(f"Date not found for documentreference {documentreference.id}")
            flat_documentreference += " was created. "
        return flat_documentreference