


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

    def get_timeago(self, datestring: datetime) -> str:
        return timeago.format(datestring, datetime.datetime.now())

    def flatten_patient(self, patient: Patient) -> str:
        flat_patient = ""
        try:
            flat_patient += f"Medical record of a {patient.gender} patient "
        except:
            _logger.info(f"Gender not found for patient {patient.id}")
            flat_patient += "Medical record of a patient "
        try:
            flat_patient += f"born {self.get_timeago(patient.birthDate)}. "
        except:
            _logger.info(f"Birthdate not found for patient {patient.id}")
            flat_patient += "of unknown age. "
        return flat_patient
