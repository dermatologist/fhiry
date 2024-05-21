


from abc import ABC
from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.medication import Medication


class FlattenFhir(ABC):

    def __init__(self, fhir_object, config_json=None):
        self._flattened = ""
        self._fhirobject = fhir_object

    @property
    def flattened(self):
        return self._flattened

    @property
    def fhirobject(self):
        return self._fhirobject

    @fhirobject.setter
    def fhir_object(self, fhirobject):
        self._fhirobject = fhirobject

    def flatten(self):
        if isinstance(self._fhirobject, Bundle):
            print("Bundle")
        elif isinstance(self._fhirobject, Patient):
            print("Patient")

