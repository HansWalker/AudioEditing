import streamlit as st
import librosa
from pydub import AudioSegment
import librosa
import pyAudioAnalysis as paa
# Load audio
from sclib import SoundcloudAPI
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


def amplitude_scale(signal, scale_factor):
    """Scale the amplitude of the signal."""
    return signal * scale_factor

def run_model(params):

    # Load audio
    audio, sr = librosa.load("./Music/"+params['song'], dtype=np.float32)

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

    tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)

    stretch_rate = params['bpm'] / tempo

    audio = librosa.effects.time_stretch(audio, rate=stretch_rate)


    audio = librosa.effects.time_stretch(audio, rate=params['tempo']/100)

    return audio, sr

def mix(audio1, audio2, tempo1, tempo2,sr1,sr2):

    # Time stretch
    audio1 = librosa.effects.time_stretch(audio1, rate=tempo2/tempo1)
    audio2 = librosa.effects.time_stretch(audio2, rate=tempo1/tempo2)

    # Resample audio2
    audio2 = librosa.resample(audio2, orig_sr=sr2, target_sr=sr1)

    # Pad signals to equal length
    if len(audio1) < len(audio2):
        audio1 = np.pad(audio1, (0, len(audio2) - len(audio1)), 'constant')
    elif len(audio2) < len(audio1):
        audio2 = np.pad(audio2, (0, len(audio1) - len(audio2)), 'constant')

    # Combine signals
    mixed = audio1 + audio2

    return mixed


def run_app(
    starting = True):
    key = 0
    #st.set_page_config(layout="wide")

    tracks={}

    get_music()
    file_names = os.listdir('./Music')

    st.title('HIIT Music App')

    placeholder = st.empty()
    # Default values
    with placeholder.container():

        tempo = st.slider("Select Tempo", 20, 200, 100)  # Added slider with default value 120
        mood = st.selectbox("Select Mood", ["Happy", "Sad", "Angry", "Relaxed", "Romantic"]) # Added selectbox for rhythm
        bpm = st.slider("Select Beats Per Minute", 80, 180, 100) # Added slider for BPM
        song = st.selectbox("Select Song", file_names) # Added selectbox for song
        remix = st.checkbox("Remix Music")
        text=st.text_input('Type in name of playlist',value='My Playlist')

        #Parameters for second song
        if(remix):
            tempo2 = st.slider("Select Second Tempo", 20, 200, 100,key=key)  # Added slider with default value 120
            key+=1
            mood2 = st.selectbox("Select Second Mood", ["Happy", "Sad", "Angry", "Relaxed", "Romantic"],key=key) # Added selectbox for rhythm
            key+=1
            bpm2 = st.slider("Select Second Beats Per Minute", 80, 180, 100,key=key) # Added slider for BPM
            key+=1
            song2 = st.selectbox("Select Song", file_names,key=key) # Added selectbox for song
            key+=1
            
        duration = st.slider(label="Select Duration (minutes)", 
                            value=5,
                            min_value = 1,
                            max_value = 60,
                            step = 1,
                            key = 'slider') # Added slider with default value 60

        submit_button = st.button("Submit")
        key+=1
            

    if submit_button:
        starting = False
        placeholder.empty()
        params = {'tempo': tempo, 'mood': mood, 'bpm': bpm, 'duration': duration, 'song':song}
        if(remix):
            params2 = {'tempo': tempo2, 'mood': mood2, 'bpm': bpm2, 'duration': duration, 'song':song2}
        placeholder.write("Please wait while we generate your music...")
        audio, sr = run_model(params)
        if(remix):
            audio2, sr2 = run_model(params2)

        placeholder.empty()

        
        #file_name=st.selectbox("Select Music", file_list)
        st.write(f'Tempo: {tempo}')
        st.write(f'Rhythm: {mood}')
        st.write(f'Beats Per Minute: {bpm}')
        st.write(f'Duration: {duration} minutes')

        if(remix):
            st.write(f'Tempo: {tempo2}')
            st.write(f'Rhythm: {mood2}')
            st.write(f'Beats Per Minute: {bpm2}')
            st.write(f'Duration: {duration} minutes')
        if(remix):
            audio = mix(audio, audio2, tempo, tempo2,sr,sr2)
            st.audio(audio, start_time=0,sample_rate=sr)
        else:
            st.audio(audio, start_time=0,sample_rate=sr)
        
        generate_next = st.button("Generate Next Track", key=key)
        if(os.path.isdir(f'./{text}')):
            number_of_tracks = len(os.listdir(f'./{text}'))
        else:
            number_of_tracks = 0
            os.mkdir(f'./{text}')
        sf.write(f'./{text}/track{number_of_tracks}.wav',audio,sr)




run_app()