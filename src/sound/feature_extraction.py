import soundfile as sf
import opensmile
import matplotlib.pyplot as plt

# Funciones para extraccion de features de los archivos de audio:

def get_lld_feats(file_path):
    '''
    Devuelve los atributos de bajo nivel (LLD) de un audio.
    '''
    smile = opensmile.Smile(
        feature_set   = opensmile.FeatureSet.eGeMAPSv02,
        feature_level = opensmile.FeatureLevel.LowLevelDescriptors,
    )
    feats = smile.process_file(file_path, channel=0)
    return feats.reset_index()


def get_functional_feats(file_path):
    '''
    Devuelve los atributos de alto nivel (Functionals) de un audio.
    
    Se calculan a partir de los atributos de bajo nivel, calculando estadísticas 
    que resuman las secuencias. Los modelos que vimos no modelan secuencias!, 
    por ende, es necesario disponer de atributos.
    que consistan de vectores fijos.
    '''
    smile = opensmile.Smile(
        feature_set   = opensmile.FeatureSet.eGeMAPSv02,
        feature_level = opensmile.FeatureLevel.Functionals,
    )
    feats = smile.process_file(file_path)
    return feats.reset_index()

def plot_feats(feats):
    feats_cols = [col for col in feats.columns if col not in ['file','start','end']]
    for col in feats_cols:
      plt.figure()
      plt.plot(feats.start.dt.total_seconds(),feats[col].values)
      plt.title(col)