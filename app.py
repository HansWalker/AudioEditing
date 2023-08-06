
import streamlit as st
def run_app():
    st.set_page_config(layout="wide")

    st.title('HIIT Music App')

    # Default values
    tempo = st.slider("Select Tempo", 60, 200, 120)  # Added slider with default value 120
    rhythm = st.selectbox("Select Rhythm", ["steady", "other rhythms..."]) # Added selectbox for rhythm
    genre = st.selectbox("Select Genre", ['pop', 'rock', 'bhangra', 'reggaeton']) # Added selectbox for genre
    duration = st.slider("Select Duration (minutes)", 1, 60, 60) # Added slider with default value 60

    submit_button = st.button("Submit")
    user_input = st.text_input('Enter some text')

    if submit_button:
        st.write(f'Tempo: {tempo}')
        st.write(f'Rhythm: {rhythm}')
        st.write(f'Genre: {genre}')
        st.write(f'Duration: {duration} minutes')
        data = {"tempo": tempo, "rhythm": rhythm, "genre": genre, "duration": duration}
        response = requests.post("http://localhost:5000/send-data", json=data)
        st.write(response.json())

run_app()
