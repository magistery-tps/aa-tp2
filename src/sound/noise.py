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
    """
        Get signal-to-noise ratio.

        SRN = quantile 0.9 of audio energy / quantile 0.9 of noise energy
        
        Notes:
        - rms: Is the audio energy.
        - quantile(rms, 0.9): Compute rms 0.9 quantile. This allows as exclude audio or noise silence signals. 
        
        See: https://youtu.be/aruFMX7f3fk?t=2993
    """
    return rms_q_09(audio) / rms_q_09(noise)


def rms_q_09(audio): return np.quantile(rms(audio), 0.9)

def append_noise(original_audio, snr_ratio, level=0.001):
    '''
        Append noise base on oiginal audio SNR ratio.
    '''
    noise = np.random.uniform(
        low=-level, 
        high=level, 
        size=(len(original_audio),)
    )

    new_snr = snr(original_audio, noise) * snr_ratio

    desired_rms = (rms_q_09(noise) *10) ** (new_snr/20.0)

    noise = (desired_rms / rms_q_09(original_audio)) * noise

    return noise + original_audio

def create_new_file_with_noise(path, snr_ratio=1, level=0.001):
    audio, samplerate = sf.read(path)
    
    file_parts = path.split('/')
    
    destiny_path = create_dir('/'.join(file_parts[:-1]) + '/noisy')
    destiny_path += '/{}-{}'.format(uuid.uuid1(), file_parts[-1])

    sf.write(destiny_path, append_noise(audio, snr_ratio, level), samplerate)
    return destiny_path