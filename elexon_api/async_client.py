"""
async_client.py
===============

Async implementation of Elexon API Client.
"""

import aiohttp
import xmltodict
from collections import OrderedDict

from .config import HEADER
from .client import Client
from .client import (prepare_query_params,
                     validate_params, 
                     get_service_url, 
                     validate_response)

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class AsyncClient(Client):

    async def query(self, 
                    service_code: str, 
                    header: dict = HEADER, 
                    check_query: bool = True,
                    check_response: bool = True, 
                    **params) -> OrderedDict:
        """Query Elexon API.

        Parameters
        ----------
        service_code : str
        header : dict
            Header for the :func:`~requests.get` call.
        check_query : bool
            If true, validate the query inputs.
        check_response : bool
            If true, validate response.
        **params
            Parameters for query.
        """
        params = prepare_query_params(self._api_key, service_code, params)
        if check_query: validate_params(service_code, params)
        url = get_service_url(self.base_url, self.api_version, service_code)
        
        # TODO recycle session?
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=header) as response:
                response.raise_for_status()
                r_text = await response.text()
        
        r_dict = xmltodict.parse(r_text)['response']
        
        if check_response: 
            validate_response(service_code, params, r_dict)
        return r_dict

