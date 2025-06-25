import pickle
import streamlit as st
import requests
import numpy as np

# Fetch movie poster from TMDb API
def fetch_movie_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Movie Recommender
def recommend_movie(movie):
    movie_index = movies_model[movies_model['title'] == movie].index[0]
    distances = sorted(list(enumerate(movies_similarity_scores[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies_model.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_movie_poster(movie_id))
        recommended_movie_names.append(movies_model.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Music Recommender
def recommend_music(music):
    music_index = musics_model[musics_model['title'] == music].index[0]
    distances = sorted(list(enumerate(musics_similarity_scores[music_index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    for i in distances[1:6]:
        recommended_music_names.append(musics_model.iloc[i[0]].title)
    return recommended_music_names

# Book Recommender with error handling
def recommend_book(books):
    if books not in books_model.index:
        st.warning("Selected book not found in recommendation model.")
        return []
    
    try:
        book_index = np.where(books_model.index == books)[0][0]
        distances = sorted(
            list(enumerate(books_similarity_scores[book_index])),
            key=lambda x: x[1],
            reverse=True
        )[1:6]

        recommended_book_names = []
        for i in distances:
            book_title = books_model.index[i[0]]
            temp_df = books_df[books_df['Book-Title'] == book_title].drop_duplicates('Book-Title')
            if not temp_df.empty:
                item = [
                    temp_df['Book-Title'].values[0],
                    temp_df['Book-Author'].values[0],
                    temp_df['Image-URL-M'].values[0]
                ]
                recommended_book_names.append(item)
        return recommended_book_names

    except Exception as e:
        st.error

# Streamlit UI
st.header('My Recommender')

# Load models
movies_model = pickle.load(open('movies_model.pkl', 'rb'))
movies_similarity_scores = pickle.load(open('movies_similarity_scores.pkl', 'rb'))

musics_model = pickle.load(open('musics_model.pkl', 'rb'))
musics_similarity_scores = pickle.load(open('musics_similarity_scores.pkl', 'rb'))

popular_df = pickle.load(open('popular.pkl', 'rb'))
books_model = pickle.load(open('books_model.pkl', 'rb'))
books_df = pickle.load(open('books_df.pkl', 'rb'))
books_similarity_scores = pickle.load(open('books_similarity_scores.pkl', 'rb'))

# Ensure books_model index is Book-Title
if 'Book-Title' in books_model.columns:
    books_model.set_index('Book-Title', inplace=True)

# User selection
selection_type = st.radio(
    "What do you want to recommend?",
    [":rainbow[Films] 🎬",":rainbow[Music] 🎵",":rainbow[Books] 📚"],
    captions=[
        "Get the popcorn.",
        "Feel the beat.",
        "Get lost in a new world."
    ],index=0
)

# Selection box
if selection_type == ":rainbow[Films] 🎬":
    movie_list = movies_model['title'].values
    selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
elif selection_type == ":rainbow[Music] 🎵":
    music_list = musics_model['title'].values
    selected_music = st.selectbox(
    "Type or select a music from the dropdown",
    music_list
)
elif selection_type == ":rainbow[Books] 📚":
    books_list = books_model.index.values
    selected_book = st.selectbox(
    "Type or select a book from the dropdown",
    books_list
)

    with st.expander("Show Top 50 Popular Books 📚"):
        for i in range(0, 50, 5):
            cols = st.columns(5)
            for j in range(5):
                if i + j < len(popular_df):
                    with cols[j]:
                        st.image(popular_df['Image-URL-M'].iloc[i + j], width=120)
                        st.text(popular_df['Book-Title'].iloc[i + j])
                        st.caption(popular_df['Book-Author'].iloc[i + j])

# Recommend on button click 
if st.button('Recommend'):
    if selection_type == ":rainbow[Films] 🎬":
        recommended_movie_names, recommended_movie_posters = recommend_movie(selected_movie)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])

    elif selection_type == ":rainbow[Music] 🎵":
        recommended_music_names = recommend_music(selected_music)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommended_music_names[i])

    elif selection_type == ":rainbow[Books] 📚":
        recommended_book_names = recommend_book(selected_book)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommended_book_names[i][0])  # Title
                st.text(recommended_book_names[i][1])  # Author
                st.image(recommended_book_names[i][2])  # Image