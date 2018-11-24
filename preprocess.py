# %% imports
import pandas as pd
import numpy as np
from datetime import timedelta
from typing import Mapping


# %% write tables for loading
def write_tables_for_loading(filename):
    (pd
        .read_csv(f'data/{filename}.csv')
        .to_csv(f'tables/{filename}.csv', header=None))


write_tables_for_loading('freeway_stations')
write_tables_for_loading('freeway_detectors')
write_tables_for_loading('highways')
write_tables_for_loading('freeway_loopdata')


# %% read_csv
def read_csv(filename: str, columns: Mapping[str, str]) -> pd.DataFrame:
    df = pd.read_csv(filename, usecols=columns.keys())
    df.rename(columns=columns, inplace=True)
    return df


# %% read in data
stations = read_csv(
    'data/freeway_stations.csv',
    columns={
        'locationtext': 'station:locationtext',
        'length': 'station:length'
    })

detectors = read_csv(
    'data/freeway_detectors.csv',
    columns={
        'detectorid': 'detector:id',
        'locationtext': 'detector:locationtext'
    })

loop_data = read_csv(
    'data/freeway_loopdata.csv',
    columns={
        'detectorid': 'loopdata:detectorid',
        'starttime': 'loopdata:starttime',
        'volume': 'loopdata:volume',
        'speed': 'loopdata:speed'
    })


# %% insert row into dataframe
def insert_row(df, row):
    df.loc[-1] = row
    df.index += 1
    df.sort_index(inplace=True)


# %% speeds greater than 100
def speeds_greater_than_100():
    return pd.DataFrame(
        [(loop_data['loopdata:speed'].dropna().values > 100).sum()],
        columns=['highspeed:count'])


high_speed = speeds_greater_than_100()


# %% loop data start time
loop_data_start_time = loop_data['loopdata:starttime']


# %% loop data in date range
def loop_data_in_date_range(start_date: str, end_date: str,
                            loop_data=loop_data,
                            loop_data_start_time=loop_data_start_time):
    lower_bound = loop_data_start_time >= start_date
    upper_bound = loop_data_start_time < end_date
    return loop_data[lower_bound & upper_bound]


# %% foster station volume september 21
def foster_station_volume_september_21():
    filtered_loop_data = loop_data_in_date_range(
        '2011-09-21 00:00:00', '2011-09-22 00:00:00')

    loop_data_volume = (filtered_loop_data['loopdata:volume']
                        .dropna()
                        .values
                        .sum())

    return pd.DataFrame([loop_data_volume], columns=['fosterstation:volume'])


foster_station_volume = foster_station_volume_september_21()


# %% add minutes to time
def add_minutes_to_time(time, minutes=5):
    new_time = pd.to_datetime(time) + timedelta(minutes=minutes)
    return new_time.strftime("%Y-%m-%d %-H:%M:%S")


# %% mean travel times between time periods
def mean_travel_times_between_time_periods(data_frame: pd.DataFrame,
                                           start_time: str, end_time: str,
                                           interval: int = 5) -> pd.DataFrame:
    filtered_loop_data = loop_data_in_date_range(start_time, end_time)

    _, foster_station_length = (stations
                                .loc[stations['station:locationtext'] == 'Foster NB']
                                .values[0])

    filtered_loop_data_start_time = filtered_loop_data['loopdata:starttime']

    interval_time = add_minutes_to_time(start_time, minutes=interval)

    while start_time < end_time:
        interval_data = loop_data_in_date_range(
            start_time, interval_time,
            filtered_loop_data, filtered_loop_data_start_time)

        speeds = interval_data['loopdata:speed'].dropna().values

        if len(speeds) > 0:
            mean_speed = speeds.mean()
            insert_row(data_frame,
                       [start_time, foster_station_length / mean_speed * 3600])

        start_time = interval_time

        interval_time = add_minutes_to_time(start_time, minutes=interval)

    return data_frame


# %% foster station travel times september 22
def foster_station_travel_times_september_22():
    foster_station_travel_times = pd.DataFrame(
        columns=['fosterstation:starttime', 'fosterstation:traveltime'])

    return mean_travel_times_between_time_periods(
        foster_station_travel_times,
        start_time='2011-09-22 00:00:00',
        end_time='2011-09-23 00:00:00')


foster_station_travel_times = foster_station_travel_times_september_22()


# %% foster station peak travel times
def foster_station_peak_travel_times_september_22() -> pd.DataFrame:
    foster_station_travel_times = pd.DataFrame(
        columns=['fosterstation:peakperiod', 'fosterstation:traveltime'])

    mean_travel_times_between_time_periods(
        foster_station_travel_times,
        start_time='2011-09-22 07:00:00',
        end_time='2011-09-22 09:00:00',
        interval=120)

    return mean_travel_times_between_time_periods(
        foster_station_travel_times,
        start_time='2011-09-22 16:00:00',
        end_time='2011-09-22 18:00:00',
        interval=120)


peak_travel_times = foster_station_peak_travel_times_september_22()


# %% visualize
stations.head()

detectors.head()

loop_data.head()


high_speed.to_csv('tables/high_speed.csv', header=None)
high_speed.head()


foster_station_volume.to_csv('tables/foster_station_volume.csv', header=None)
foster_station_volume.head()


foster_station_travel_times.to_csv(
    'tables/foster_station_travel_times.csv', header=None)
foster_station_travel_times.head()


peak_travel_times.to_csv(
    'tables/foster_station_peak_travel_times.csv', header=None)
peak_travel_times.head()
