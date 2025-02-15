import streamlit as st
import datetime ,requests , json , pycountry
from streamlit_lottie import st_lottie
from openai import OpenAI


def topic_headlines(country,topic,date):
  url = "https://google-news22.p.rapidapi.com/v1/topic-headlines"
  
  # Helper function to get country code
  def get_country_code(country_name):
    country = pycountry.countries.get(name=country_name)
    return country.alpha_2 if country else None

  querystring = {"country":get_country_code(country),"topic":topic,"language":"english","date":date}



  headers = {
  "x-rapidapi-key":  st.secrets["api"]["rapidapi_a"],
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
    stream=False,
  )

  return response.choices[0].message.content

def search_by_keyword(country,keyword,from_date,to_date):

    def get_country_code(country_name):
        country = pycountry.countries.get(name=country_name)
        return country.alpha_2 if country else None
        
    url = "https://google-news22.p.rapidapi.com/v1/search" 

    querystring = {"q":keyword,"country":get_country_code(country),"language":"en","from":from_date,"to":to_date}

    headers = {
        "x-rapidapi-key": st.secrets["api"]["rapidapi_a"],
        "x-rapidapi-host": "google-news22.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    response_json = response.json()


    
    if 'data' not in response_json:
        error = "Error: 'data' key not found in response. Response: {response_json}"
        return error

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
    stream=False,
    )
    return response.choices[0].message.content





# Main Page Layout
st.markdown(
    """
    <style>
    .custom-title {
        text-align: center;
        background: linear-gradient(to right, #4CAF50, #FF5733); /* Replace with your desired gradient colors */
        -webkit-background-clip: text;
        color: transparent;
        font-size: 70px; /* Adjust the font size as needed */
        font-family: 'sans-serif'; /* Choose your preferred font family */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Applying the custom CSS class to the title
st.markdown('<h1 class="custom-title">AI News Assist</h1>', unsafe_allow_html=True)
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
        selected_country = st.text_input("Enter your country")
        keyword = st.text_input("Enter a keyword to search")

        from_selected_date = st.date_input("From date", min_value=datetime.date(2020, 1, 1), max_value=datetime.date(2025, 12, 31))
        to_selected_date = st.date_input("To date", min_value=from_selected_date, max_value=datetime.date(2025, 12, 31), key="to_date_picker"  )

        if st.button("Search"):
            if keyword:
                response_text = f"Here’s what I found for '{keyword}' in {selected_country}. \n {search_by_keyword(selected_country,keyword,from_selected_date,to_selected_date)} "
                with st.container():
                    st.markdown("### Assistant Response")
                    st.markdown(response_text)  
                    st.markdown("Stay tuned! 📰✨")

    elif search_option == "Browse Topic Headlines":
        selected_country = st.text_input("Enter your country")
        selected_topic = st.selectbox("Select Topic", [
            "Beauty", "Business", "Cryptocurrency", "Economy", "Education", "Entertainment", "Finance", "Gadgets", 
            "Lifestyle", "Markets", "Movies", "Music", "Politics", "Science", "Soccer", "Startup", "World", 
            "Technology", "Sports", "Gaming", "Health"
        ])
        selected_date = st.date_input("Select a date", min_value=datetime.date(2020, 1, 1), max_value=datetime.date(2025, 12, 31))

        if st.button("Search"):
            response_text = f"Here’s the latest news about {selected_topic} in {selected_country}.\n {topic_headlines(selected_country,selected_topic,selected_date)} "
            with st.container():
                st.markdown("### Assistant Response")
                st.markdown(response_text)  
                st.markdown("Stay tuned! 📰✨")

    # Clear Chat Button
    if st.button("Clear Chat"):
        st.text_area("Assistant Response", "", height=100)

    # Back button to reset choice
    if st.button("⬅️ Back to Home"):
        st.session_state.search_option = None  # Reset selection
        st.rerun()  # Refresh to start over
