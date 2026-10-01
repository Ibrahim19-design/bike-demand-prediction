import streamlit as st
import joblib

@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

loaded_model = load_model()

low, high = 40, 280   # <- put YOUR real low, high values here

# ---- paste your build_input function here (plus any imports it needs) ----


st.title("Bike Demand Prediction Application")
st.write("Enter time and weather conditions to predict hourly bike rentals.")

weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
weathers = ["Clear", "Mist/Cloudy", "Light Rain/Snow", "Heavy Rain/Snow"]

year = st.radio("Year", ["2011", "2012"], index=1, horizontal=True)
month = st.slider("Month", 1, 12, 7)
hour = st.slider("Hour of day", 0, 23, 8)
weekday = st.selectbox("Weekday", weekdays, index=2)
holiday = st.checkbox("Holiday")
weather = st.selectbox("Weather", weathers)
temp_c = st.slider("Temperature (°C)", 0, 41, 25)
humidity = st.slider("Humidity (%)", 0, 100, 50)
wind = st.slider("Wind speed (km/h)", 0, 67, 10)

if st.button("Predict"):
    yr = 1 if year == "2012" else 0
    wd = weekdays.index(weekday)
    wthr = weathers.index(weather) + 1
    row = build_input(yr, month, hour, wd, holiday, wthr, temp_c, humidity, wind)
    pred = int(round(loaded_model.predict(row)[0]))
    level = "Low" if pred < low else "High" if pred > high else "Medium"
    st.success(f"Predicted Bike Demand: {pred} bikes")
    st.info(f"Demand Level: {level}")
