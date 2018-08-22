import os
from pathlib import Path
import requests
from io import StringIO
import pandas as pd

# default values
API_BASE_URL     = 'https://api.bmreports.com/BMRS'
API_KEY_FILENAME = 'api_key.txt'
API_VERSION      = 'v1'
DATE_FORMAT      = '%Y-%m-%d'

def _get_path_to_module():
    '''Get path to this module.'''
    return Path(os.path.realpath(__file__)).parent


def _load_api_key(filename=API_KEY_FILENAME):
    '''Load api key.'''
    path_to_dir = _get_path_to_module()
    path_to_file = path_to_dir / filename
    
    if not path_to_file.is_file():
        raise Exception(f'{path_to_file} not found.')
        
    with open(path_to_file, 'r') as f:
        api_key = f.read()
        
    return api_key


def query_apy(signal_key, settlement_date, 
              period=None, output_format='csv', api_key=None,
              api_base_url=API_BASE_URL, api_version=API_VERSION):
    
    if api_key is None: api_key = _load_api_key()
    date_qstr = settlement_date.strftime(DATE_FORMAT)
    period_qstr = get_period_qstr(period)
    api_url = f'{api_base_url}/{signal_key}/{api_version}'
    
    params = {'SettlementDate': date_qstr,
              'Period':         '*',
              'ServiceType':    output_format,
              'APIKey':         api_key}
    
    r = requests.get(api_url, params=params)
    if not r.ok: raise Exception(f'Query failed with code {r.status_code}. \n Full message: {r.text}')
    
    return r


def extract_csv_from_response(r):
    """A bit hacky."""
    with StringIO(r.text.split('\n*\n*')[-1].replace('<EOF>','')) as data:
        df = pd.read_csv(data)
    return df


def query_multiple_days(signal_key, start, end, **query_kwargs):
    """
    Start and end dates are included.
    """
    
    df_l = []
    
    for settlement_date in pd.DatetimeIndex(start=start, end=end, freq='d'):
        r = query_apy(signal_key, settlement_date, **query_kwargs)
        df_l.append(extract_csv_from_response(r))

    return pd.concat(df_l, axis=0, ignore_index=True)
    

def get_period_qstr(period=None):
    if period is None:
        return '*'
    elif isinstance(period, int):
            return str(period)
    else:
        raise TypeError(f'period must be None (for whole day) or int, but {period!r} was passed')
        
