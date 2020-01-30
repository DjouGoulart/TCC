import numpy as np
import pandas as pd
from statsmodels.formula.api import ols

import matplotlib.pyplot as plt
import seaborn as sns

from IPython.core.display import HTML

from data import *

def plot_reg(x, y, data, hue='litologia', ax=None, format_axis=True, log_y=False, log_x=False, scatter=True):
    if ax is None:
        figure, ax = plt.subplots(1, 1, figsize=(7, 5))
    
    formula = '%s ~ %s' % (y if not log_y else 'np.log(%s)' % y, x if not log_x else 'np.log(%s)' % x)
    result = ols(formula=formula, data=data).fit()
    
    lmin = data[x].min()
    lmax = data[x].max()
    steps = (lmax - lmin) / 40    
    
    prediction = pd.DataFrame(np.arange(lmin, lmax + steps, steps), columns=[x])
    
    if (log_y):
        prediction = prediction.join(np.exp(result.get_prediction(prediction).summary_frame()))
    else:
        prediction = prediction.join(result.get_prediction(prediction).summary_frame())
        
    prediction = prediction.rename(columns={'mean': y})
    
    if scatter:
        sns.scatterplot(x=x, y=y, data=data, hue=hue, palette='bright', ax=ax)
        
    sns.lineplot(x=x, y=y, data=prediction, ax=ax)
    
    handles, labels = ax.get_legend_handles_labels()
    if len(labels) > 0:
        idx = labels.index(hue)
        labels.pop(idx)
        handles.pop(idx)
        l = ax.legend(handles=handles, labels=labels, prop={'size': 12}, frameon=True, edgecolor='black')
    
    if format_axis:
        format_ax(x, y, ax)

    return ax


def format_ax(x, y, ax, fontsize=14):
    unit = '($%s$)'
    
    if x:
        metax = meta[x]
        ax.set_xlim(metax['limits'])
        ax.set_xlabel(r'$%s$ %s' % (metax['symbol'], unit % metax['unit'] if metax['unit'] else ''), fontsize=fontsize)
    
    
    if y:
        metay = meta[y]
        ax.set_ylim(metay['limits'])
        ax.set_ylabel(r'$%s$ %s' % (metay['symbol'], unit % metay['unit'] if metay['unit'] else ''), fontsize=fontsize)
    
    
def multi_table(table_list):
    ''' Acceps a list of IpyTable objects and returns a table which contains each IpyTable in a cell
    '''
    return HTML(
        '<table><tr>' + 
        ''.join(['<td>' + table._repr_html_() + '</td>' for table in table_list]) +
        '</tr></table>'
    )