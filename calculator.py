import tkinter as tk
from tkinter import ttk
from api_handler import get_solar
from logic import runtime_calculator

# Function to handle form submission
def submit():
    tracking_options = {
        "Fixed" : 0,
        "Single-axis": 1,
        "Two-axis": 2,
        "Vertical-axis": 3,
        "Horizontal East-West": 4,
        "Inclined North-South": 5
    }   

    battery_rate_options = {
        "0" : 0,
        "2" : 8.6,
        "3" : 12.9,
        "4" : 14.4,
        "5" : 14.4,
        "6" : 14.4,
        "7" : 14.4,
        "8" : 14.4,
    }

    required = [
        bifacial_gain, lat, lon, peakpower, loss, angle, aspect, tracking, mounting_place, pvtech_choice, annual_load, battery_num, inverter_rate
    ]

    numerical = [
        bifacial_gain, lat, lon, peakpower, loss, angle, aspect, annual_load, inverter_rate
    ]

    for field in required:
        if field.get().strip() == "":
            result_label.config(text = "Please fill out all fields before submitting.")
            return
        
    for field in numerical:
        try:
            float(field.get())
        except ValueError:
            result_label.config(text = "All fields must only contain numbers")
            return

    if float(generator_output.get()) < float(annual_load.get()):
        result_label.config(text= "Generator output must be greater than average load")
        return


    tracking_type = tracking_options[tracking.get()]
    battery_rate = battery_rate_options[battery_num.get()]
    battery_capacity = int(battery_num.get()) * 4.8

    if(float(peakpower.get()) > 0):
        data = get_solar(float(bifacial_gain.get()), lat.get(), lon.get(), peakpower.get(), loss.get(), angle.get(), aspect.get(), tracking_type, mounting_place.get(), pvtech_choice.get())
    else:
        data = 0


    runtime = runtime_calculator(data, float(bifacial_gain.get()), float(annual_load.get()), battery_capacity, battery_rate, float(inverter_rate.get()), float(generator_output.get()))
    
    if float(inverter_rate.get()) < float(annual_load.get()):
        result_label.config(text=f"{round(runtime, 2)} \nWarning: inverter rate below average load")
    else:
        result_label.config(text=round(runtime, 2))



# Create main window
root = tk.Tk()
root.title("7 Input Form")
root.geometry("800x400")

# Labels + Inputs
tk.Label(root, text="Latitude").grid(row=0, column=0, padx=10, pady=5, sticky="w")
lat = tk.Entry(root)
lat.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Longitude").grid(row=1, column=0, padx=10, pady=5, sticky="w")
lon = tk.Entry(root)
lon.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Peak Power (KW)").grid(row=2, column=0, padx=10, pady=5, sticky="w")
peakpower = tk.Entry(root)
peakpower.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Loss (%)").grid(row=3, column=0, padx=10, pady=5, sticky="w")
loss = tk.Entry(root)
loss.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Angle (Degrees From Horizontal)").grid(row=4, column=0, padx=10, pady=5, sticky="w")
angle = tk.Entry(root)
angle.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Aspect (Degrees From South)").grid(row=5, column=0, padx=10, pady=5, sticky="w")
aspect = tk.Entry(root)
aspect.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Tracking Type").grid(row=6, column=0, padx=10, pady=5, sticky="w")
tracking = ttk.Combobox(root, values=["Fixed", "Single-axis", "Two-axis", "Vertical-axis", "Horizontal East-West", "Inclined North-South"], state="readonly")
tracking.grid(row=6, column=1, padx=10, pady=10)

tk.Label(root, text="Mounting Place ").grid(row=7, column=0, padx=10, pady=5, sticky="w")
mounting_place = ttk.Combobox(root, values=["free", "building"], state="readonly")
mounting_place.grid(row=7, column=1, padx=10, pady=10)

tk.Label(root, text="PV Tech").grid(row=8, column=0, padx=10, pady=5, sticky="w")
pvtech_choice = ttk.Combobox(root, values=["crystSi", "CIS", "CdTe", "Unknown"], state="readonly")
pvtech_choice.grid(row=8, column=1, padx=10, pady=10)

tk.Label(root, text="PV Tech").grid(row=8, column=0, padx=10, pady=5, sticky="w")
pvtech_choice = ttk.Combobox(root, values=["crystSi", "CIS", "CdTe", "Unknown"], state="readonly")
pvtech_choice.grid(row=8, column=1, padx=10, pady=10)

tk.Label(root, text="Bifacial Gain (%)").grid(row=9, column=0, padx=10, pady=5, sticky="w")
bifacial_gain = tk.Entry(root)
bifacial_gain.grid(row=9, column=1, padx=10, pady=5)

#Hardware Specs Input
tk.Label(root, text="Average Load (KW)").grid(row=0, column=2, padx=10, pady=5, sticky="w")
annual_load = tk.Entry(root)
annual_load.grid(row=0, column=3, padx=10, pady=5)

tk.Label(root, text="Number of Batteries").grid(row=1, column=2, padx=10, pady=5, sticky="w")
battery_num = ttk.Combobox(root, values=[0, 2, 3, 4, 5, 6, 7, 8], state="readonly")
battery_num.grid(row=1, column=3, padx=10, pady=5)

tk.Label(root, text="Inverter Rate (KW)").grid(row=3, column=2, padx=10, pady=5, sticky="w")
inverter_rate = tk.Entry(root)
inverter_rate.grid(row=3, column=3, padx=10, pady=5)

tk.Label(root, text="Max Generator Output (KW)").grid(row=2, column=2, padx=10, pady=5, sticky="w")
generator_output = ttk.Combobox(root, values=[6, 8, 20, 35], state="readonly")
generator_output.grid(row=2, column=3, padx=10, pady=10)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=10, column=0, columnspan=2, pady=10)

# Output label
tk.Label(root, text="Annual Generator Runtime (H)").grid(row=8, column=2, padx=10, pady=5, sticky="w")
result_label = tk.Label(root, text="", justify="left")
result_label.grid(row=8, column=3, columnspan=2, padx=10, pady=10)

#default values
lat.insert(0, "55")
lon.insert(0, "-119")
peakpower.insert(0, "4.45")
loss.insert(0, "14")
angle.insert(0, "49")
aspect.insert(0, "-8")

annual_load.insert(0, "5")

inverter_rate.insert(0, "12")
bifacial_gain.insert(0, "0")
generator_output.current(0)

tracking.current(0)         # "Fixed"
mounting_place.current(1)   # "building"
pvtech_choice.current(0)    # "crystSi"
battery_num.current(3)

# Run app
root.mainloop()
