from . import config
from .utils import get_required_parameters, extract_df, extract_df_by_record_type
from .client import Client

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

try:
    import aiohttp
    async_available = True
except ImportError:
    async_available = False

if async_available:
    from .async_client import AsyncClient
    logger.info("Async client available.")
else:
    logger.info("Async client not available, aiohttp is needed.")
    class AsyncClient(Client):
        def __init__(self, *args, **kwargs):
            raise NotImplementedError(
                "AsyncClient is not available" 
                + " because aiohttp is not installed.")