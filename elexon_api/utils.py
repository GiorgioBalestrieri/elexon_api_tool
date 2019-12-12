import os
from pathlib import Path
import pandas as pd
from collections import defaultdict
from typing import Dict, List

from .config import REQUIRED_D, API_KEY_FILENAME

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def get_required_parameters(service_code: str) -> List[str]:
    """Get list of required parameters for service."""
    return REQUIRED_D[service_code]


def _get_path_to_module() -> Path:
    """Get path to this module."""
    return Path(os.path.realpath(__file__)).parent


def get_api_key_path(filename=API_KEY_FILENAME) -> Path:
    """Load api key."""
    path_to_dir = _get_path_to_module()
    return path_to_dir / filename


class ElexonAPIException(Exception):
    pass


def extract_df(r_dict: dict) -> pd.DataFrame:
    """Extract DataFrame from dictionary.

    Parameters
    ----------
    r_dict
        Obtained from response through xmltodict.
    """
    r_body       = r_dict['responseBody']
    r_items_list = r_body['responseList']['item']
    try:
        df_items = pd.DataFrame(r_items_list)
    except Exception as e:
        logger.warning(f"Failed to create DataFrame.", exc_info=True)
        try:
            df_items = pd.DataFrame(r_items_list, index=[0])
        except Exception as e:
            logger.error("Failed to create DataFrame.")
            raise e
    
    return df_items


def extract_df_by_record_type(r_dict: dict) -> Dict[str,pd.DataFrame]:
    content: List[dict] = r_dict['responseBody']['responseList']['item']
    records_d = split_list_of_dicts(content, 'recordType')
    return {k: pd.DataFrame(l) for k,l in records_d.items()}


def split_list_of_dicts(dict_list: List[dict], key: str) -> Dict[str,List[dict]]:
    """Split list of dictionaries into multiples lists based on a specific key.
    
    Output lists are stored in a dicionary with the value used as key.

    Example:
    >>> dict_list = [
            {
                "recordType": "a",
                "foo": 1,
                "bar": 1,
            },
            {
                "recordType": "b",
                "foo": 2,
                "bar": 2,
            },
            {
                "recordType": "b",
                "foo": 3,
                "bar": 3,
            }
        ]
    >>> split_list_of_dicts(dict_list, 'recordType')
    {
        "a": [
            {
                "recordType": "a",
                "foo": 1,
                "bar": 1,
            },
        ],
        "b": [
            {
                "recordType": "b",
                "foo": 2,
                "bar": 2,
            },
            {
                "recordType": "b",
                "foo": 3,
                "bar": 3,
            }
        ]
    }
    ]
    """
    result = defaultdict(list)
    for d in dict_list:
        result[d[key]].append(d)
    return result