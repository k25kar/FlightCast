# FlightCast

This project provides a flight delay prediction model based on various input features such as origin, destination, weather conditions, airline, and departure time. It uses machine learning to predict whether a flight is likely to be on time or delayed.

## Requirements

Before running the application, ensure you have the following dependencies installed:

- Python 3.x
- Required Python libraries:
  - `tkinter` (for the GUI)
  - `pickle` (for loading pre-trained models)
  - `folium` (for map visualization)
  - `webbrowser`
  - `os`
  - `threading`
  - `sklearn` (for the machine learning model)
  - `pandas`

You can install the required libraries using pip:

```bash
pip install tkinter folium pandas scikit-learn

```
## Running the Application

1. Clone the repository:

   ```bash
   git clone https://github.com/k25kar/FlightCast.git
   cd FlightCast
2. Make sure that the necessary model and encoder files (flight_model.pkl, encoders.pkl) are present in the model/ directory.

3. Run the application:

``` bash
python app.py
```

The graphical user interface (GUI) will open. Fill in the required details like origin, destination, departure time, weather, airline, and duration.

Click the Predict button to get the flight delay prediction. The result will show the likelihood of the flight being on time or delayed.

# Notes

The model uses pre-trained data to make predictions, so ensure the necessary model files (flight_model.pkl and encoders.pkl) are available in the project directory.

The map visualization will open in your default browser showing the flight route between the origin and destination airports.
