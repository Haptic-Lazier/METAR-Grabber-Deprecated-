import requests

""" This is the API portion of the program
    
    ARGs:
        aic: Airport Identifier Code
    
    RETURNS:
        Raw JSON dictionary
    
    Limitations:
        This program is limited by the fact it uses AWC.
            You cannot call more than 100 times a minute. 
            I would reccomend attaching this to a database that stores the last known weather report for that airport.
            If you truely need more than 100 requests a minute please vist https://aviationweather.gov/data/api/#cache
            
            You cannot call outside of the US as this is an American Data site.
            
            You cannot call more than one station at a time. See Link above for that capability.
    
    Made by entirely by Haptic-Lazier
"""


def metar_get(aic):
# This function returns the METAR Value
    url = f"https://aviationweather.gov/api/data/metar?ids={aic}&format=json"
    page = requests.get(url)
    data = page.json()

    metar = data[0]

    return metar

def taf_get(aic):
# This function returns the TAF Value
    url = f"https://aviationweather.gov/api/data/taf?ids={aic}&format=json"
    page = requests.get(url)
    data = page.json()

    taf = data[0]

    return taf

#print(metar_get("KOMA")) #Test function calling Omaha International Airport
#print(taf_get("KOMA")) #Test function calling Omaha International Airport