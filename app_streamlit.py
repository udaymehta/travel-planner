import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error(
        "Missing GOOGLE_API_KEY environment variable. Please set it in a .env file."
    )
    st.stop()

MODEL_NAME = "gemini-2.0-flash-001"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)


def calculate_num_days(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    return (end_date - start_date).days + 1


def generate_itinerary(location, start_date, end_date, interests, budget):
    num_days = calculate_num_days(start_date, end_date)
    budget_prompt = f"The traveler has a {budget} budget." if budget else ""

    prompt = f"""
    Create a detailed daily itinerary for a {num_days}-day trip to {location} from {start_date} to {end_date}. 🛫🌍
    The traveler is interested in: {interests}. 🎭🎨🍽️
    {budget_prompt}
    Provide a day-by-day breakdown with specific activities, suggested times (using a 24-hour clock), and brief descriptions. 🕰️ Include realistic travel times between activities where appropriate.
    If a specific date falls on a day of the week where some attractions might be closed, make a note of that and suggest alternatives. 🚦
    Format the itinerary clearly and concisely using Markdown with relevant emojis to make it engaging. 😊
    DO NOT provide any extra or unrelated information beyond the request. 🔒
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating itinerary: {e}"


st.set_page_config(
    page_title="Travel Itinerary Planner", page_icon="✈️", layout="centered"
)

st.title("🌍 Travel Itinerary Generator ✈️")
st.write(
    "Plan your next adventure with a detailed itinerary tailored to your preferences! 🗺️"
)

location = st.text_input("📍 Enter your destination:")
start_date = st.date_input("📅 Select your start date:", min_value=datetime.today())
end_date = st.date_input("📅 Select your end date:", min_value=start_date)
interests = st.text_input("🎭 Enter your interests (comma-separated):")
budget = st.selectbox("💰 Select your budget:", ["Low", "Mid", "High"])

if st.button("🚀 Generate Itinerary"):
    if not location or not interests:
        st.error("Please fill in all required fields.")
    elif (
        calculate_num_days(
            start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
        )
        <= 0
    ):
        st.error("End date must be after start date.")
    else:
        with st.spinner("✨ Generating itinerary... ✨"):
            itinerary = generate_itinerary(
                location,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
                interests,
                budget,
            )
        st.markdown("## 🌟 Your Itinerary:")
        st.markdown(itinerary)
