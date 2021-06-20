from librosa.feature import rms
import soundfile as sf
import numpy as np
import uuid
import os
import pathlib

def create_dir(path):
    if not pathlib.Path(path).exists():
        os.mkdir(path)
    return path
            
def snr(audio, noise):
    return 20 * np.log10(np.quantile(rms(audio), 0.9) / np.quantile(rms(0.005 * noise), 0.9))

def append_noise(audio, level=1):
    noise = np.random.uniform(low=-level, high=level, size=(len(audio),))
    return snr(audio, noise) * noise + audio

def create_new_file_with_noise(path, level):
    audio, samplerate = sf.read(path)
    
    file_parts = path.split('/')
    
    destiny_path = create_dir('/'.join(file_parts[:-1]) + '/noisy')
    destiny_path += '/{}-{}'.format(uuid.uuid1(), file_parts[-1])

    sf.write(destiny_path, append_noise(audio, level), samplerate)
    return destiny_path