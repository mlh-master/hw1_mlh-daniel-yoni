# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 17:14:23 2019

@author: smorandv
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def rm_ext_and_nan(CTG_features, extra_feature):
    """

    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A dictionary of clean CTG called c_ctg
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    c_ctg = {col: (CTG_features[col].apply(pd.to_numeric, args=('coerce',))).dropna() for col in CTG_features if col!=extra_feature}
    # --------------------------------------------------------------------------
    return c_ctg


def nan2num_samp(CTG_features, extra_feature):
    """

    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A pandas dataframe of the dictionary c_cdf containing the "clean" features
    """
    c_cdf = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    for key in CTG_features:
        if key != extra_feature:
            prev_val = CTG_features[key]
            curr_val = pd.to_numeric(prev_val,errors='coerce')
            for i in range(len(curr_val)):
                while np.isnan(curr_val.values[i]):
                    curr_val.values[i] =np.random.choice(curr_val)
        c_cdf[key] = curr_val
    del c_cdf[extra_feature]   
        # -------------------------------------------------------------------------
    return pd.DataFrame(c_cdf)


def sum_stat(c_feat):
    """

    :param c_feat: Output of nan2num_cdf
    :return: Summary statistics as a dicionary of dictionaries (called d_summary) as explained in the notebook
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    d_summary={}
    for key in c_feat:
            curr_dict = {'Min' : np.amin(c_feat[key]) , 'Max' : np.amax(c_feat[key]), 'Median' : np.median(c_feat[key]), 'Q1' : np.quantile(c_feat[key], 0.25) , 'Q3'  : np.quantile(c_feat[key], 0.75)}
            d_summary.update({key: curr_dict})
    # -------------------------------------------------------------------------
    return d_summary


def rm_outlier(c_feat, d_summary):
    """

    :param c_feat: Output of nan2num_cdf
    :param d_summary: Output of sum_stat
    :return: Dataframe of the dictionary c_no_outlier containing the feature with the outliers removed
    """
    c_no_outlier = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    for key , value in c_feat.items():
        c_no_outlier[key]= value[(c_feat[key]<= d_summary[key]['Q3']+1.5*(d_summary[key]['Q3']-d_summary[key]['Q1'])) & (c_feat[key]>=  d_summary[key]['Q1']-1.5*(d_summary[key]['Q3']-d_summary[key]['Q1']))]
    # -------------------------------------------------------------------------
    return pd.DataFrame(c_no_outlier)


def phys_prior(c_cdf, feature, thresh):
    """

    :param c_cdf: Output of nan2num_cdf
    :param feature: A string of your selected feature
    :param thresh: A numeric value of threshold
    :return: An array of the "filtered" feature called filt_feature
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:-----------------------------
    filt_feature=c_cdf[feature][c_cdf[feature]<=thresh]
    # -------------------------------------------------------------------------
    return filt_feature


def norm_standard(CTG_features, selected_feat=('LB', 'ASTV'), mode='none', flag=False):
    """

    :param CTG_features: Pandas series of CTG features
    :param selected_feat: A two elements tuple of strings of the features for comparison
    :param mode: A string determining the mode according to the notebook
    :param flag: A boolean determining whether or not plot a histogram
    :return: Dataframe of the normalized/standardazied features called nsd_res
    """
    x, y = selected_feat
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    import matplotlib.pyplot as plt
    nsd_res={}
    if( mode=='none'):
        nsd_res=CTG_features.to_dict()
    if(mode=='standard'):
        nsd_res={x: (CTG_features[x]-np.mean(CTG_features[x]))/np.std(CTG_features[x]) for x in CTG_features}
    if(mode=='MinMax'):  
        nsd_res = {x: (CTG_features[x]-np.amin(CTG_features[x]))/(np.amax(CTG_features[x])-np.amin(CTG_features[x])) for x in CTG_features}
    if(mode=='mean'): 
        nsd_res = {x:(CTG_features[x]-np.mean(CTG_features[x]))/(np.amax(CTG_features[x])-np.amin(CTG_features[x])) for x in CTG_features }
    if(flag):
        pd.DataFrame(nsd_res)[[x,y]].plot(kind='hist',bins=100)
        plt.ylabel('Counts')
        plt.xlabel('Values')
        plt.title(mode)
        plt.legend()
        plt.show()
        
        
    # --------------------------------------------------------------------------
    return pd.DataFrame(nsd_res)
