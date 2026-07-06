import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Energy Optimization AI Agent",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Energy Optimization AI Agent")
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
    else:
        st.error("CSV must contain a 'Daily_Energy_kWh' column.")
