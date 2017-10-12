# coding = UTF-8

import os
import pandas as pd
import pickle


MAIN_PATH = 'F:/roombackup/dataset/yangstock'

raw_state_owned_data = pd.read_pickle(os.path.join(MAIN_PATH, 'raw_state_owned_data.pkl'))

print(raw_state_owned_data)





