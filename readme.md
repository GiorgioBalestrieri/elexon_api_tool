# Elexon API Tool

This is a minimal tool to query data from the [Elexon API](https://www.elexon.co.uk/wp-content/uploads/2017/06/bmrs_api_data_push_user_guide_v1.1.pdf).

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