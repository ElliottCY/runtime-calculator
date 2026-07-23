def get_rate(soc, high_soc_rate, battery_rate, inverter_rate):
    return min(battery_rate, inverter_rate)
    if(soc >= 0.90):
        
        return high_soc_rate
    else:
        return min(battery_rate, inverter_rate)

def runtime_calculator(hourly_solar, high_soc_rate, bifacial_gain, load, battery_capacity, battery_rate, inverter_rate, generator_output):
    
    runtime = 0
    hours = 8760
    battery_state = battery_capacity
    hourly_load = load
    generator_loading = 0.9
    generator_output = generator_output * generator_loading
    low = 0.4
    high = 1
    inverter_efficiency = 0.97
    rate = min(inverter_rate, battery_rate)
    hybrid = rate > 0 and battery_capacity > 0
    battery_efficiency = 0.98

    
    
    for i in range(hours):
        if(isinstance(hourly_solar, list)): #checks if there is solar power
            solar = hourly_solar[i] * (1 + bifacial_gain/100)
            
        else:
            solar = 0
        charge_rate = get_rate(battery_state/battery_capacity, high_soc_rate, battery_rate, inverter_rate)
        if(hourly_load - solar <= 0): #solar exceeds load, battery gets charged
            battery_state += battery_efficiency*min(charge_rate, (solar - hourly_load))
            battery_state = min(battery_state, battery_capacity)
            
            
        elif((battery_state - (hourly_load - solar)) > low*battery_capacity and rate >= (hourly_load - solar)/inverter_efficiency): #battery can cover the difference, generator not needed
            battery_state -= (hourly_load - solar)/inverter_efficiency
            

        else: #generator has to run
            temp = 0
            generator_on = False

            while(temp < 60): #cycles through every minute of an hour that uses the generator
                charge_rate = get_rate(battery_state/battery_capacity, high_soc_rate, battery_rate, inverter_rate)
                if(battery_state < low*battery_capacity or not hybrid or rate < (hourly_load - solar)/inverter_efficiency): #turn generator on
                    generator_on = True
                    
                
                if(battery_state >= high*battery_capacity and hybrid and rate >=(hourly_load - solar)/inverter_efficiency): #turn generator off
                    generator_on = False
                    

                if(generator_on):
                    battery_state += battery_efficiency*min(charge_rate, inverter_efficiency * (generator_output - hourly_load + solar))/60
                    battery_state = min(battery_state, battery_capacity)
                    runtime += 1/60
                else:
                    battery_state -= (hourly_load - solar)/60/inverter_efficiency
                    

                temp += 1

    if(load > inverter_rate*inverter_efficiency):
        return 8760

    return runtime
    
