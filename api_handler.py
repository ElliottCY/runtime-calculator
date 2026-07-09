import requests
import pprint 
def get_solar(bifacial_gain, lat, lon, peakpower, loss, angle, aspect, tracking_type, mounting_place, pvtech_choice):
    url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"

    params = {
        "lat": lat,
        "lon": lon,
        "peakpower": peakpower,
        "loss": loss,
        "angle": angle,    #tilt
        "aspect": aspect,    #azimuth
        "outputformat": "json",
        "pvcalculation": 1,
        
        "trackingtype": tracking_type,        # 0 = fixed, 1 = single-axis, 2 = dual-axis
        "mountingplace": mounting_place,  # "free" = ground-mounted, "building" = roof

        #module_type
        "pvtechchoice": pvtech_choice,  # crystalline silicon (default)
        "startyear" : 2015,
        "endyear": 2015

    }

    response = requests.get(url, params=params)
    data = response.json()
    #pprint.pprint(data)
   
    hourly_solar = []
    for hour in data["outputs"]["hourly"]:
        hourly_solar.append(hour["P"]/1000)



    print(sum(hourly_solar)*(1 + bifacial_gain / 100))
    
    #pprint.pprint(hourly_solar)
    

    return hourly_solar



