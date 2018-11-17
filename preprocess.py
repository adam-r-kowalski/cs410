# %% imports
import pandas as pd


# %% stations
stations = pd.read_csv('data/freeway_stations.csv')
stations = stations[['locationtext', 'length']]

# %% detectors
detectors = pd.read_csv('data/freeway_detectors.csv')
detectors = detectors[['detectorid', 'locationtext']]

# %% loop data
loop_data = pd.read_csv('data/freeway_loopdata_OneHour.csv')
loop_data = loop_data[['detectorid', 'starttime', 'volume', 'speed']]

# %% visualize
stations.head()

detectors.head()

loop_data.head()
