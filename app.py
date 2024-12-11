import pickle
import streamlit as st
import requests

def fetch_movie_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend_movie(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_movie_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

def recommend_music(musics):
    music_index = music[music['title'] == musics].index[0]
    distances = sorted(list(enumerate(similarity1[music_index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    for i in distances[1:6]:
        recommended_music_names.append(music.iloc[i[0]].title)
    return recommended_music_names

# Streamlit UI
st.header('My Recommender')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
music = pickle.load(open('music_list.pkl', 'rb'))
similarity1 = pickle.load(open('similarity1.pkl', 'rb'))

selection_type = st.radio(
    "What do you want to recommend?",
    ["Films:movie_camera:",":rainbow[Music]"],
    captions=[
        "Get the popcorn.",
        "Feel the beat."
    ],index=0
)

if selection_type == "Films:movie_camera:":
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
elif selection_type == ":rainbow[Music]":
    music_list = music['title'].values
    selected_music = st.selectbox(
    "Type or select a music from the dropdown",
    music_list
)
    
if st.button('Recommend'):
    if selection_type == "Films:movie_camera:":
        recommended_movie_names, recommended_movie_posters = recommend_movie(selected_movie)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])

    elif selection_type == ":rainbow[Music]":
        recommended_music_names = recommend_music(selected_music)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommended_music_names[i])