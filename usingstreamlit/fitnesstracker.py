import streamlit as st
import pandas as pd
import os

# File for saving data
DATA_FILE = "workouts.csv"

# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Exercise Type", "Duration (min)", "Calories Burned"])

# Save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Load workouts
workouts = load_data()

# Streamlit UI
st.title("🏋️ Personal Fitness Tracker")

# Form for new workout entry
with st.form("add_workout"):
    date = st.date_input("Date")
    exercise_type = st.text_input("Exercise Type")
    duration = st.number_input("Duration (min)", min_value=1, step=1)
    calories_burned = st.number_input("Calories Burned", min_value=1, step=1)
    submit = st.form_submit_button("Add Workout")

    if submit:
        new_data = pd.DataFrame([[date, exercise_type, duration, calories_burned]],
                                columns=["Date", "Exercise Type", "Duration (min)", "Calories Burned"])
        workouts = pd.concat([workouts, new_data], ignore_index=True)
        save_data(workouts)
        st.success("Workout Added Successfully!")

# Display workouts
st.subheader("📜 Workout History")
if not workouts.empty:
    st.dataframe(workouts)

    # Delete option
    if st.button("Clear All Workouts"):
        workouts = pd.DataFrame(columns=["Date", "Exercise Type", "Duration (min)", "Calories Burned"])
        save_data(workouts)
        st.warning("All workouts deleted!")
else:
    st.info("No workouts recorded yet.")

# Statistics
if not workouts.empty:
    st.subheader("📊 Workout Statistics")
    total_workouts = len(workouts)
    total_duration = workouts["Duration (min)"].sum()
    total_calories = workouts["Calories Burned"].sum()
    avg_duration = total_duration / total_workouts if total_workouts else 0

    st.write(f"**Total Workouts:** {total_workouts}")
    st.write(f"**Total Duration:** {total_duration} minutes")
    st.write(f"**Total Calories Burned:** {total_calories} kcal")
    st.write(f"**Average Duration per Workout:** {avg_duration:.2f} minutes")
