import os
from pathlib import Path
import requests
import xmltodict
import datetime as dt
import pandas as pd
from .api_config import (API_BASE_URL, API_VERSION, 
                        DATE_FORMAT, TIME_FORMAT, DATETIME_FORMAT, 
                        DATE_PARAMS, TIME_PARAMS, DATETIME_PARAMS, 
                        REQUIRED_D, RESPONSE_D, DEFAULT_PARAM_VALUES,
                        API_KEY_FILENAME, HEADER)

#--------------------------------------------------------
#                       UTILS
#--------------------------------------------------------
def _get_path_to_module():
    """Get path to this module."""
    return Path(os.path.realpath(__file__)).parent


def _load_api_key(filename=API_KEY_FILENAME):
    """Load api key."""
    path_to_dir = _get_path_to_module()
    path_to_file = path_to_dir / filename
    
    if not path_to_file.is_file():
        raise Exception(f'{path_to_file} not found.')
        
    with open(path_to_file, 'r') as f:
        api_key = f.read()
        
    return api_key


#--------------------------------------------------------
#                       VALIDATION
#--------------------------------------------------------
def _check_query(params):
    """
    Check that query inputs are of the correct format.
    Will fail on missing arguments, 
    """
    assert 'ServiceCode' in params.keys(), \
           "ServiceCode not specified."
    assert params['ServiceCode'] in REQUIRED_D.keys(), \
           f"Unknown ServiceCode: {params['ServiceCode']}"

    passed_set      = set(params.keys())
    required_set    = set(REQUIRED_D[params['ServiceCode']])

    if passed_set != required_set:
        print("Extra arguments: \n", "\n".join(passed_set - required_set))
        if not required_set.issubset(passed_set):
            raise Exception("Missing arguments: \n" + 
                            "\n".join(required_set - passed_set))
    return


def _check_response(params, r_dict, r):
    """
    Check response validity (for applicable signals).

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
        raise Exception(f"Bad Query. Description : \n{r_httpdesc}"
                        f"Query url: {r.url}")
    
    if RESPONSE_D[params['ServiceCode']] == True:
        r_body = r_dict['responseBody']
        r_servicecode = r_body['dataItem']
        if r_servicecode != params['ServiceCode']:
            raise Exception("Service codes don't match \n" +
                            f"Returned code is {r_servicecode}" +
                            f"Query url: {r.url}")
    return


def get_required_parameters(service_code, verbose=False):
    """
    Get list of required parameters for service.
    """
    param_list = REQUIRED_D[service_code]
    if verbose: print('Required parameters: \n', '\n'.join(param_list))
    return param_list


#--------------------------------------------------------
#                       QUERY
#--------------------------------------------------------
def query_API(header=HEADER, check_query=True, check_response=True,  **params):
    """
    Query Elexon API.

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

    # get API key if not passed
    if params.get('APIKey') is None: params['APIKey'] = _load_api_key()

    # for all required params which have default values, replace None with default
    params.update({k:v for k,v in DEFAULT_PARAM_VALUES.items() 
                  if k in REQUIRED_D[params['ServiceCode']] 
                  and params.get(k) is None})
    
    if check_query: _check_query(params)

    url = f"{API_BASE_URL}/{params['ServiceCode']}/{API_VERSION}"

    # update date, time and datetime params
    params.update({k:v.strftime(DATE_FORMAT) for k,v in params.items() 
                  if k in DATE_PARAMS and isinstance(v, (dt.date, dt.datetime, pd.Timestamp))})
    params.update({k:v.strftime(TIME_FORMAT) for k,v in params.items() 
                  if k in TIME_PARAMS and isinstance(v, (dt.time, dt.datetime, pd.Timestamp))})
    params.update({k:v.strftime(DATETIME_FORMAT) for k,v in params.items() 
                  if k in DATETIME_PARAMS and isinstance(v, (dt.datetime, pd.Timestamp))})
    
    response = requests.get(url, params=params, headers=header)

    if not response.ok: 
        raise Exception(f"Query failed with status code {response.status_code}" +
                        f"Query url: {response.url}" +
                        f"\nFull message: {response.text}")
    
    r_dict = xmltodict.parse(response.text)['response']    
    
    if check_response: _check_response(params, r_dict, response)
    
    df_items = extract_df(r_dict)
    
    return df_items


def query_multiple_days(start, end, date_param, **params):
    """
    Wrapper around query_API.

    Args:
    ------
    start : datetime.datetime or datetime.date
        Included.
    end : datetime.datetime or datetime.date
        Included.
    date_param : str
        Name of the parameter associated to the date.
    **params
        Passed to query_API.
    """

    df_l = [] # faster than appending dataframes
    
    for date in pd.DatetimeIndex(start=start, end=end, freq='d'):
        if isinstance(date_param, str):            
            params.update({date_param: date})
        elif isinstance(date_param, (list, tuple, set)):
            params.update({p:date for p in date_param})
        df = query_API(**params)
        df_l.append(df)

    return pd.concat(df_l, axis=0, ignore_index=True)


def extract_df(r_dict):
    """
    Extract DataFrame from dictionary.

    Parameters
    ----------
    r_dict : dict 
        Obtained from response through xmltodict.
    """
    r_body       = r_dict['responseBody']
    r_items_list = r_body['responseList']['item']
    try:
        df_items = pd.DataFrame(r_items_list)
    except:
        df_items = pd.DataFrame(r_items_list, index=[0])
    
    return df_items

