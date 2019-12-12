"""
config.py
=========

Elexon API configuration.
"""

API_VERSION         = 'v1'
API_BASE_URL        = f'https://api.bmreports.com/BMRS'
API_KEY_FILENAME    = 'api_key.txt'
HEADER              = {'Accept': 'application/xml'}

#---------------------------------------------
#           Date/Datetime Info
#---------------------------------------------
DATE_FORMAT     = '%Y-%m-%d'
TIME_FORMAT     = '%H:%M:%S'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DATE_PARAMS = ['SettlementDate', 
               "FromSettlementDate", "ToSettlementDate",
               'StartDate', 'EndDate', 
               "FromDate", "ToDate", 
               "FromClearedDate", "ToClearedDate"]

TIME_PARAMS = ["StartTime", "EndTime"]

DATETIME_PARAMS = ["FromDateTime", "ToDateTime"]

#---------------------------------------------
#           Required Params
#---------------------------------------------

DEFAULT_PARAM_VALUES = {
    'Period': '*' # by default, get all periods
}

# parameters common to all services (mandatory)
COMMON_PARAMS = ["APIKey"]

# map ServiceCode to group
SERVICE_TO_GROUP = {'B0610': 1,
                    'B0620': 1,
                    'B0630': 2,
                    'B0640': 3,
                    'B0650': 4,
                    'B0710': 5,
                    'B0720': 5,
                    'B0810': 4,
                    'B0910': 4,
                    'B1010': 5,
                    'B1020': 5,
                    'B1030': 5,
                    'B1320': 1,
                    'B1330': 3,
                    'B1410': 4,
                    'B1420': 4,
                    'B1430': 1,
                    'B1440': 1,
                    'B1510': 5,
                    'B1520': 5,
                    'B1530': 5,
                    'B1540': 5,
                    'B1610': 1,
                    'B1620': 1,
                    'B1630': 1,
                    'B1720': 1,
                    'B1730': 1,
                    'B1740': 1,
                    'B1750': 1,
                    'B1760': 1,
                    'B1770': 1,
                    'B1780': 1,
                    'B1790': 1,
                    'B1810': 1,
                    'B1820': 1,
                    'B1830': 1,
                    'BMUNITSEARCH': 14,
                    'BOD': 11,
                    'CDN': 7,
                    'DEMCI': 15,
                    'DEMMF2T14D': 11,
                    'DEMMF2T52W': 11,
                    'DERBMDATA': 8,
                    'DERSYSDATA': 12,
                    'DETSYSPRICES': 8,
                    'DEVINDOD': 6,
                    'DISBSAD': 6,
                    'DYNBMDATA': 8,
                    'FORDAYDEM': 6,
                    'FOU2T14D': 11,
                    'FOU2T52W': 11,
                    'FREQ': 9,
                    'FUELHH': 6,
                    'FUELINST': 9,
                    'FUELINSTHHCUR': 10,
                    'HISTACCEPTS': 8,
                    'HISTSYSWARN': 11,
                    'INDOITSDO': 6,
                    'INDPKDEMINFO': 11,
                    'INDTRIADDEMINFO': 11,
                    'INTERFUELHH': 6,
                    'LATESTACCEPTS': 11,
                    'LOLPDRM': 15,
                    'MELIMBALNGC': 6,
                    'MID': 6,
                    # 'MID_BMRS': 'MID_BMRS',
                    'MKTDEPTHDATA': 13,
                    'NETBSAD': 8,
                    'NONBM': 6,
                    'NOU2T14D': 11,
                    'NOU2T52W': 11,
                    'NOUY1': 11,
                    'NOUY2': 11,
                    'NOUY3': 11,
                    'NOUY4': 11,
                    'NOUY5': 11,
                    'PHYBMDATA': 8,
                    'PKDEMYESTTDYTOM': 11,
                    'QAS': 6,
                    'ROLSYSDEM': 6,
                    'SOSOP': 11,
                    'SOSOT': 11,
                    'STORAW': 16,
                    'SYSDEM': 6,
                    'SYSMSG': 11,
                    'SYSWARN': 6,
                    'SYSWARNTDYTOM': 11,
                    'TEMP': 6,
                    'TRADINGUNIT': 8,
                    'UOU2T14D': 11,
                    'UOU2T52W': 11,
                    'WINDFORFUELHH': 6,
                    'WINDFORPK': 6,
                    'ZOU2T14D': 11,
                    'ZOU2T52W': 11,
                    'ZOUY1': 11,
                    'ZOUY2': 11,
                    'ZOUY3': 11,
                    'ZOUY4': 11,
                    'ZOUY5': 11}

# list of parameters required by each group
GROUP_TO_REQUIRED = {
        1   :   ["SettlementDate", "Period"],
        2   :   ["Year", "Week"],
        3   :   ["Year", "Month"],
        4   :   ["Year"],
        5   :   ["StartDate", "EndTime", "StartTime", "EndDate"],
        6   :   ["FromDate", "ToDate"],
        7   :   ["FromClearedDate", "ToClearedDate"],
        8   :   ["SettlementDate", "SettlementPeriod"],
        9   :   ["FromDateTime", "ToDateTime"],
        10  :   ["FuelType"],
        11  :   [],
        12  :   ["FromSettlementDate", "ToSettlementDate", "SettlementPeriod"],
        13  :   ["SettlementDate"],
        14  :   ["BmUnitId", "BmUnitType", "LeadPartyName", "NgcBmUnitName"],
        15  :   ["FromSettlementDate", "ToSettlementDate"],
        16  :   ["FromSettlementDate"]
    }

# to be implemented (as dict?)
OPTIONAL_PARAMS = [
    'FuelType',
    'BMUnitId' 
]

# create dictionary {ServiceCode: list_of_parameters}
# watch out, this can fail silently
assert set(SERVICE_TO_GROUP.values()).issubset(set(GROUP_TO_REQUIRED.keys())), \
       ("Some service groups are not defined: \n", 
        "\n".join(set(SERVICE_TO_GROUP.values()) - set(GROUP_TO_REQUIRED.keys())))
REQUIRED_D = {service: COMMON_PARAMS + GROUP_TO_REQUIRED[group] 
              for service, group in SERVICE_TO_GROUP.items()}

#---------------------------------------------
#           Response Info
#---------------------------------------------
# NOTE convert to list?
RESPONSE_D = {'B0610': True,
              'B0620': True,
              'B0630': True,
              'B0640': True,
              'B0650': True,
              'B0710': True,
              'B0720': True,
              'B0810': True,
              'B0910': True,
              'B1010': True,
              'B1020': True,
              'B1030': True,
              'B1320': True,
              'B1330': True,
              'B1410': True,
              'B1420': True,
              'B1430': True,
              'B1510': True,
              'B1520': True,
              'B1530': True,
              'B1540': True,
              'B1610': True,
              'B1620': True,
              'B1630': True,
              'B1720': True,
              'B1730': True,
              'B1740': True,
              'B1750': True,
              'B1760': True,
              'B1770': True,
              'B1780': True,
              'B1790': True,
              'B1810': True,
              'B1820': True,
              'B1830': True,
              'BMUNITSEARCH': False,
              'BOD': False,
              'CDN': False,
              'DEMCI': False,
              'DEMMF2T14D': False,
              'DEMMF2T52W': False,
              'DERBMDATA': False,
              'DERSYSDATA': False,
              'DETSYSPRICES': False,
              'DEVINDOD': False,
              'DISBSAD': False,
              'DYNBMDATA': False,
              'FORDAYDEM': False,
              'FOU2T14D': False,
              'FOU2T52W': False,
              'FREQ': False,
              'FUELHH': False,
              'FUELINST': False,
              'FUELINSTHHCUR': False,
              'HISTACCEPTS': False,
              'HISTSYSWARN': False,
              'INDOITSDO': False,
              'INDPKDEMINFO': False,
              'INDTRIADDEMINFO': False,
              'INTERFUELHH': False,
              'LATESTACCEPTS': False,
              'LOLPDRM': False,
              'MELIMBALNGC': False,
              'MID': False,
              'MID_BMRS': False,
              'MKTDEPTHDATA': False,
              'NETBSAD': False,
              'NONBM': False,
              'NOU2T14D': False,
              'NOU2T52W': False,
              'NOUY1': False,
              'NOUY2': False,
              'NOUY3': False,
              'NOUY4': False,
              'NOUY5': False,
              'PHYBMDATA': False,
              'PKDEMYESTTDYTOM': False,
              'QAS': False,
              'ROLSYSDEM': False,
              'SOSOP': False,
              'SOSOT': False,
              'STORAW': False,
              'SYSDEM': False,
              'SYSMSG': False,
              'SYSWARN': False,
              'SYSWARNTDYTOM': False,
              'TEMP': False,
              'TRADINGUNIT': False,
              'UOU2T14D': False,
              'UOU2T52W': False,
              'WINDFORFUELHH': False,
              'WINDFORPK': False,
              'ZOU2T14D': False,
              'ZOU2T52W': False,
              'ZOUY1': False,
              'ZOUY2': False,
              'ZOUY3': False,
              'ZOUY4': False,
              'ZOUY5': False}