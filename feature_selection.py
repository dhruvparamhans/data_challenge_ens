# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 10:56:04 2017

@author: Admin
"""

import numpy as np
import pandas as pd
import time
import sklearn

tags = ['ID', 'offset', 'bid_1', 'ask_1','bid_2', 'ask_2', 'bid_size_1', 'ask_size_1','bid_size_2',
        'ask_size_2', 'bid_entry_1','ask_entry_1', 'bid_entry_2', 'ask_entry_2',
		'bid_entropy_1', 'ask_entropy_1', 'bid_entropy_2',
		'ask_entropy_2', 'bid_sqentry_1', 'ask_sqentry_1',
          'bid_sqentry_2', 'ask_sqentry_2', 'nb_trade']

useful_tags = tags[2:]
input_file_name='Smaller Files/xaa'
input_file_name ='Training_XS_300.csv'

training_data = pd.read_csv(input_file_name, delimiter=';')
training_group=training_data.groupby('ID')
#'Target_data.csv'
target_data = pd.read_csv(input_file_name+'_target', delimiter=';', nrows=len(training_group))
training_group1=training_group.get_group(1)

def add_product(vect, ind1, ind2):
    ## adds a new colum to vect from the product of ind1 and ind2
    vect[str(ind1)+"_prod_"+str(ind2)]=vect[str(ind2)]*vect[str(ind2)]
    return vect
    

def group_hetero_modification(group1, df2, indlist):
    ## adds two new columns to df2 for ind in indlist in group1
    for name, df1 in group1:
        for ind in indlist:        
            count=df1[str(ind)].diff().astype(bool).sum()-1
            df2.ix[name,'change_times_'+str(ind)]=count
    for ind in indlist:                  
        df2['if_change_'+str(ind)] = df2['change_times_'+str(ind)].astype(bool)
    return

    
def group_self_modification(x, *arg):
    ## in order to create a new matrix with just added columns
    add_product(x, 'ask_1', 'ask_size_1')
    add_product(x, 'bid_1', 'bid_size_1')
    return x

target_data.set_index('ID', inplace=True)

start_time = time.time()
extended_training_data=training_group.apply(group_self_modification)
print("--- %s seconds ---" % (time.time() - start_time))
#120s
extended_training_group=extended_training_data.groupby('ID')
extended_training_group1=extended_training_group.get_group(1)

extended_training_stats=extended_training_group['ask_1','bid_1','nb_trade'].agg([np.mean, np.std, np.max, np.min])

start_time = time.time()
group_hetero_modification(extended_training_group, extended_training_stats, ['ask_1','bid_1','nb_trade'])
print("--- %s seconds ---" % (time.time() - start_time))
#270s
#extended_training_data.set_index(['ID','offset'], inplace=True)

from sklearn import feature_selection
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import SelectKBest


MI=sklearn.feature_selection.mutual_info_classif(extended_training_stats, target_data['TARGET']);MI
X_new = SelectKBest(mutual_info_classif, k=5).fit_transform(extended_training_stats, target_data['TARGET'])