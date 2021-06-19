import soundfile as sf
from IPython.display import Audio
import numpy as np
import matplotlib.pyplot as plt

# Funciones para escuchar el audio de un ejemplo del dataset:

def play_audio(path, rate=None, show_signal=False):
    x, sr = sf.read(path)
    display(Audio(x, rate=sr))    
    if show_signal:
        time = np.arange(0,len(x)) / sr
        plt.plot(time,x)

def play(example):
    play_audio(example.file_path)