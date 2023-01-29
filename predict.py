# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:28:53 2022

@author: Administrator
"""

import pandas as pd
import numpy as np
import joblib
from utility import extract
from esm.pretrained import load_model_and_alphabet_local

def predict(in_fasta, batch_size, maxlen = 200):
    ## 1. load arg model and category model and category index
    arg_model = joblib.load('models/arg_model.pkl') #joblib.load('models/arg_model.pkl')
    cat_model = joblib.load('models/cat_model.pkl') #joblib.load('models/cat_model.pkl')
    cat_index = np.loadtxt('models/Category_Index.csv',dtype = str,delimiter = ",").tolist()

    # 2. generating the embedding representation
    print("Loading the ESM-1b model for protein embedding ...")
    try:
        model, alphabet = load_model_and_alphabet_local('models/esm1b_t33_650M_UR50S.pt')
        model.eval()
    except IOError:
        print("The ESM-1b model is not accessible.")
    
    seq_id, embedding_res = extract(in_fasta, alphabet, model, repr_layers = [32], 
                                    batch_size = batch_size, max_len= maxlen)
    seq_num = len(seq_id)
    cat_num = len(cat_index)
    pred_res = pd.DataFrame({'seq_id':seq_id, 'pred':''})
    pred_res = pd.concat([pred_res, pd.DataFrame(data = np.zeros((seq_num,cat_num+1),dtype='float64'),
                     columns= ['ARG']+cat_index)], axis = 1)
    # predict ARGs
    pred_res['ARG'] = arg_model.predict_proba(embedding_res)[:,1]
    # predict Category
    arg_ind = np.where(pred_res['ARG']>0.5)[0].tolist()
    cat_out = cat_model.predict_proba(embedding_res[arg_ind,])
    for i in range(len(cat_out)):
       pred_res.iloc[arg_ind, i+3] = cat_out[i][:,1]
       
    for i in arg_ind:
        cats = [cat_index[k] for k,v in enumerate(pred_res.iloc[i, 3:]) if v>=0.5]
        pred_res.iloc[i, 1] = ';'.join(cats)
    return pred_res

