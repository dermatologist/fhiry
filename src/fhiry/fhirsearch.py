import pandas as pd
import requests

from . import Fhiry


class Fhirsearch(object):

    def __init__(self, fhir_base_url):

        self.fhir_base_url = fhir_base_url

        # Batch size (entries per page)
        self.page_size = 500

        # Keyword arguments for HTTP(s) requests (f.e. for auth)
        # Example parameters:
        # Authentication: https://requests.readthedocs.io/en/latest/user/authentication/#basic-authentication
        # Proxies: https://requests.readthedocs.io/en/latest/user/advanced/#proxies
        # SSL Certificates: https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification
        self.requests_kwargs = {}

    def search(self, resource_type="Patient", search_parameters={}):

        headers = {"Content-Type": "application/fhir+json"}

        if '_count' not in search_parameters:
            search_parameters['_count'] = self.page_size

        search_url = f'{self.fhir_base_url}/{resource_type}'
        r = requests.get(search_url, params=search_parameters, headers=headers, **self.requests_kwargs)
        r.raise_for_status()
        bundle_dict = r.json()

        if 'entry' in bundle_dict:
            df = process_bundle(bundle_dict)

            next_page_url = get_next_page_url(bundle_dict)

            while next_page_url:
                r = requests.get(next_page_url, headers=headers, **self.requests_kwargs)
                r.raise_for_status()
                bundle_dict = r.json()
                df_page = process_bundle(bundle_dict)
                df = pd.concat([df, df_page])

                next_page_url = get_next_page_url(bundle_dict)
        else:
            df = pd.DataFrame(columns=[])

        return df


def process_bundle(bundle_dict):
    f = Fhiry()
    f.process_bundle_dict(bundle_dict)
    return f.df


def get_next_page_url(bundle_dict):
    links = bundle_dict.get('link')
    if links:
       for link in links:
            relation = link.get('relation')
            if relation == 'next':
                return link.get('url')

    return None
