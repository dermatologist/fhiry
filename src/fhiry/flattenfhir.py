


from abc import ABC
from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.medication import Medication


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
            self._flattened = "Patient"

