# %% imports
import pandas as pd
from datetime import timedelta


# %% read_csv
def read_csv(filename, columns):
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

# TODO: use all loop data instead of just one hour
loop_data = read_csv(
    'data/freeway_loopdata_OneHour.csv',
    columns={
        'detectorid': 'loopdata:detectorid',
        'starttime': 'loopdata:starttime',
        'volume': 'loopdata:volume',
        'speed': 'loopdata:speed'
    })


# %% loop data start time
loop_data_start_time = loop_data['loopdata:starttime']


# %% loop data in date range
def loop_data_in_date_range(start_date, end_date,
                            loop_data=loop_data,
                            loop_data_start_time=loop_data_start_time):
    lower_bound = loop_data_start_time >= start_date
    upper_bound = loop_data_start_time < end_date
    return loop_data[lower_bound & upper_bound]


# %% foster station volume september 21, TODO: change dates
def foster_station_volume_september_21():
    filtered_loop_data = loop_data_in_date_range(
        '9/15/2011 0:00:00', '9/15/2011 0:10:00')

    loop_data_volume = (filtered_loop_data['loopdata:volume']
                        .dropna()
                        .values
                        .sum())

    return pd.DataFrame([loop_data_volume], columns=['fosterstation:volume'])


foster_station_volume = foster_station_volume_september_21()


# %% insert row into dataframe
def insert_row(df, row):
    df.loc[-1] = row
    df.index += 1
    df.sort_index(inplace=True)


# %% add minutes to time
def add_minutes_to_time(time, minutes=5):
    new_time = pd.to_datetime(time) + timedelta(minutes=minutes)
    return new_time.strftime("%-m/%d/%Y %-H:%M:%S")


# %% foster station travel times september 22, TODO: change dates, refactor code?
def foster_station_travel_times_september_22():
    foster_station_travel_times = pd.DataFrame(
        columns=['fosterstation:starttime', 'fosterstation:traveltime'])

    start_time = '9/15/2011 0:10:00'
    end_time = '9/15/2011 0:20:00'
    filtered_loop_data = loop_data_in_date_range(start_time, end_time)

    _, foster_station_length = (stations
                                .loc[stations['station:locationtext'] == 'Foster NB']
                                .values[0])

    filtered_loop_data_start_time = filtered_loop_data['loopdata:starttime']

    # TODO: remove hard coded minutes
    interval_time = add_time_to_interval(start_time, minutes=1)

    while start_time < end_time:
        interval_data = loop_data_in_date_range(
            start_time, interval_time,
            filtered_loop_data, filtered_loop_data_start_time)

        mean_speed = interval_data['loopdata:speed'].dropna().values.mean()

        # TODO: convert mean speed from mph to mps and report travel time in seconds
        insert_row(foster_station_travel_times,
                   [start_time, mean_speed / foster_station_length])

        start_time = interval_time

        interval_time = add_minutes_to_time(start_time, minutes=1)

    return foster_station_travel_times


foster_station_travel_times = foster_station_travel_times_september_22()


# %% visualize
stations.head()

detectors.head()

loop_data.head()


foster_station_volume.head()


foster_station_travel_times.head()
