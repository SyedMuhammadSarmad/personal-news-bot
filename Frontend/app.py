import streamlit as st
import datetime
from streamlit_lottie import st_lottie
import json

# Load the Lottie animation from a local file
def load_lottie_file(filepath: str):
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

lottie_animation = load_lottie_file("chatbot-robot.json")

# Display animation in the sidebar
with st.sidebar:
    st_lottie(lottie_animation, height=200, key="news_bot")  # ✅ Animation always visible

# Sidebar Layout
st.sidebar.markdown("### 👋 Welcome!")
st.sidebar.write("I'm your Personal News Bot. Stay updated with the latest news! 📰✨")

# Main Page Layout
st.title("🗞️ Personal News Bot 🤖")
st.write("I'm here to keep you updated with the latest news. Just tell me what you're looking for!")

# User selects an option
search_option = st.radio("Choose your search method:", ["Search by Keyword", "Browse Topic Headlines"])

# Single "Continue" button to confirm selection
if st.button("Continue"):
    st.session_state.search_option = search_option  # Store selection
    st.rerun()  # Refresh page

# Use session state to persist choice
if "search_option" in st.session_state:
    search_option = st.session_state.search_option

    response_text = ""  # Initialize response text

    if search_option == "Search by Keyword":
        selected_country = st.selectbox("Select Country", ["US", "UK", "Canada", "India"])
        keyword = st.text_input("Enter a keyword to search")

        if st.button("Search"):
            if keyword:
                response_text = f"Here’s what I found for '{keyword}' in {selected_country} and {selected_language}. Hope this helps!"
                st.text_area("Assistant Response", response_text, height=100)
            else:
                st.warning("Oops! Please enter a keyword to search.")

    elif search_option == "Browse Topic Headlines":
        selected_country = st.selectbox("Select Country", ["US", "UK", "Canada", "India", "Pakistan", "France", "Spain", "Germany"])
        selected_topic = st.selectbox("Select Topic", [
            "Beauty", "Business", "Cryptocurrency", "Economy", "Education", "Entertainment", "Finance", "Gadgets", 
            "Lifestyle", "Markets", "Movies", "Music", "Politics", "Science", "Soccer", "Startup", "World", 
            "Technology", "Sports", "Gaming", "Health"
        ])
        selected_date = st.date_input("Select a date", min_value=datetime.date(2020, 1, 1), max_value=datetime.date(2025, 12, 31))

        if st.button("Search"):
            response_text = f"Here’s the latest news about {selected_topic} in {selected_country} and {selected_language}. Stay tuned!"
            st.text_area("Assistant Response", response_text, height=100)

    # Clear Chat Button
    if st.button("🧹 Clear Chat"):
        st.text_area("Assistant Response", "", height=100)

    # Back button to reset choice
    if st.button("⬅️ Back to Home"):
        st.session_state.search_option = None  # Reset selection
        st.rerun()  # Refresh to start over

else:
    st.warning("Select an option and press 'Continue' to proceed.")
