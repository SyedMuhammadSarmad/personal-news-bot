import streamlit as st
import datetime
from streamlit_lottie import st_lottie
import json

# Load the Lottie animation from a local file
def load_lottie_file(filepath: str):
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

lottie_animation = load_lottie_file("chatbot-robot.json")

# Display and place animation in the sidebar
with st.sidebar:
    st_lottie(lottie_animation, height=200, key="news_bot")  # ✅ Animation always visible

# Sidebar Layout
st.sidebar.markdown("### 👋 Welcome!")
st.sidebar.write("I'm your Personal News Bot. Stay updated with the latest news! 📰✨")

# Main Page Layout
st.title("🗞️ Personal News Bot 🤖")
st.write("I'm here to keep you updated with the latest news. Just tell me what you're looking for!")

# Creating Buttons for Option Selection
search_option = None

if st.button("Search specific Keyword"):

    search_option = "Search by Keyword"
    st.session_state.search_option = search_option  # Storing the option in session state

elif st.button("Browse Different Topic Headlines"):

    search_option = "Search by Topic"
    st.session_state.search_option = search_option  # Storing the option in session state

# Use the session state to persist the selected option
if 'search_option' in st.session_state:
    search_option = st.session_state.search_option

    response_text = ""  # Initialize response text outside the search blocks

    # Conditional form based on selected option
    if search_option == "Search by Keyword":
        # Input Fields for Keyword Search
        selected_country = st.selectbox("Select Country", ["US", "UK", "Canada", "India"])
        selected_language = st.selectbox("Select Language", ["English", "Spanish", "French", "German"])
        keyword = st.text_input("Enter a keyword to search")

        # Display response after pressing Search button
        if st.button("Search"):
            if keyword:  # Check if a keyword is entered
                response_text = f"Here’s what I found for '{keyword}' in {selected_country} and {selected_language}. Hope this helps!"
                st.text_area("Assistant Response", response_text, height=100)  # Display response in the text area below
            else:
                st.warning("Oops! Please enter a keyword to search.")

    elif search_option == "Search by Topic":
        # Input Fields for Topic Search
        selected_country = st.selectbox("Select Country", ["US", "UK", "Canada", "India","Pakistan","France","Spain","Germany"])
        selected_topic = st.selectbox("Select Topic", ["Beauty","Business","CryptoCuurency","Economy","Education","Entertainment","Finance","Gadgets","Lifestyle",
                                                       "Markets","Movies","Music","Politics","Science","Soccer","Startup","World","Technology", "Sports", "Gaming", "Health"])
        
        selected_language = st.selectbox("Select Language", ["English", "Spanish", "French", "German"])

        # Date selection for Topic Search
        selected_date = st.date_input("Select a date", min_value=datetime.date(2020, 1, 1), max_value=datetime.date(2025, 12, 31))


        # Display response after pressing Search button
        if st.button("Search"):
            response_text = f"Here’s the latest news about {selected_topic} in {selected_country} and {selected_language}. Stay tuned!"
            st.text_area("Assistant Response", response_text, height=100)  # Display response in the text area below

   # Clear Chat Button with Smooth Interaction
    if st.button("🧹 Clear Chat"):
        st.text_area("Assistant Response", "", height=100)
        
    # Back button to reset and go back to the initial state
    if st.button("⬅️ Back to Home"):
        st.session_state.search_option = None  # Reset the search option
        st.rerun()  # Reset and go back

else:
    st.warning("I'm ready to assist you! Just pick an option to continue")
