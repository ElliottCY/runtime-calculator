import pandas as pd
import numpy as np
import matplotlib as plt

from api_handler import get_solar
from logic import runtime_calculator

df = pd.read_csv("calc_data.csv")

lat = 55
lon = -119
loss = 14
angle = 49
aspect = -8
tracking_type = 0
mounting_place = "building"
pvtech_choice = "crystSi"
bifacial_gain = 0
inverter_rate = 12
peak_power = 1
start = 0
end = 0

hourly_solar = get_solar(bifacial_gain, lat, lon, peak_power, loss, angle, aspect, tracking_type, mounting_place, pvtech_choice)

values = []

for _, row in df.iterrows():
    if row["Peak power"] == 0:
        solar = 0
    else:
        solar = hourly_solar.copy()
        for i in range(len(solar)):
            solar[i] = solar[i]*row["Peak power"]
            
    values.append(runtime_calculator(start, end, solar, bifacial_gain, row["Load"], row["Battery capacity"], row["Battery rate"], inverter_rate, row["Generator output"]))

runtime = pd.Series(values)

df["Generator runtime"] = runtime
df["Generator runtime"].to_csv("runtime.csv", index=False)
