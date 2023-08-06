import streamlit as st
import librosa
#generate the music
def run_model():
    return librosa.load('TheFatRat, Anjulie - Close To The Sun.mp3', sr=48000)[0]

def run_app():
    key = 0
    st.set_page_config(layout="wide")

    st.title('HIIT Music App')

    placeholder = st.empty()
    # Default values
    with placeholder.container():
        tempo = st.slider("Select Tempo", 60, 200, 120)  # Added slider with default value 120
        rhythm = st.selectbox("Select Rhythm", ["Steady", "Other Rhythms..."]) # Added selectbox for rhythm
        genre = st.selectbox("Select Genre", ['Pop', 'Rock', 'Bhangra', 'Reggaeton']) # Added selectbox for genre
        duration = st.slider(label="Select Duration (minutes)", 
                            value=5,
                            min_value = 1,
                            max_value = 60,
                            step = 1,
                            key = 'slider') # Added slider with default value 60

        submit_button = st.button("Submit")

    if submit_button:
        placeholder.empty()
        placeholder.write("Please wait while we generate your music...")
        sound_file = run_model()
        placeholder.empty()
        st.audio(sound_file, start_time=0, sample_rate=48000)
        st.write(f'Tempo: {tempo}')
        st.write(f'Rhythm: {rhythm}')
        st.write(f'Genre: {genre}')
        st.write(f'Duration: {duration} minutes')

        regenerate_button = st.button("Generate New Music", key=key)
        key += 1

        if regenerate_button:
            with placeholder.container():
                tempo = st.slider("Select Tempo", 60, 200, 120, key=key)  # Added slider with default value 120
                key+=1
                rhythm = st.selectbox("Select Rhythm", ["Steady", "other rhythms..."], key=key) # Added selectbox for rhythm
                key+=1
                genre = st.selectbox("Select Genre", ['pop', 'rock', 'bhangra', 'reggaeton'], key=key) # Added selectbox for genre
                key+=1
                duration = st.slider(label="Select Duration (minutes)", 
                                    min_value = 1,
                                    max_value = 60,
                                    step = 1,key=key) # Added slider with default value 60
                key+=1
                submit_button = st.button("Submit",key=key)
                key+=1



import inspect

run_app()