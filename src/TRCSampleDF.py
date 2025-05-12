import pandas as pd

def sites_dataframe():
    sites = {
    "site": [8, 32, 33, 4, 42, 24],
    "site_label": ["Kapoaiaia at Cape Egmont", "Stony at Mangatete Bridge", "Taungatara at Eltham Road", "Waiwhakaiho at Hillsborough", "Waitara at Bertrand Road", "North Egmont at Visitor Centre"],
    "wd": [True, False, True, True, False, False],
    "wg": [True, False, True, True, False, False],
    "ws": [True, False, True, True, False, False],
    "at": [True, True, True, True, False, True],
    "rf": [True, True, True, True, True, True],
    "cu": [True, True, True, True, True, False],
    "ht": [True, True, True, True, False, False],
    "sm": [True, False, True, True, False, False]
    }
    df_sites = pd.DataFrame(sites)
    return(df_sites)

def measures_dataframe():
    measures = {
    "measure": [10, 4, 2, 3, 1, 9, 7, 5],
    "measure_label": ["wg", "wd", "ws", "at", "rf", "cu", "ht", "sm"],
    "description": ["Wind Gust", "Wind Direction", "Wind Speed", "Air Temperature", "Rainfall", "River Flow", "River Level", "Soil Moisture"],
    "weather": [True, True, True, True, True, False, False, False],
    "river": [False, False, False, False, True, True, True, True]
    }
    df_measures = pd.DataFrame(measures)
    return(df_measures)


def timelinks_dataframe():
    timelink = {
    "id": [1, 2, 3],
    "label": ["7days", "30days", "365days"]
    }
    df_timelink = pd.DataFrame(timelink)
    return(df_timelink)