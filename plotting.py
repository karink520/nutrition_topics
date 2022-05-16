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
