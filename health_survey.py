import streamlit as st
import requests

# Raw URL for the exercises.json file
URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"

# Function to fetch exercise data from the JSON file
@st.cache_data
def fetch_exercise_data():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Raise error for bad responses
        return response.json()  # Parse JSON content
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data: {e}")
        return []

# Load exercise data
exercise_data = fetch_exercise_data()

# Sidebar Filters
st.sidebar.title("Filter Your Exercises")
goal = st.sidebar.selectbox("Select Your Fitness Goal", ["Strength", "Endurance", "Flexibility", "Weight Loss"])
equipment = st.sidebar.selectbox("Available Equipment", ["Body Only", "Barbell", "Dumbbell", "Kettlebell", "Resistance Band", "Machine"])
muscle_group = st.sidebar.selectbox("Target Muscle Group", ["Abdominals", "Chest", "Back", "Arms", "Legs", "Core", "Shoulders", "Full Body"])

# Main UI
st.title("Exercise Recommendations")
st.write("Based on your inputs, here are some exercises you can try:")

# Filter exercises based on user inputs
filtered_exercises = [
    exercise for exercise in exercise_data
    if goal.lower() in (exercise.get("category", "") or "").lower()  # Match category (e.g., "strength")
    and equipment.lower() in ((exercise.get("equipment", "") or "").lower())  # Safely handle None for equipment
    and muscle_group.lower() in [m.lower() for m in exercise.get("primaryMuscles", []) or []]  # Match primary muscles
]

if filtered_exercises:
    for exercise in filtered_exercises:
        st.subheader(exercise["name"])
        st.write(f"**Force:** {exercise.get('force', 'N/A')}")
        st.write(f"**Level:** {exercise.get('level', 'N/A')}")
        st.write(f"**Mechanic:** {exercise.get('mechanic', 'N/A')}")
        st.write(f"**Primary Muscles:** {', '.join(exercise.get('primaryMuscles', []))}")
        st.write(f"**Equipment:** {exercise.get('equipment', 'No equipment needed')}")
        st.write(f"**Instructions:**")
        for step in exercise.get("instructions", []):
            st.write(f"- {step}")
        if exercise.get("images"):
            for image in exercise["images"]:
                st.image(f"https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/{exercise['id']}/{image}")
else:
    st.write("No exercises found matching your criteria. Try adjusting your filters.")

# Footer
st.write("Note: Always consult a professional trainer before starting a new exercise routine.")
