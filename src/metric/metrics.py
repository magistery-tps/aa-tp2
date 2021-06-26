import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score
import itertools

def show_cv_score(model, X, y, cv, groups=None, scoring='accuracy', n_jobs=24):
    scores = cross_val_score(model, X, y, scoring=scoring, cv=cv, n_jobs=n_jobs, groups=groups)
    print('Accuracy: {:.4f} %'.format(np.mean(scores * 100)))
    return model

def show_summary(model, X, y_true, labels=None):
    y_pred = model.predict(X)

    print('Accuracy: {:.4f} %\n'.format(accuracy_score(y_true, y_pred) * 100))
    print('Classification Report:')
    print(classification_report(y_true, y_pred, target_names=labels))
    plot_confusion_matrix(y_true, y_pred, labels=labels)
    return model

def plot_confusion_matrix(y_true, y_pred, title='Confusion matrix', cmap=plt.cm.Blues, labels=None):
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots()

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    
    ax = plt.gca()
    
    classes_count = y_true.value_counts().index.values    
    tick_marks = np.arange(len(classes_count))
    plt.xticks(tick_marks, rotation=45)
        
    if labels:
        ax.set_xticklabels(labels)
        ax.set_yticklabels(labels)
    else:
        ax.set_xticklabels((ax.get_xticks() +1).astype(str))

    plt.yticks(tick_marks)

    thresh = cm.max() / 2.
    for row, col in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        value      = cm[row, col]
        text_color = "white" if value > thresh else "black"
        plt.text(row, col, value, horizontalalignment="center", color=text_color)

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

def set_summary(features, target, title=None):
    '''
    Funciones utilizadas para contruir un resumen de datos relevante de un objeto SetsGroup.
    '''
    if title:
        print(f'\n{title}:')
    print('- Features shape:',  features.shape)
    print('- Target shape:',     target.shape)
    print('- Target classes:')
    classes = target.value_counts(normalize=True)

    for index in range(0, len(classes) - 1):
        print("\t- Clase '{}': {:.2f} %".format(str(classes.index[index][0]), classes.values[index]* 100))
  
    missing = missing_values_summary(features)

    if missing.empty:
        print('- Valores faltantes en features: No hay valores faltantes!')
    else:
        print('- Valores faltantes en features: ')
        print(missing)

def missing_values_summary(df):
    '''
    Funciones usada para detectar missing values.
    '''
    result = round(df.isna().sum() * 100 / len(df), 2)
    result = result[result > 0]
    result = result.apply(lambda value: f'{value}%')
    return result