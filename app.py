import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Sales Call Logger", layout="wide")
st.title("📞 Sales Call Logger")

# --- Logging Section ---
st.subheader("📝 Log a New Call")

rep = st.selectbox("Rep Name", ["Doug", "Wes", "Ava"])
client = st.text_input("Client Name")
call_type = st.selectbox("Call Type", ["Intro", "Demo", "Follow-up"])
outcome = st.selectbox("Outcome", ["Interested", "Not Interested", "Pending"])
notes = st.text_area("Notes")

if st.button("Log Call"):
    new_call = {
        "Date": datetime.today().strftime("%Y-%m-%d"),
        "Rep Name": rep,
        "Client": client,
        "Call Type": call_type,
        "Outcome": outcome,
        "Notes": notes
    }

    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)

    # Load or create CSV
    try:
        df = pd.read_csv("data/sample_calls.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=new_call.keys())

    # Append and save
    df = pd.concat([df, pd.DataFrame([new_call])], ignore_index=True)
    df.to_csv("data/sample_calls.csv", index=False)

    st.success("✅ Call logged successfully!")

# --- Load Data ---
try:
    df = pd.read_csv("data/sample_calls.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Rep Name", "Client", "Call Type", "Outcome", "Notes"])

# --- Filtering Section ---
st.subheader("🔍 Filter Calls")

selected_rep = st.selectbox("Filter by Rep", ["All"] + sorted(df["Rep Name"].unique()))
selected_call_type = st.selectbox("Filter by Call Type", ["All"] + sorted(df["Call Type"].unique()))
selected_outcome = st.selectbox("Filter by Outcome", ["All"] + sorted(df["Outcome"].unique()))

filtered_df = df.copy()

if selected_rep != "All":
    filtered_df = filtered_df[filtered_df["Rep Name"] == selected_rep]
if selected_call_type != "All":
    filtered_df = filtered_df[filtered_df["Call Type"] == selected_call_type]
if selected_outcome != "All":
    filtered_df = filtered_df[filtered_df["Outcome"] == selected_outcome]

# --- Display Filtered Data ---
st.subheader("📋 Filtered Call Log")
st.dataframe(filtered_df)

# --- Summary Tables ---
st.subheader("📊 Summary by Rep and Call Type")
summary_type = filtered_df.groupby(["Rep Name", "Call Type"]).size().unstack(fill_value=0)
st.dataframe(summary_type)

st.subheader("📊 Summary by Rep and Outcome")
summary_outcome = filtered_df.groupby(["Rep Name", "Outcome"]).size().unstack(fill_value=0)
st.dataframe(summary_outcome)
