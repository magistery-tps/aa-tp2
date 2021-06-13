# Aprendizaje Automatico - TP 2

* [Enunciado](https://github.com/magistery-tps/aa-tp2/blob/master/docs/Enunciado.pdf)

## Notebooks

* [consultar-datos](https://github.com/magistery-tps/aa-tp2/blob/master/notebooks/consultar-datos.ipynb)


## Instalacion

**Paso 1**: Descargar el repositorio.

```bash
$ git clone https://github.com/magistery-tps/aa-tp2.git
$ cd aa-tp1
```

**Paso 2**: Instalar [anaconda](https://www.anaconda.com/products/individual) (Necesario para instalar las dependencias del proyecto).

```bash
$ wget http://repo.continuum.io/archive/Anaconda3-5.0.0-Linux-x86_64.sh
$ sh Anaconda3-5.0.0-Linux-x86_64.sh
$ source ~/.bashrc  (o source ~/.zshrc)
```

**Paso 3**: Crear environment de dependencias para el proyecto (Parado en el directorio del proyecto).

```bash
$ conda env create -f environment.yml
```

**Nota**: Se peude [mamba](https://github.com/mamba-org/mamba) en vez de conda. Mamba es 100 veces mas rapido que conda.

```bash
$ conda install mamba
```

```bash
$ mamba env create -f environment.yml
```


## Actualizar dependencias

Si agregamos nuevas dependencias en `environment.yml` para instalarlas es necesario correr el siguiente comando:

```bash
$ conda env update -f environment.yml
```

## Comenzar a desarrollar

**Paso 1**: Activamos el entorno donde se encuentran instaladas las dependencias del proyecto.

```bash
$ activate aa-tp1
```

**Paso 2**: Sobre el directorio del proyecto levantamos jupyter lab.

```bash
$ jupyter lab

Jupyter Notebook 6.1.4 is running at:
http://localhost:8888/?token=45efe99607fa6......
```

**Paso 3**: Ir a http://localhost:8888.... como se indica en la consola.


## Tema Material Darker para Jupyter Lab

**Paso 1**: Instalar tema.
```bash
$ jupyter labextension install @oriolmirosa/jupyterlab_materialdarker
```

**Paso 2**: Reiniciar Jupyter Lab
