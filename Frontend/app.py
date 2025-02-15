import streamlit as st  # Importing the Streamlit library
from streamlit_lottie import st_lottie
import json

# Load the Lottie animation from a local file
def load_lottie_file(filepath:str):
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

lottie_animation = load_lottie_file("E:\personal-news-bot\Frontend\chatbot-robot.json")

# Display and Place animation in the sidebar
with st.sidebar:
    st_lottie(lottie_animation, height=200, key="news_bot")  # ✅ Animation always visible

# Mock news dataset
news_data = {
    "Trending Topics": [
        "🚀 SpaceX successfully launches Starship test flight!",
        "🎤 Grammy Awards 2025: Biggest winners and surprises!",
        "💰 Bitcoin crosses $50,000 mark after market surge.",
    ],
    "Business News": [
        "📉 Stock market sees a major dip amid inflation fears.",
        "💼 Tesla announces expansion plans in Europe.",
        "🏦 Federal Reserve hints at possible interest rate cuts.",
    ],
    "Tech & Gaming": [
        "🎮 PlayStation 6 rumored to launch in 2026!",
        "📱 Apple unveils new AI-powered iPhone.",
        "💻 OpenAI releases ChatGPT-5 with groundbreaking features.",
    ],
    "Sports Updates": [
        "⚽ Messi scores a hat-trick in a stunning comeback match!",
        "🏀 NBA Finals: Lakers vs. Celtics showdown confirmed!",
        "🏏 Cricket World Cup 2025 schedule officially released.",
    ]
}

# Sidebar UI
st.sidebar.markdown("### 👋 Welcome!")
st.sidebar.write("I'm your Personal News Bot. Stay updated with the latest news! 📰✨")

st.sidebar.markdown("### 🔥 Quick Access")

# State for selected category
selected_category = None

if st.sidebar.button("🔥 Trending Topics"):
    selected_category = "Trending Topics"
elif st.sidebar.button("📈 Business News"):
    selected_category = "Business News"
elif st.sidebar.button("🎮 Tech & Gaming"):
    selected_category = "Tech & Gaming"
elif st.sidebar.button("⚽ Sports Updates"):
    selected_category = "Sports Updates"

# Display news if a category is selected
if selected_category:
    st.write(f"### {selected_category}")
    for news in news_data[selected_category]:
        st.write(f"- {news}")

 # Back button
    if st.button("⬅️ Back to Home"):
        st.experimental_rerun()  # Reset and go back

if st.button("🆕 New Chat"):
    st.session_state.messages = []  # Clear previous messages
    st.rerun()  # Refresh the app



# Set the title of the chat application with an emoji
st.title("🗞️ Personal News Bot 🤖")

# Initialize session state to store chat messages (only if not already present)
if "messages" not in st.session_state:
    st.session_state.messages = []  # Create an empty list to store chat history

# Loop through the stored messages and display them in the chat format
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # Display message based on user/assistant role
        st.markdown(message["content"])  # Show message content

# Chat input field (takes user input and triggers a response when entered)
if prompt := st.chat_input("Ask me anything about the latest news 📰..."):  # Waits for user input
    st.session_state.messages.append({"role": "user", "content": prompt})  # Store user input in chat history

    # Display the user message in the chat UI
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create an assistant response section
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # Placeholder for assistant response (currently empty)
        full_response = ""  # No backend processing yet (can be updated later)

    # Store assistant response in chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
