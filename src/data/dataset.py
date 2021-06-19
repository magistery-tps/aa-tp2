import os
from pathlib import Path
import tqdm
import glob
import pandas as pd
import numpy as np
from tqdm import tqdm
import subprocess

from sound import get_functional_feats

def download_audio_dataset(path, dataset_name):
    '''
    Descarga el dataset y los descomprime en el path pasado como parametro.
    '''
    if os.path.exists(path):
        print('Dataset alredy downloaded!')
        return

    filename = 'Audio_{}_Actors_01-24.zip'.format(dataset_name.capitalize())
    url = 'https://zenodo.org/record/1188976/files/{}'.format(filename)

    print('Download {} dataset...'.format(url))
    subprocess.run(["wget", url])    
    subprocess.run(["unzip", filename, "-d", path])
    subprocess.run(["rm", filename, "-d", filename])

class Dataset:
    def __init__(self, path='.', dataset_name='speech'):
        self.dataset_path = '{}/{}'.format(path, dataset_name)
        download_audio_dataset(self.dataset_path, dataset_name)

    def get_all(self, with_feats=True):
        '''
        Usa el metodo de busqueda search_by para consultar todos lo ejemplos del dataset.
        '''
        return self.search_by('Actor_*', '*', with_feats)

    def search_by(self, actor_pattern, filename_pattern, with_feats=True):
        '''
        Permite buscar ejemplos en el dataset buscando con un patro por artista y otro patro 
        para el nombre del archivo. 
        
        Devuelve una tabla donde cada ejemplo tiene como columnas todos los datos extraidos del
        nombre del archivo de audio y ademas todos los atributos extraido del audio con la 
        libreria opensmile.
        ''' 
        search_path = '{}/{}/{}.wav'.format(self.dataset_path, actor_pattern, filename_pattern)
        result_file_paths = glob.glob(search_path)

        examples = []        
        for index in tqdm(range(len(result_file_paths))):
            file_path = result_file_paths[index]

            file_name_parts = self.__get_file_parts(file_path) 
 
            example = {
                'actor'              : self.__get_actor_number_from(file_path),
                'file_path'          : file_path,
                'modality'           : file_name_parts[0],
                'vocal_channel'      : file_name_parts[1],
                'emotion'            : file_name_parts[2],
                'emotional_intensity': file_name_parts[3],
                'statement'          : file_name_parts[4],
                'repetition'         : file_name_parts[5],
                'actor'              : file_name_parts[6]
            }
            if with_feats:
                self.__append_feats(example)
            
            examples.append(example)

        return pd.DataFrame(examples)

    
    def __get_actor_number_from(self, path):
        actor_part = path.replace(self.dataset_path, '') .split('/')[1]
        return int(actor_part.split('_')[1])
    
    def __get_file_parts(self, file_path):
        filename       = Path(file_path).stem
        return filename.split('-')
    
    def __append_feats(self, example):
        feats = get_functional_feats(example['file_path'])            
        for feat_col in feats.columns:
            example[feat_col] = feats[feat_col][0]