import pickle

# Load model and encoders
model=pickle.load(open('flight-delay-predictor/model/flight_model.pkl','rb'))
le_origin,le_dest,le_weather,le_airline,le_day=pickle.load(open('flight-delay-predictor/model/encoders.pkl','rb'))

# Get user input
origin=input("Enter origin airport code (e.g., DOH): ").strip().upper()
dest=input("Enter destination airport code (e.g., DEL): ").strip().upper()
dep_time=int(input("Enter departure hour (0-23): "))
weather=input("Enter weather condition (Clear, Rain, Fog, Storm, Snow): ").strip().title()
airline=input("Enter airline name (e.g., Qatar Airways): ").strip()
duration=int(input("Enter duration in minutes (e.g., 180): "))
day=input("Enter day of week (e.g., Monday): ").strip().title()

try:
    origin_encoded=le_origin.transform([origin])[0]
    dest_encoded=le_dest.transform([dest])[0]
    weather_encoded=le_weather.transform([weather])[0]
    airline_encoded=le_airline.transform([airline])[0]
    day_encoded=le_day.transform([day])[0]
except ValueError as e:
    print(f"\nInvalid input: {e}")
    exit()

# Prepare feature vector
features=[[origin_encoded,dest_encoded,dep_time,weather_encoded,airline_encoded,duration,day_encoded]]
prediction=model.predict(features)[0]

print("\nPrediction:", "Likely Delayed" if prediction else "On Time")
