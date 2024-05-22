


from abc import ABC
from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.medication import Medication
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
        if isinstance(self._fhirobject, Bundle):
            self._flattened = "Bundle"
        elif isinstance(self._fhirobject, Patient):
            self._flattened = self.flatten_patient(self._fhirobject)
        elif isinstance(self._fhirobject, Observation):
            self._flattened = self.flatten_observation(self._fhirobject)

    def get_timeago(self, datestring: datetime) -> str:
        """
        Returns a string representing the time elapsed since the given date.

        :param datestring: The date to calculate the time ago from.
        :type datestring: datetime
        :return: A string representing the time elapsed since the given date.
        :rtype: str
        """
        return timeago.format(datestring.replace(tzinfo=None), datetime.datetime.now())

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
        try:
            flat_patient += f"born {self.get_timeago(patient.birthDate)}. "
        except:
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