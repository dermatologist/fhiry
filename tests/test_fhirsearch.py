import json
from pathlib import Path

import responses

from src.fhiry.fhirsearch import Fhirsearch


# Test import FHIR search results (five resources with different codes)
# separated by three mocked FHIR search results pages
# to one Pandas dataframe
@responses.activate
def test_fhirsearch():

    # Mock FHIR search URL of page 1
    jsonfile = open(
        Path(__file__).parent
        / "resources"
        / "fhirsearch"
        / "search-conditions-page1.json"
    )
    responses.add(
        responses.GET,
        "http://fhir-server/fhir/Condition?_count=2",
        json=json.load(jsonfile),
        status=200,
    )

    # Mock FHIR search URL of page 2
    jsonfile = open(
        Path(__file__).parent
        / "resources"
        / "fhirsearch"
        / "search-conditions-page2.json"
    )
    responses.add(
        responses.GET,
        "http://fhir-server/fhir?_getpages=b5f2b2b3-6372-4159-969a-49cbd243e154&_getpagesoffset=2&_count=2&_bundletype=searchset",
        json=json.load(jsonfile),
        status=200,
    )

    # Mock FHIR search URL of page 3
    jsonfile = open(
        Path(__file__).parent
        / "resources"
        / "fhirsearch"
        / "search-conditions-page3.json"
    )
    responses.add(
        responses.GET,
        "http://fhir-server/fhir?_getpages=b5f2b2b3-6372-4159-969a-49cbd243e154&_getpagesoffset=4&_count=2&_bundletype=searchset",
        json=json.load(jsonfile),
        status=200,
    )

    # Start a FHIR search on/with the mocked FHIR Server URLs
    # which should process all 5 Condition resources (separated on three FHIR search results pages)
    fs = Fhirsearch(fhir_base_url="http://fhir-server/fhir")
    fs.page_size = 2

    df = fs.search(resource_type="Condition", search_parameters={})

    # exit if df is None
    if df is None:
        raise ValueError("Dataframe is None, something went wrong with the FHIR search")

    # resulting df must include all 5 condition resources (processed from all three mocked search results pages)
    assert len(df) == 5

    # Are all the different Condition codes there (exactly once)?
    assert len(df[df["code.coding.codes"].astype("string") == "A00.0"]) == 1
    assert len(df[df["code.coding.codes"].astype("string") == "A01.0"]) == 1
    assert len(df[df["code.coding.codes"].astype("string") == "A02.0"]) == 1
    assert len(df[df["code.coding.codes"].astype("string") == "A03.0"]) == 1
    assert len(df[df["code.coding.codes"].astype("string") == "A04.0"]) == 1

    # There is no resource with code A05.0 in the FHIR search results
    assert len(df[df["code.coding.codes"].astype("string") == "A05.0"]) == 0
