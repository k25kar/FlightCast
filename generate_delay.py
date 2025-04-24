import pandas as pd
import random
from datetime import datetime

origins=['DOH','DXB','JFK','LHR']
destinations=['DEL','CDG','SIN','HND']
weather_conditions=['Clear','Rain','Fog','Storm']
airlines=['Qatar Airways','Emirates','British Airways','Air India']
days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

data=[]
for _ in range(5000):  
    origin=random.choice(origins)
    dest=random.choice(destinations)
    dep_time=random.randint(0,23)
    weather=random.choices(weather_conditions,weights=[0.5,0.2,0.2,0.1])[0]
    airline=random.choice(airlines)
    duration=random.randint(2,15)*10
    day=random.choice(days)

    # Delay logic (improved)
    delayed='Yes' if (
        weather!='Clear' and random.random()>0.3
        or dep_time in range(0,6)
        or airline=='Air India' and random.random()>0.4
        or day in ['Friday','Sunday'] and random.random()>0.5
        or duration>900 and weather in ['Storm','Fog']
    ) else 'No'

    data.append([origin,dest,dep_time,weather,airline,duration,day,delayed])

df=pd.DataFrame(data,columns=['Origin','Dest','DepTime','Weather','Airline','Duration','Day','Delayed'])
df.to_csv('flight-delay-predictor/flights.csv',index=False)
print("Enhanced flight dataset generated at flight-delay-predictor/flights.csv")
