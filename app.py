import tkinter as tk
from tkinter import messagebox
import pickle
import folium
import webbrowser
import os
import threading
from tkinter import ttk

# Load model and encoders
model = pickle.load(open('flight_model.pkl', 'rb'))
le_origin, le_dest, le_weather, le_airline, le_day = pickle.load(open('encoders.pkl', 'rb'))

# Coordinates for airport codes
coordinates = {
    'DOH': (25.276987, 51.520008),
    'DXB': (25.276987, 55.296249),
    'JFK': (40.641311, -73.778139),
    'LHR': (51.507222, -0.1275),
    'DEL': (28.6139, 77.2090),
    'CDG': (48.8566, 2.3522),
    'SIN': (1.290270, 103.851959),
    'HND': (35.652832, 139.839478)
}

def show_map(origin, dest):
    coords_origin = coordinates.get(origin)
    coords_dest = coordinates.get(dest)
    if coords_origin and coords_dest:
        m = folium.Map(location=coords_origin, zoom_start=4)
        folium.Marker(coords_origin, popup=f"Origin: {origin}").add_to(m)
        folium.Marker(coords_dest, popup=f"Destination: {dest}").add_to(m)
        folium.PolyLine([coords_origin, coords_dest], color="blue", weight=3).add_to(m)
        map_file = 'flight_map.html'
        m.save(map_file)
        webbrowser.open('file://' + os.path.realpath(map_file))
    else:
        messagebox.showerror("Map Error", "Could not find coordinates for selected airports.")

def predict_delay_threaded():
    spinner.start()
    threading.Thread(target=predict_delay).start()

def predict_delay():
    try:
        origin=origin_var.get()
        dest=dest_var.get()
        dep_time=int(dep_time_entry.get())
        weather=weather_var.get()
        airline=airline_entry.get()
        duration=int(duration_entry.get())
        day=day_var.get()

        features=[[
            le_origin.transform([origin])[0],
            le_dest.transform([dest])[0],
            dep_time,
            le_weather.transform([weather])[0],
            le_airline.transform([airline])[0],
            duration,
            le_day.transform([day])[0]
        ]]

        prediction=model.predict(features)[0]
        result_text="ON TIME" if prediction==0 else "LIKELY DELAYED"

        detail_msg=f"✈️ Flight Status: {result_text}\n\n" \
                   f"• Origin: {origin}\n" \
                   f"• Destination: {dest}\n" \
                   f"• Departure Time: {dep_time}:00\n" \
                   f"• Airline: {airline}\n" \
                   f"• Duration: {duration} min\n" \
                   f"• Weather: {weather}\n" \
                   f"• Day: {day}"

        messagebox.showinfo("Prediction Result", detail_msg)
        show_map(origin,dest)

    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))

origin_options = ['DOH', 'DXB', 'JFK', 'LHR']
dest_options = ['DEL', 'CDG', 'SIN', 'HND']

# GUI setup
root = tk.Tk()
root.title("Flight Delay Predictor")
root.geometry("500x590")
root.configure(bg="#212529")

header = tk.Label(root, text="Flight Delay Predictor", font=("Helvetica", 16, "bold"), fg="#f8f9fa", bg="#212529")
header.pack(pady=15)

def styled_option(label_text, variable, options):
    label = tk.Label(root, text=label_text, bg="#212529", fg="white", font=("Helvetica", 10, "bold"))
    label.pack(pady=(8, 2))
    menu = tk.OptionMenu(root, variable, *options)
    menu.config(bg="#343a40", fg="white", font=("Helvetica", 9), width=18, highlightthickness=0, relief="flat")
    menu["menu"].config(bg="#343a40", fg="white")
    menu.pack()
    return menu

def styled_entry(label_text):
    label = tk.Label(root, text=label_text, bg="#212529", fg="white", font=("Helvetica", 10, "bold"))
    label.pack(pady=(8, 2))
    entry = tk.Entry(root, font=("Helvetica", 9), width=22, bg="#343a40", fg="white", insertbackground="white")
    entry.pack()
    return entry

# Create variables after root is initialized
origin_var = tk.StringVar(value='DOH')
dest_var = tk.StringVar(value='DEL')
weather_var = tk.StringVar(value='Clear')
day_var = tk.StringVar(value='Monday')

# Dropdowns
origin_menu = styled_option("Origin Airport", origin_var, [k for k in coordinates if k != 'DEL'])
dest_menu = styled_option("Destination Airport", dest_var, [k for k in coordinates if k != 'DOH'])

# Input Fields
dep_time_entry = styled_entry("Departure Hour (0–23)")
styled_option("Weather Condition", weather_var, ['Clear', 'Rain', 'Fog', 'Storm'])
airline_entry = styled_entry("Airline (Qatar Airways | Emirates | British Airways | Air India)")
duration_entry = styled_entry("Duration (in minutes)")
styled_option("Day of the Week", day_var, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

# Destination list updates when origin changes and vice versa
def update_dest_options(*args):
    origin = origin_var.get()
    dest_menu['menu'].delete(0, 'end')
    for airport in dest_options:
        dest_menu['menu'].add_command(label=airport, command=tk._setit(dest_var, airport))
    if dest_var.get() not in dest_options:
        dest_var.set(dest_options[0])

def update_origin_options(*args):
    dest = dest_var.get()
    origin_menu['menu'].delete(0, 'end')
    for airport in origin_options:
        origin_menu['menu'].add_command(label=airport, command=tk._setit(origin_var, airport))
    if origin_var.get() not in origin_options:
        origin_var.set(origin_options[0])

origin_var.trace_add('write', update_dest_options)
dest_var.trace_add('write', update_origin_options)

# Predict Button
predict_btn = tk.Button(root, text="Predict", font=("Helvetica", 11, "bold"),
                        bg="#28a745", fg="white", padx=15, pady=4, command=predict_delay_threaded)
predict_btn.pack(pady=(20, 10))

# Spinner
spinner = ttk.Progressbar(root, mode='indeterminate', length=180)
spinner.pack()

root.mainloop()
