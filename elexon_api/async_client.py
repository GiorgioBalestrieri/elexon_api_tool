"""
async_client.py
===============

Async implementation of Elexon API Client.
"""

import aiohttp
import xmltodict

from .config import HEADER
from .client import Client
# from .utils import extract_df

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class AsyncClient(Client):

    async def query(self, service_code, header=HEADER, check_query=True,
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
        
        # TODO recycle session?
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=header) as response:
                response.raise_for_status()
                r_text = await response.text()
        
        r_dict = xmltodict.parse(r_text)['response']
        
        if check_response: 
            self._validate_response(service_code, params, r_dict)
        
        return r_dict

