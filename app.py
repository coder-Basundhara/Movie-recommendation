import streamlit as st
import pandas as pd
import requests
import pickle

# Load the processed data and similarity matrix
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    api_key = '190cc74fe879150743c14bd334857d3e'  # Replace with your TMDB API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return full_path

# Streamlit UI
st.title("Hey!Confused what to binge? Find your best match here!")
st.markdown("""
    <style>
    /* Elegant orangish gradient background */
    .stApp {
        background: linear-gradient(to bottom, #cba6f7, #8e2de2, #4a00e0);
    background-attachment: fixed;
    }

    /* Set modern font and text color */
    html, body, [class*="css"] {
        font-family: 'Helvetica Neue', sans-serif;
        color: #333333;
    }

    /* Custom title styling */
    h1 {
        text-align: center;
        color: #b3541e;
        font-size: 3em;
        font-weight: 700;
        margin-bottom: 0.5em;
    }

    /* Button styling */
    div.stButton > button {
        background-color: #ff7e5f;
        color: white;
        padding: 0.6em 1.2em;
        font-size: 1.1em;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        transition: background 0.3s ease;
    }

    div.stButton > button:hover {
        background-color: #feb47b;
        color: white;
    }

    /* Styling for movie titles below posters */
    .element-container > div > div > div > div {
        text-align: center;
        font-weight: 600;
        color: #6e2c00;
    }

    /* Image box hover effect */
    img {
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("<label style='color:white; font-size:18px;'>Choose your favs!</label>", unsafe_allow_html=True)
selected_movie = st.selectbox("", movies['title'].values)


if st.button('Recommend'):
    recommendations = get_recommendations(selected_movie)
    st.markdown("<p style='color:white; font-size:18px;'>Voila! here you go!</p>", unsafe_allow_html=True)


    # Create a 2x5 grid layout
    for i in range(0, 10, 5):  # Loop over rows (2 rows, 5 movies each)
        cols = st.columns(5)  # Create 5 columns for each row
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']
                poster_url = fetch_poster(movie_id)
                with col:
                    st.image(poster_url, width=130)
                    st.markdown(f"<p style='color:white; text-align:center; font-weight:500;'>{movie_title}</p>", unsafe_allow_html=True)
