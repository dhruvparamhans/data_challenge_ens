import numpy as np
import pandas as pd

tags = ['ID', 'offset', 'bid_1', 'ask_1',
		'bid_2', 'ask_2', 'bid_size_1', 'ask_size_1',
		'bid_size_2', 'ask_size_2', 'bid_entry_1',
		'ask_entry_1', 'bid_entry_2', 'ask_entry_2',
		'bid_entropy_1', 'ask_entropy_1', 'bid_entropy_2',
		'ask_entropy_2', 'bid_sqentry_1', 'ask_sqentry_1',
'		bid_sqentry_2', 'ask_sqentry_2', 'nb_trade']

useful_tags = tags[2:]

DATAPATH = '/media/dhruv/New Volume/data challenge/data/smaller files'

def get_data(input_file_name):
	target_file_name = input_file_name+'_target'
	input_data = pd.read_csv(input_file_name)
	target_data = pd.read_csv(target_file_name)
	unique_ids = input_data.ID.unique()
	input_data_dict = {elem: pd.DataFrame for elem in unique_ids}
	for keys in target_data_dict.keys():
		input_data_dict[key] = input_data[:][input_data.ID == key]
	dummy_index = list(target_data.ID)
	target_data.index = dummy_index
	return unique_ids, target_data_dict, input_data_dict

def is_change(test_dict, tag):
	ser = test_dict['df'][tag]
	count = 0
	for i in range(len(ser)):
		if ser[i-1] != ser[i]:
			count +=1
	 ## creating key-value pairs
    test_dict['max_'+tag] = max(ser)
    test_dict['min_'+tag] = min(ser)
    test_dict['change_by_'+tag] = -ser[0]+ser[len(ser)-1]
    test_dict['if_change_'+tag] = (count !=0)
    test_dict['mean_'+tag] = ser.mean()
    test_dict['change_times_'+tag] = count
    test_dict['target'] = target_data.TARGET

def create_hash_list(unique_ids):
	hash_list = {}
	for unique_id in unique_ids:
		test_dict = {}
		test_dict['df'] = input_data_dict[unique_id]
    	test_dict['df'].index = list(range(len(test_dict['df'].ID)))
    	test_dict['target'] = target_data.TARGET[unique_id]
    	test_dict['stats'] = test_dict['df'].describe()
    	test_dict['ID'] = unique_id
    	for tag in useful_tags:
        	is_change(test_dict,tag)
    	hash_list[unique_id] = test_dict
    return hash_list