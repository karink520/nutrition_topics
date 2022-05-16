import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def plot_article_counts_over_time(years):
    """
    Histogram of counts of articles in years

    Parameters:
    -----------
    years : a Pandas Series or numpy array giving the years of each article
    
    Returns:
    --------
    fig
    ax
    """
    fig, ax = plt.subplots()
    y_padding_for_text = 5
    #range_str = str(years.min()) +  '-' + str(years.max())

    bins = np.linspace(1980, 2020, 9)
    counts, bins = np.histogram(years, bins=bins)
    sns.histplot(years, bins=bins, edgecolor='white', ax=ax, color="seagreen")

    for idx in range(len(bins) - 1):
        ax.text((bins[idx] + bins[idx+1])/2, counts[idx] + y_padding_for_text ,str(counts[idx]), alpha=0.8, ha='center')
        
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    #ax.spines["bottom"].set_visible(False)
    ax.set_title("Count of Articles by Year")

    return fig, ax


def construct_legend_label(topic, feature_names, n_top_words_for_legend):
    """
    Creates a label for one topic with top words, for inclusion in legend
    
    Parameters:
    -----------
    topic: np.ndarray
        An array of length vocab_size that represents a topic 
        (e.g. an element of lda.components_)
    feature_names: list of str
        List of words
    n_top_words_for_legend: int
        Number of words to include
    Returns:
    --------
    label: str
    """
    top_features_ind = topic.argsort()[: -n_top_words_for_legend - 1 : -1]
    top_features = [feature_names[i] for i in top_features_ind]
    label = ''
    for word in top_features:
        label += word
        label += ', '
    label += "..."
    return label


def construct_title(model_name, smooth, normalize_by_yearly_counts):
    """
    Make title for plot of topics over time

    Parameters:
    -----------
    model_name: str
        E.g. LDA, NMF
    smooth: bool
    normalize_by_yearly_counts: bool

    Returns:
    --------
    title: str
    """
    title = model_name
    if smooth:
        title += ", smoothed"
    if normalize_by_yearly_counts:
        title += ", normalized"
    return title
