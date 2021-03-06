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
    def __init__(
        self, 
        path='.', 
        dataset_name='speech'
    ):
        self.dataset_path = '{}/{}'.format(path, dataset_name)
        download_audio_dataset(self.dataset_path, dataset_name)

    def get_all(self, with_feats=True):
        '''
        Devuelve todods los ejemplo del dataset.
        '''
        return self.search_by_pattern('Actor_*/*', with_feats)

    def search_by_pattern(self, filename_pattern, with_feats=True):
        '''
        Permite buscar ejemplos en el dataset usando un patro para el path del archivo.
        ''' 
        return self.search_by_paths(
            paths      = glob.glob('{}/{}.wav'.format(self.dataset_path, filename_pattern)), 
            with_feats = with_feats
        )
    
    def search_by_paths(self, paths, with_feats=True, feature_extract_fn=get_functional_feats):
        '''
        Devuelve una tabla donde cada ejemplo tiene como columnas todos los datos extraidos del
        nombre del archivo de audio y ademas todos los atributos extraido del audio con la 
        libreria opensmile.
        ''' 
        examples = []        
        for index in tqdm(range(len(paths))):
            
            try:
                file_path = paths[index]

                file_name_parts = self.__get_file_parts(file_path) 

                example = {
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
                    self.__append_feats(example, feature_extract_fn)

                examples.append(example)
            except:
                # print("Can't process {}!".format(file_path))
                pass

        return pd.DataFrame(examples).dropna()

    def __get_file_parts(self, file_path):
        filename       = Path(file_path).stem
        return filename.split('-')

    def __append_feats(self, example, feature_extract_fn):
        feats = feature_extract_fn(example['file_path'])
        for feat_col in feats.columns:
            example[feat_col] = feats[feat_col][0]