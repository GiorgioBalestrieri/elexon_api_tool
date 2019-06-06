import os
from pathlib import Path
import pandas as pd

from .config import REQUIRED_D, API_KEY_FILENAME

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def get_required_parameters(service_code):
    """Get list of required parameters for service."""
    return REQUIRED_D[service_code]


def _get_path_to_module():
    """Get path to this module."""
    return Path(os.path.realpath(__file__)).parent


def get_api_key_path(filename=API_KEY_FILENAME):
    """Load api key."""
    path_to_dir = _get_path_to_module()
    return path_to_dir / filename


class ElexonAPIException(Exception):
    pass


def extract_df(r_dict):
    """Extract DataFrame from dictionary.

    Parameters
    ----------
    r_dict : dict 
        Obtained from response through xmltodict.
    """
    r_body       = r_dict['responseBody']
    r_items_list = r_body['responseList']['item']
    try:
        df_items = pd.DataFrame(r_items_list)
    except Exception as e:
        logger.warning(f"Failed to create DataFrame: {e!r}")
        try:
            df_items = pd.DataFrame(r_items_list, index=[0])
        except Exception as e:
            logger.error("Failed to create DataFrame.")
            raise e
    
    return df_items