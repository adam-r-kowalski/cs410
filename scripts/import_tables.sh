#!/bin/bash
#Imports the csv files to Hbase table. 
#Table must be created in Hbase first
#

./hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=',' -Dimporttsv.columns=HBASE_ROW_KEY,highspeed:count highspeed tables/highspeed.csv


./hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=',' -Dimporttsv.columns=HBASE_ROW_KEY,fosterstation:peakperiod,fosterstation:traveltime fosterstationpeaktraveltimes tables/foster_station_peak_travel_times.csv


./hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=',' -Dimporttsv.columns=HBASE_ROW_KEY,fosterstation:starttime,fosterstation:traveltime fosterstationtraveltimes tables/fosterstationtraveltimes.csv


./hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=',' -Dimporttsv.columns=HBASE_ROW_KEY,fosterstation:volume fosterstationvolume tables/fosterstationvolume.csv

./hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=',' -Dimporttsv.columns=HBASE_ROW_KEY,highway:id,highway:shortdirection,highway:standard,highway:name highways tables/highways.csv

./hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=',' -Dimporttsv.columns=HBASE_ROW_KEY,freewaystation:sid,freewaystation:hid,freewaystation:milepost,freewaystation:locationtext,freewaystation:upstream,freewaystation:downstream,freewaystation:stationclass,freewaystation:numberlane,freewaystation:lat,freewaystation:lon,freewaystation:length freewaystations tables/freeway_stations2.csv

./hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=',' -Dimporttsv.columns=HBASE_ROW_KEY,freewaydetector:did,freewaydetector:hid,freewaydetector:milepost,freewaydetector:locationtext,freewaydetector:class,freewaydetector:lanenumber,freewaydetector:sid freewaydetectors tables/freeway_detectors.csv

./hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=',' -Dimporttsv.columns=HBASE_ROW_KEY,freewayloopdata:did,freewayloopdata:starttime,freewayloopdata:volume,freewayloopdata:speed,freewayloopdata:occupancy,freewayloopdata:status,freewayloopdata:flags freewayloopdataoneday tables/freeway_loopdata_oneday.csv

#freeway_loopdata.csv failed to import at `53 % map, 0 % reduce`
#./hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=',' -Dimporttsv.columns=HBASE_ROW_KEY,freewayloopdata:did,freewayloopdata:starttime,freewayloopdata:volume,freewayloopdata:speed,freewayloopdata:occupancy,freewayloopdata:status,freewayloopdata:flags freewayloopdata tables/freeway_loopdata.csv








