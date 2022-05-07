import pandas as pd
import numpy as np
from collections import Counter
import math
import random
import matplotlib.pyplot as plt

# read STL data
school = pd.read_csv("Demand/Pima_OD_UA_team_School_2267_Travel/Pima_OD_UA_team_2267_od_all.csv")
summer = pd.read_csv("Demand/Pima_OD_UA_team_Summer_7548_Travel/Pima_OD_UA_team_7548_od_all.csv")
snow = pd.read_csv("Demand/Pima_OD_UA_team_Snowbirds_6202_Travel/Pima_OD_UA_team_6202_od_all.csv")

sample = school.sample(n=math.ceil(0.01*len(school)))
sample.shape
sample.to_csv(r'sample.csv', index=None, header=True)

# create example 1-1104, 0-23
x1 = 1
x2 = 1104  # number of zones
x = list(range(x1, x2 + 1))
Orig = np.repeat(x, x2)
len(Orig)  # 1218816
Orig = list(Orig) * 24

x1 = 1
x2 = 1104  # number of zones
x = list(range(x1, x2 + 1))
Dest = x * x2
len(Dest)  # 1218816
Dest = list(Dest) * 24

hr = list(range(0, 1380 + 60, 60))
hr = np.repeat(hr, 1218816)

example = pd.DataFrame({'Orig': Orig, 'Dest': Dest, 'time': hr})
example.shape

# missing data
1-len(snow)/len(example)


# create dictionary to convert time
interval = {'01: 12am (12am-1am)': 0,
            '02: 1am (1am-2am)': 60,
            '03: 2am (2am-3am)': 120,
            '04: 3am (3am-4am)': 180,
            '05: 4am (4am-5am)': 240,
            '06: 5am (5am-6am)': 300,
            '07: 6am (6am-7am)': 360,
            '08: 7am (7am-8am)': 420,
            '09: 8am (8am-9am)': 480,
            '10: 9am (9am-10am)': 540,
            '11: 10am (10am-11am)': 600,
            '12: 11am (11am-12noon)': 660,
            '13: 12pm (12noon-1pm)': 720,
            '14: 1pm (1pm-2pm)': 780,
            '15: 2pm (2pm-3pm)': 840,
            '16: 3pm (3pm-4pm)': 900,
            '17: 4pm (4pm-5pm)': 960,
            '18: 5pm (5pm-6pm)': 1020,
            '19: 6pm (6pm-7pm)': 1080,
            '20: 7pm (7pm-8pm)': 1140,
            '21: 8pm (8pm-9pm)': 1200,
            '22: 9pm (9pm-10pm)': 1260,
            '23: 10pm (10pm-11pm)': 1320,
            '24: 11pm (11pm-12am)': 1380}

########################## Input STL Data #################################
input_list = [school, summer, snow]
input_name = ['school', 'summer', 'snow']
name_num = 0

for input_file in input_list:
    # demand - summer, school, snow
    demand_dt = input_file
    demand_dt.columns
    set(demand_dt['Day Type'])
    demand_dt = demand_dt[demand_dt['Day Type'] == '1: Average Weekday (M-Th)']

    # keep only O, D, OD traffic
    demand_dt = demand_dt[['Origin Zone ID', 'Destination Zone ID', 'Day Part', 'O-D Traffic (Calibrated Index)']]
    # remove redundant rows!
    set(demand_dt['Day Part'])
    demand_dt = demand_dt[demand_dt['Day Part'] != '00: All Day (12am-12am)']
    demand_dt.shape  # (1004375, 4)
    Counter(demand_dt['Day Part'])
    set(demand_dt['Origin Zone ID'])  # 1061
    set(demand_dt['Destination Zone ID'])  # 1069

    # convert text to time
    demand_dt['time'] = demand_dt['Day Part'].map(interval)
    demand_dt = demand_dt.drop('Day Part', axis=1)

    demand_dt.rename(columns={'Origin Zone ID': 'Orig',
                              'Destination Zone ID': 'Dest'},
                     inplace=True)

    # MERGE
    vol_dt = example.merge(demand_dt, on=['Orig', 'Dest', 'time'], how='left')
    len(vol_dt)  # 29251584

    vol_dt['O-D Traffic (Calibrated Index)'].describe()
    vol_dt = vol_dt.drop('time', 1)

    # replace nan with 0's
    vol_dt['O-D Traffic (Calibrated Index)'] = vol_dt['O-D Traffic (Calibrated Index)'].fillna(0)
    file_name = 'demand_' + input_name[name_num] + '.csv'
    vol_dt.to_csv(file_name, index=None, header=False)  # no header

    ########################## Convert to Demand.dat #################################
    # input
    intervals = 24  # total hours
    zone_num = 1104
    from_zone = [i for i in range(1, zone_num + 1)]

    input_od = file_name
    output_demand = 'demand_' + input_name[name_num] + '_Dy.dat'

    # open file
    f = open(input_od, 'r')
    g = open(output_demand, 'w')

    hrseq = '    '  # four space in front of hour sequence
    for zz in range(intervals + 1):
        hr = zz * 60  # turn to minutes
        hrseq = hrseq + '  %0.1f' % hr

    constant_st = "   %s 1.000" % intervals  # first line, three space in front!
    constant_st = constant_st + "\n"
    constant_st = constant_st + hrseq
    constant_st = constant_st + "\n"

    g.write(constant_st)

    i = 1
    trips = ''
    k = 1
    with open(input_od, 'r') as od_file:
        f = od_file.readlines()
        hour_time = 0
        for line in f:
            if i % (zone_num ** 2) == 1:  # new start time
                time_st = "Start Time ="
                len_time = 5 - len(str(hour_time * 60))
                time_st += ' ' * len_time + str(hour_time * 60) + ".0" + "\n"
                hour_time += 1
                g.write(time_st)

            od_traf = line.split(',')[2]
            od_traf = float(od_traf[:-1])
            intpart = int(od_traf)

            od_traf = str(format(od_traf, '.4f'))  # od traffic

            len_int = len(str(intpart))
            len_space = 5 - len_int
            trips = trips + ' ' * len_space + od_traf  # four spaces

            if k % 6 == 0:  # new line
                trips = trips + "\n"
                g.write(trips)
                trips = ''
            elif i % zone_num == 0:  # new Origin
                trips = str(trips) + "\n"
                g.write(trips)
                trips = ''
                k = 0
            k += 1
            i += 1

    g.close()

    name_num += 1

