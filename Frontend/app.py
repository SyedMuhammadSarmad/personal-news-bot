import streamlit as st
import datetime ,requests , json , pycountry
from streamlit_lottie import st_lottie
from pprint import pprint
from openai import OpenAI


def topic_headlines(country,topic,date):
  url = "https://google-news22.p.rapidapi.com/v1/topic-headlines"
  
  # Helper function to get country code
  def get_country_code(country_name):
    country = pycountry.countries.get(name=country_name)
    return country.alpha_2 if country else None

  querystring = {"country":get_country_code(country),"topic":topic,"language":"english","date":date,"limit":"20"}



  headers = {
  "x-rapidapi-key": st.secrets["api"]["rapidapi"],
  "x-rapidapi-host": "google-news22.p.rapidapi.com"
  }

  response = requests.get(url, headers=headers, params=querystring)

  response_json = response.json()

  if 'data' not in response_json:
    error = "Error: 'data' key not found in response. Response: {response_json}"
    return error

  # Filter
  filtered_data = [
    {
        "author": ", ".join(article.get("authors", ["Unknown"])),  # Join multiple authors
        "date": article.get("date", "Unknown"),
        "description": article.get("description", "No description available"),
        "title": article.get("title", "No title available"),
        "url": article.get("url", "No URL available"),
    }
    for article in response_json['data']
  ]

  # Convert to JSON
  result_json = json.dumps(filtered_data, indent=4)

  client = OpenAI(api_key = st.secrets["api"]["aimlapi"], base_url="https://api.aimlapi.com/v1") or OpenAI(api_key = st.secrets["api"]["openrouterapi"], base_url="https://openrouter.ai/api/v1")

  response = client.chat.completions.create(
    model="deepseek/deepseek-chat" or "deepseek/deepseek-chat:free",
    messages=[
        {"role": "system", "content": f"You are an AI news summarizer. Your task is to extract key information from the provided JSON news articles and filter them out according to the {country} and summarize them into clear, concise paragraphs with proper headings. Maintain an informative and neutral tone."},
        {"role": "user", "content": result_json},
    ],
    max_tokens=1500,
    stream=False,
  )

  return response.choices[0].message.content


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
                response_text = f"Here’s what I found for '{keyword}' in {selected_country}. Hope this helps!"
                st.text_area("Assistant Response", response_text, height=100)
            else:
                st.warning("Oops! Please enter a keyword to search.")

    elif search_option == "Browse Topic Headlines":
        selected_country = st.text_input("Enter your country")
        selected_topic = st.selectbox("Select Topic", [
            "Beauty", "Business", "Cryptocurrency", "Economy", "Education", "Entertainment", "Finance", "Gadgets", 
            "Lifestyle", "Markets", "Movies", "Music", "Politics", "Science", "Soccer", "Startup", "World", 
            "Technology", "Sports", "Gaming", "Health"
        ])
        selected_date = st.date_input("Select a date", min_value=datetime.date(2020, 1, 1), max_value=datetime.date(2025, 12, 31))

        if st.button("Search"):
            actual_response = topic_headlines(selected_country,selected_topic,selected_date)
            response_text = f"Here’s the latest news about {selected_topic} in {selected_country}.\n {actual_response} "
            with st.container():
                st.markdown("### Assistant Response")
                st.markdown(response_text)  
                st.markdown("Stay tuned! 📰✨")

    # Clear Chat Button
    if st.button("🧹 Clear Chat"):
        st.text_area("Assistant Response", "", height=100)

    # Back button to reset choice
    if st.button("⬅️ Back to Home"):
        st.session_state.search_option = None  # Reset selection
        st.rerun()  # Refresh to start over

else:
    st.warning("Select an option and press 'Continue' to proceed.")
