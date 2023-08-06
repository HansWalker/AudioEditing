import streamlit as st
import librosa
import pydub
import mido
from pydub import AudioSegment
import librosa
import pyAudioAnalysis as paa
# Load audio
from sclib import SoundcloudAPI, Track, Playlist
import os
import numpy as np
import soundfile as sf

def get_music():

    # do not pass a Soundcloud client ID that did not come from this library, but you can save a client_id that this lib found and reuse it
    api = SoundcloudAPI()  
    playlist = api.resolve('https://soundcloud.com/hans-walker-54974308/sets/shalini_stuff')

    file_names=[]

    for track in playlist.tracks:
        filename = './Music'+f'/{track.title}.mp3'
        file_names.append(track.title)
        if(not os.path.isfile(filename)):
            with open(filename, 'wb+') as file:
                track.write_mp3_to(file)

    return file_names

def amplitude_scale(signal, scale_factor):
    """Scale the amplitude of the signal."""
    return signal * scale_factor

def run_model(params):

    # Load audio
    audio, sr = librosa.load("./Music/"+params['song']+".mp3", dtype=np.float32)

    # Remix audio for emotions using librosa's pitch shifting and time stretching functions
    if(params['mood']=='Happy'):
        audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=5)
        happy_mfcc = librosa.feature.mfcc(y=audio, sr=sr)
    if(params['mood']=='Sad'):
        audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=-5)
        sad_mfcc = librosa.feature.mfcc(y=audio, sr=sr)
    if(params['mood']=='Angry'):
        audio = amplitude_scale(audio, 5.0)
        angry_mfcc = librosa.feature.mfcc(y=audio, sr=sr)
    if(params['mood']=='Relaxed'):
        audio = librosa.effects.time_stretch(audio, rate=0.8)
        relaxed_mfcc = librosa.feature.mfcc(y=audio, sr=sr)
    if(params['mood']=='Romantic'):
        audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=3)
        romantic_mfcc = librosa.feature.mfcc(y=audio, sr=sr)

    audio = librosa.effects.time_stretch(audio, rate=params['tempo']/100)

    return audio, sr

    

def run_app():
    key = 0
    #st.set_page_config(layout="wide")

    file_names=get_music()

    st.title('HIIT Music App')

    placeholder = st.empty()
    # Default values
    with placeholder.container():

        tempo = st.slider("Select Tempo", 20, 200, 1)  # Added slider with default value 120
        mood = st.selectbox("Select Mood", ["Happy", "Sad", "Angry", "Relaxed", "Romantic"]) # Added selectbox for rhythm
        genre = st.selectbox("Select Genre", ['Pop', 'Rock', 'Bhangra', 'Reggaeton']) # Added selectbox for genre
        song = st.selectbox("Select Song", file_names) # Added selectbox for song
        duration = st.slider(label="Select Duration (minutes)", 
                            value=5,
                            min_value = 1,
                            max_value = 60,
                            step = 1,
                            key = 'slider') # Added slider with default value 60

        submit_button = st.button("Submit")

    if submit_button:
        placeholder.empty()
        params = {'tempo': tempo, 'mood': mood, 'genre': genre, 'duration': duration, 'song':song}
        placeholder.write("Please wait while we generate your music...")
        audio, sr = run_model(params)

        placeholder.empty()

        
        #file_name=st.selectbox("Select Music", file_list)
        st.audio(audio, start_time=0,sample_rate=sr)
        st.write(f'Tempo: {tempo}')
        st.write(f'Rhythm: {mood}')
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
                song = st.selectbox("Select Song", file_names) # Added selectbox for song
                key+=1
                duration = st.slider(label="Select Duration (minutes)", 
                                    min_value = 1,
                                    max_value = 60,
                                    step = 1,key=key) # Added slider with default value 60
                key+=1
                submit_button = st.button("Submit",key=key)
                key+=1



run_app()