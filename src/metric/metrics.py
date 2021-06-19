import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
import itertools

def plot_confusion_matrix(y_true, y_pred, title='Confusion matrix', cmap=plt.cm.Blues):
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots()
    labels = y_true.value_counts().index.values

    
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, rotation=45)
    ax = plt.gca()
    ax.set_xticklabels((ax.get_xticks() +1).astype(str))
    plt.yticks(tick_marks)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

def show_score(model, X, y, cv, groups=None, scoring='accuracy', n_jobs=24):
    scores = cross_val_score(model, X, y, scoring=scoring, cv=cv, n_jobs=n_jobs, groups=groups)
    print('Accuracy: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))

def show_summary(rs, X, y):
    model = rs.best_estimator_
    print('Hiper parameters:', rs.best_params_)
    print('Best score:', rs.best_score_)
    print('Accuracy: {:.3f} %'.format(model.score(X, y) * 100))