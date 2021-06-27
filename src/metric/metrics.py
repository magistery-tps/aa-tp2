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

    show_score(y_true, y_pred)

    print('Classification Report:')
    value_labels = [labels[r] for r in y_true_pred_values(y_true, y_pred)]
    print(classification_report(y_true, y_pred, target_names=value_labels))
    
    plot_confusion_matrix(y_true, y_pred, labels=labels)

    return model


def y_true_pred_values(y_true, y_pred):
    true_values  = y_true[y_true.columns[0]].unique()            
    return np.sort(np.unique(np.concatenate((true_values, np.unique(y_pred)))))

def show_score(y_true, y_pred):
    print('Accuracy: {:.4f} %\n'.format(accuracy_score(y_true, y_pred) * 100))

def plot_confusion_matrix(y_true, y_pred, title='Confusion matrix', cmap=plt.cm.Blues, labels=None):
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots()

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    
    ax = plt.gca()
    
    thresh = cm.max() / 2.
    for row, col in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        value      = cm[row, col]
        text_color = "white" if value > thresh else "black"
        plt.text(row, col, value, horizontalalignment="center", color=text_color)

    classes_count = y_true.value_counts().index.values    
    tick_marks = np.arange(len(classes_count))
    plt.xticks(tick_marks, rotation=45)
    plt.yticks(tick_marks)

    if labels:
        used_labels = [labels[r] for r in y_true_pred_values(y_true, y_pred)]
        ax.set_yticklabels(used_labels)
        ax.set_xticklabels(used_labels)
    else:
        ax.set_xticklabels((ax.get_xticks() +1).astype(str))

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