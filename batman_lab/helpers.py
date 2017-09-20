import numpy as np
from datascience import *
import folium

def remove_nan(t):
    """
    Removes all rows with nan values checking each column
    Note you should use this AFTER stripping the table of columns you do not need
    so you do not remove rows when given a column without much information

    Will remove most nan values but may not work with some other default missing values
    (specifically, will not remove 0, -999, etc. values)

    Parameters:
    t: a table whose rows with nan values you want to remove

    returns a table identical to t but without rows containing nan values
    """
    def checkNotnan(val):
        if (val!=val)|(val=='nan')|(val=='NAN')|(val=='NaN'):
            return False
        return True
    for i in range(t.num_columns):
        t = t.where(i, checkNotnan)
    return t

def addMarkers(fol_map, mark, color="blue",icon='star',max_num=100):
    """
    adds markers to folium fol_map based on a table mark
    Parameters:
    fol_map: a folium.Map class that you want to add markers to
    mark: a table containing two columns 'Latitude' and 'Longitude'
        if these columns do not exits, defaults to using first column as latitude and 2nd as longitude
    color: color of the marker added (default: blue)
    icon: icon of marker added (default: star)
    max_num: the maximum number of markers added. Use to not overload folium map (default: 100)

    returns nothing. Will modify fol_map directly
    """

    if ("Latitude" in mark.column_labels) & ("Longitude" in mark.column_labels):
        lat_index = mark.column_index("Latitude")
        lon_index = mark.column_index("Longitude")
    else:
        lat_index = 0
        lon_index = 1
    for i in range(mark.num_rows):
        row = mark.row(i)
        lat = row[lat_index]
        lon = row[lon_index]
        folium.Marker([lat,lon],icon=folium.Icon(color=color, icon=icon)).add_to(fol_map)
        if (i>max_num):
             return

def dist_coord(lat1,lon1,lat2,lon2):
    """
    returns distance in km between 2 coordinates
    Not entirely accurate (assumes perfectly spherical earth) but works for most purposes
    """

    R = 6373.0
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (np.sin(dlat/2))**2 + np.cos(lat1) * np.cos(lat2) * (np.sin(dlon/2))**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = R * c
    return distance
