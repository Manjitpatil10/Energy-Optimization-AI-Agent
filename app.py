from google import genai
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Energy Optimization AI Agent",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Energy Optimization AI Agent")
st.sidebar.header("⚙️ Settings")

api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password"
)
client = None
if api_key:
    client = genai.Client(api_key=api_key)
st.write("Upload your electricity usage CSV file and analyze energy consumption.")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Data")
    st.dataframe(df)

    if "Daily_Energy_kWh" in df.columns:
        st.subheader("Energy Consumption Chart")

        fig, ax = plt.subplots()
        ax.bar(df["Device"], df["Daily_Energy_kWh"])
        ax.set_xlabel("Device")
        ax.set_ylabel("Daily Energy (kWh)")
        st.pyplot(fig)

        total = df["Daily_Energy_kWh"].sum()

        st.metric("Total Daily Energy", f"{total:.2f} kWh")
        rate = st.number_input(
    "Electricity Rate (₹ per kWh)",
    value=8.0
)

    monthly_units = total * 30
    monthly_bill = monthly_units * rate

    st.metric("Estimated Monthly Bill", f"₹ {monthly_bill:.2f}")
    co2 = monthly_units * 0.82

    st.metric(
    "Estimated Monthly CO₂",
    f"{co2:.2f} kg"
)
if client and st.button("🤖 Analyze with Gemini"):

    prompt = f"""
Analyze this energy usage data:

{df.to_string(index=False)}

Provide:
1. Summary
2. Highest consuming device
3. Saving tips
4. Final recommendation
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    st.subheader("AI Analysis")
    st.write(response.text)
else:
  st.error("CSV must contain a Daily_Energy_kWh column.")
