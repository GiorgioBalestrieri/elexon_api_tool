# Elexon API Tool

This is a minimal tool to query data from the [Elexon BMRS API](https://www.elexon.co.uk/guidance-note/bmrs-api-data-push-user-guide/).

> The Balancing Mechanism Reporting Service (BMRS) is the primary channel for
providing operational data relating to the GB Electricity Balancing and
Settlement arrangements. It’s used extensively by market participants to help
make trading decisions and understanding market dynamics, and acts as a
prompt reporting platform as well as a means of accessing historic data. The
BMRS has a wider user base both within and outside of the energy industry
and includes traders, regulators, industry forecasting teams and academics

Much content derived from [ElexonAPIWrapper](https://github.com/AyrtonB/ElexonAPIWrapper):
* extrapolating DataFrames from the `.xml` response is way less hacky than doing so from the `.csv` response
* grouping signals (`ServiceCode`s) by required arguments makes it much easier to validate queries

Contents:
1. [Dependencies](#dependencies)
2. [Installation](#installation)
3. [How To Use](#how-to-use)

## Dependencies

* `requests`
* `xmltodict`
* `pandas`

## Installation

Can be installed through pip:

* locally: `cd` into this directory and do
  ```bash
  pip install ./
  ```
* from GitHub:
  ```bash
  pip install git+https://github.com/GiorgioBalestrieri/elexon_api_tool.git
  ```

## How To Use

* register on the Elexon website to get your API key
* store it in a `api_key.txt` file in this folder
* choose the signal you are interested in (see attached csv file)
* use `query_API`
* to download data from multiple days, use `query_multiple_days`

## Example

```python
>>> from elexon_api import Client # checkout the AsyncClient to speed things up
>>> from elexon_api import get_required_parameters
>>> from elexon_api import extract_df
>>> client = Client.from_key_file() # specify path to file
>>> service_code = 'B1760'
['APIKey', 'SettlementDate', 'Period']

>>> params = {'SettlementDate': pd.datetime(2019,6,15),
              'Period': '*'}

>>> r_dict = client.query(service_code, **params, check_response=False)
>>> df = extract_df(r_dict)
>>> df.head()
```