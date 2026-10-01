import os
import joblib
import gradio as gr

loaded_model = joblib.load("model.pkl")
low, high = 40, 280   # <- replace with your printed quantile values

# ---- paste your build_input function here (plus any imports it needs, e.g. pandas) ----


def predict_demand(year, month, hour, weekday, holiday, weather, temp_c, humidity, wind):
    yr = 1 if year == "2012" else 0
    wd = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].index(weekday)
    wthr = ["Clear", "Mist/Cloudy", "Light Rain/Snow", "Heavy Rain/Snow"].index(weather) + 1
    row = build_input(yr, month, hour, wd, holiday, wthr, temp_c, humidity, wind)
    pred = int(round(loaded_model.predict(row)[0]))
    level = "Low" if pred < low else "High" if pred > high else "Medium"
    return f"{pred} bikes", level

app = gr.Interface(
    fn=predict_demand,
    inputs=[
        gr.Radio(["2011", "2012"], value="2012", label="Year"),
        gr.Slider(1, 12, value=7, step=1, label="Month"),
        gr.Slider(0, 23, value=8, step=1, label="Hour of day"),
        gr.Dropdown(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                    value="Tuesday", label="Weekday"),
        gr.Checkbox(label="Holiday"),
        gr.Dropdown(["Clear", "Mist/Cloudy", "Light Rain/Snow", "Heavy Rain/Snow"],
                    value="Clear", label="Weather"),
        gr.Slider(0, 41, value=25, label="Temperature (°C)"),
        gr.Slider(0, 100, value=50, label="Humidity (%)"),
        gr.Slider(0, 67, value=10, label="Wind speed (km/h)"),
    ],
    outputs=[gr.Textbox(label="Predicted Bike Demand"), gr.Textbox(label="Demand Level")],
    title="Bike Demand Prediction Application",
    description="Enter time and weather conditions to predict hourly bike rentals.",
    examples=[
        ["2012", 7, 8, "Tuesday", False, "Clear", 25, 50, 10],
        ["2012", 7, 3, "Tuesday", False, "Clear", 20, 60, 5],
        ["2012", 7, 12, "Saturday", False, "Clear", 32, 45, 8],
        ["2012", 7, 18, "Tuesday", False, "Light Rain/Snow", 20, 85, 20],
        ["2012", 1, 8, "Tuesday", False, "Clear", 3, 60, 15],
    ],
)

app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
