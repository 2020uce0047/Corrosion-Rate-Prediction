# app.py

import streamlit as st
import joblib
import numpy as np

# Load the pre-trained model
model_filename = 'corrosion_rate_model.pkl'
loaded_model = joblib.load(model_filename)

default_values = {
    'mild': {'chloride_content': 0.1, 'temperature': 300.0, 'relative_humidity': 50.0},
    'moderate': {'chloride_content': 0.3, 'temperature': 310.0, 'relative_humidity': 60.0},
    'severe': {'chloride_content': 0.5, 'temperature': 320.0, 'relative_humidity': 70.0},
}

def main():
    st.title("Residual Strength")

    st.header("Enter the following parameters:")

    # Condition selection
    condition = st.selectbox("Choose the condition", ("mild", "moderate", "severe"))

    # Get default values based on condition
    defaults = default_values[condition]

    # Taking user inputs
    steel_diameter = st.number_input("Steel diameter (mm)", min_value=0)
    duration = st.number_input("Duration (years)", min_value=0.0, format="%.2f")
    wc_ratio = st.number_input("w/c ratio", min_value=0.0, format="%.2f")
    chloride_content = st.number_input("Chloride content (%)", min_value=0.0, value=defaults['chloride_content'], format="%.2f")
    temperature = st.number_input("Temperature (K)", min_value=0.0, value=defaults['temperature'], format="%.2f")
    relative_humidity = st.number_input("Relative humidity (%)", min_value=0.0, value=defaults['relative_humidity'], format="%.2f")
    

    # Make prediction and display the result
    if st.button("Submit"):
        chloride_diffusion_rate = chloride_content/duration
        mass_of_corroded_substance = np.exp(-duration)/(1+(wc_ratio/1 + wc_ratio))
        input_features = np.array([[steel_diameter, temperature, relative_humidity, duration, chloride_diffusion_rate, mass_of_corroded_substance]])
        corrosion_rate = loaded_model.predict(input_features)[0]
        corrosion_percent = 0.046*corrosion_rate*duration/steel_diameter
        reduction_residual_str = 0.5*corrosion_percent
        st.write(f"Degree of corrosion : {corrosion_percent:.2f}")
        st.write(f"Percentage reduction in strength : {reduction_residual_str:.2f}")

if __name__ == "__main__":
    main()
