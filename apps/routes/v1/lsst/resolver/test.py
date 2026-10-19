# Copyright 2026 AstroLab Software
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import io
import sys

import pandas as pd
import requests

APIURL = sys.argv[1]


def resolver(resolver="simbad", name_or_id="Markarian 2", output_format="json"):
    """Resolve a name using the Fink REST API"""
    payload = {
        "resolver": resolver,
        "name_or_id": name_or_id,
        "output-format": output_format,
    }

    r = requests.post(f"{APIURL}/api/v1/resolver", json=payload)

    assert r.status_code == 200, r.content

    if output_format == "json":
        pdf = pd.read_json(io.BytesIO(r.content))
    else:
        pdf = pd.read_csv(io.BytesIO(r.content))

    return pdf


def test_simbad_resolver() -> None:
    """
    Examples
    --------
    >>> test_simbad_resolver()
    """
    pdf = resolver()

    assert not pdf.empty

    for col in ["name", "oid", "otype", "jradeg", "jdedeg"]:
        assert col in pdf.columns, [col, pdf.columns]


def test_simbad_resolver_csv() -> None:
    """
    Examples
    --------
    >>> test_simbad_resolver_csv()
    """
    pdf = resolver(output_format="csv")

    assert not pdf.empty


def test_bad_request() -> None:
    """
    Examples
    --------
    >>> test_bad_request()
    """
    r = requests.post(f"{APIURL}/api/v1/resolver", json={"resolver": "simbad"})

    assert r.status_code == 400, r.content
    assert b"name_or_id" in r.content, r.content


if __name__ == "__main__":
    """ Execute the test suite """
    import doctest
    import sys

    sys.exit(doctest.testmod()[0])
