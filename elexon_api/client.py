import os
from pathlib import Path

import asyncio
import aiohttp

import xmltodict

import datetime as dt
import pandas as pd

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from .config import (API_BASE_URL, API_VERSION,
                     DATE_FORMAT, TIME_FORMAT, DATETIME_FORMAT, 
                     DATE_PARAMS, TIME_PARAMS, DATETIME_PARAMS, 
                     REQUIRED_D, RESPONSE_D, DEFAULT_PARAM_VALUES,
                     API_KEY_FILENAME, HEADER)

class ElexonAPIException(Exception):
    pass


def get_required_parameters(service_code):
    """Get list of required parameters for service."""
    return REQUIRED_D[service_code]


class Client:

    def __init__(self, api_key, base_url=API_BASE_URL, 
                 api_version=API_VERSION):
        self._api_key = api_key
        self.base_url = base_url
        self.api_version = api_version

    @classmethod
    def from_key_file(cls, key_file=None, *args, **kwargs):
        """Initialize from api key file.
        
        If ``key_file`` is not passed, will try to
        read ``api_key`` from package directory.
        """
        if key_file is None:
            key_file = _get_api_key_path()

        if not key_file.is_file():
            raise Exception(f'{key_file} not found.')

        with open(key_file, 'r') as f:
            api_key = f.read()
        return cls(api_key, *args, **kwargs)

    def get_service_url(self, service_code):
        return f"{self.base_url}/{service_code}/{self.api_version}"

    #--------------------------------------------------------
    #                       VALIDATION
    #--------------------------------------------------------
    def _validate_params(self, service_code, params):
        """
        Check that query inputs are of the correct format.
        Will fail on missing arguments, 
        """
        if service_code not in REQUIRED_D.keys():
            raise ElexonAPIException(f"Unknown service_code: {service_code}.")

        passed_set      = set(params.keys())
        required_set    = set(REQUIRED_D[service_code])

        if passed_set != required_set:
            for extra_arg in passed_set - required_set:
                logger.info(f"Extra argument for {service_code}: {extra_arg}")
            if not required_set.issubset(passed_set):
                for missing_arg in required_set - passed_set:
                    logger.warning(f"Missing argument for {service_code}: {missing_arg}.")
                raise ElexonAPIException("Missing arguments for {service_code}.")
        return


    def _validate_response(self, service_code, params, r_dict):
        """Check response validity (for applicable signals).

        Parameters
        ----------
        params : dict
            Parameters passed to GET method.
        r_dict : dict
            Parsed response through xml.
        r : requests.Response
            Response from API call.
        """
        r_metadata = r_dict['responseMetadata']
        r_httpdesc = r_metadata['description']
        r_query = r_metadata['queryString']
        
        if r_httpdesc != 'Success':
            logger.warning(f"Bad Query. Description : {r_httpdesc}")
            msg = (f"Bad query description. Query string: {r_query}")
            raise ElexonAPIException(msg)
        
        if RESPONSE_D[service_code]:
            r_body = r_dict['responseBody']
            r_servicecode = r_body['dataItem']
            if r_servicecode != service_code:
                raise ElexonAPIException(
                    "Service codes don't match \n" +
                    f"Requested code is {service_code}" +
                    f"Returned code is {r_servicecode}")
        return

    #--------------------------------------------------------
    #                       QUERY
    #--------------------------------------------------------
    def prepare_query_params(self, service_code, params):
        """Prepare parameters for query."""
        params['APIKey'] = self._api_key

        # Use default value for required params which are not defined
        params.update({
            k:v for k,v in DEFAULT_PARAM_VALUES.items() 
            if k in REQUIRED_D[service_code] 
            and params.get(k) is None})

        params = self._format_datetime_params(params)

        return params
    
    def _format_datetime_params(self, params):
        """Update date, time and datetime params."""
        params.update({
            k:v.strftime(DATE_FORMAT) 
            for k,v in params.items() 
            if k in DATE_PARAMS 
            and isinstance(v, (dt.date, dt.datetime, pd.Timestamp))})
        
        params.update({
            k:v.strftime(TIME_FORMAT) 
            for k,v in params.items() 
            if k in TIME_PARAMS 
            and isinstance(v, (dt.time, dt.datetime, pd.Timestamp))})

        params.update({
            k:v.strftime(DATETIME_FORMAT) 
            for k,v in params.items() 
            if k in DATETIME_PARAMS 
            and isinstance(v, (dt.datetime, pd.Timestamp))})
        
        return params


    async def query_API(self, service_code, header=HEADER, check_query=True,
                        check_response=True, **params):
        """Query Elexon API.

        Parameters
        ----------
        header : dict
            Header for the :func:`~requests.get` call.
        check_query : bool
            If true, validate the query inputs.
        check_response : bool
            If true, validate response.
        **params
            Parameters for query.
        """
        params = self.prepare_query_params(service_code, params)
        if check_query: self._validate_params(service_code, params)
        url = self.get_service_url(service_code)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=header) as response:
                response.raise_for_status()
                r_text = await response.text()
        
        r_dict = xmltodict.parse(r_text)['response']
        
        if check_response: 
            self._validate_response(service_code, params, r_dict)
        
        return r_dict


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


#--------------------------------------------------------
#                       UTILS
#--------------------------------------------------------
def _get_path_to_module():
    """Get path to this module."""
    return Path(os.path.realpath(__file__)).parent

def _get_api_key_path(filename=API_KEY_FILENAME):
    """Load api key."""
    path_to_dir = _get_path_to_module()
    return path_to_dir / filename