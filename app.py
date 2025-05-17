import streamlit as st
import pickle
import requests

# API setup
API_KEY = '28cf36de7674dfe275bd66d5a68e33b3'

# Load data
new_df = pickle.load(open('movies.pkl', 'rb'))
similar = pickle.load(open('similar.pkl', 'rb'))

movie_titles = new_df['title'].values


# Get poster from TMDb
def fetch_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        'api_key': API_KEY,
        'query': movie_title
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = data.get('results')
    if results and len(results) > 0:
        poster_path = results[0].get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

    return "https://via.placeholder.com/300x450?text=No+Image"


# Recommend movies
def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similar[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        title = new_df.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))
    return recommended_movies, recommended_posters


# UI
st.title('🎬 Movie Recommender System')

option = st.selectbox(
    "Select a movie to get recommendations:",
    movie_titles,
    key="movie_selector"
)

if st.button("Recommend"):
    recommendations, posters = recommend(option)
    cols = st.columns(len(recommendations))
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.caption(recommendations[idx])
