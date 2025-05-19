import pandas as pd
import requests
from lxml import html
import json

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


# Function to generate a dataframe with information on site and measure combinations for which data is available.
# Run this function with number of sites and measures you want to try for, e.g. df_all_measures(20, 30) will look for site_id's 1 through 20 and measure id's 1 through 30
def df_all_measures(ns, nm):
    print("running all measures")
    base_url = "https://www.trc.govt.nz/environment/maps-and-data/site-details"
    site_link = "?siteID="
    measure_link = "&measureID="
    time_link = "&timePeriod="
    df_all_combos = pd.DataFrame(columns=['site_id', 'site_label', 'measure_id', 'measure_label'])

    # Outer loop is by site
    for i in range(1, ns+1):
        site_id = str(i)

        # Inner loop is by measure
        for j in range(1, nm+1):
            measure_id = str(j)
            url_link = base_url + site_link + site_id + measure_link + measure_id + time_link + "365days"

            try:
                page = requests.get(url_link).text
                site_label = html.fromstring(page).xpath('/html/body/div[2]/div/div/h1/text()')[0]
                measure_label = html.fromstring(page).xpath('/html/body/div[3]/div[2]/div/div/div[2]/div[1]/h2/text()')[0]
                if len(site_label) > 0 and len(measure_label) > 0: 
                    new_row = pd.DataFrame({"site_id": site_id, "site_label": site_label, "measure_id": measure_id, "measure_label": measure_label}, index=[0])
                    df_all_combos = pd.concat([df_all_combos, new_row])
                    df_all_combos.to_csv('df_all_combos.csv', index=False)
            except:
                pass
    df_all_combos.to_csv('df_all_combos.csv', index=False)
