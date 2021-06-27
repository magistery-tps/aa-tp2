import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import learning_curve

def plot_curve(ax, values, label): 
    sns.lineplot(ax=ax, x=range(1, len(values) +1), y=values, label=label)
    
def plot_train_vs_val(ax, train_scores, valid_scores, train_size):
    plot_curve(ax, train_scores, label='Train')
    plot_curve(ax, valid_scores, label='Validation')
    ax.set_xlabel('Epocs')
    ax.set_ylabel('Accuracy')
    ax.set_title('Train size: {}'.format(train_size))

def plot_all_train_vs_val(train_sizes, train_scores, valid_scores, figsize=(10, 15), pad=4.0):
    fig, axs = plt.subplots(len(train_sizes), figsize=figsize)
    fig.suptitle('Accuracy train vs validation')
    fig.tight_layout(pad=pad)
    for index, train_size in enumerate(train_sizes):
        plot_train_vs_val(
            axs[index], 
            train_scores[index], 
            valid_scores[index],
            train_size
        )
    plt.show()

    
