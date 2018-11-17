# %% imports
import pandas as pd


# %% stations
stations = pd.read_csv(
    'data/freeway_stations.csv', usecols=['locationtext', 'length'])
stations.rename(
    columns={
        'locationtext': 'station:locationtext',
        'length': 'station:length'},
    inplace=True)

# %% detectors
detectors = pd.read_csv(
    'data/freeway_detectors.csv', usecols=['detectorid', 'locationtext'])
detectors.rename(
    columns={
        'detectorid': 'detector:id',
        'locationtext': 'detector:locationtext'},
    inplace=True)

# %% loop data
loop_data = pd.read_csv(
    'data/freeway_loopdata_OneHour.csv',
    usecols=['detectorid', 'starttime', 'volume', 'speed'])
loop_data.rename(
    columns={
        'detectorid': 'loopdata:detectorid',
        'starttime': 'loopdata:starttime',
        'volume': 'loopdata:volume',
        'speed': 'loopdata:speed'},
    inplace=True)


# %% loop data start time
loop_data_start_time = loop_data['loopdata:starttime']


def loop_data_in_date_range(start_date, end_date):
    lower_bound = loop_data_start_time >= start_date
    upper_bound = loop_data_start_time < end_date
    return loop_data[lower_bound & upper_bound]


# %% foster station volume september 21, TODO: change dates
filtered_loop_data = loop_data_in_date_range(
    '9/15/2011 0:00:00', '9/15/2011 0:10:00')
loop_data_volume = filtered_loop_data['loopdata:volume'].dropna().values.sum()

foster_station_volume = pd.DataFrame(
    [loop_data_volume], columns=['fosterstation:volume'])


# %% foster station travel times september 22, TODO: change dates
filtered_loop_data = loop_data_in_date_range(
    '9/15/2011 0:10:00', '9/15/2011 0:20:00')
filtered_loop_data['loopdata:speed'].dropna().values

# %% visualize
stations.head()

detectors.head()

loop_data.head()


foster_station_volume.head()
