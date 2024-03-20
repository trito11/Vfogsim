import pandas as pd
import os

def preprocess(file_addr, source):
    os.chdir('..')
    os.chdir('Data')
    os.chdir(source)
    traffic = pd.read_csv(file_addr).values
    os.chdir('../..')  # Trở lại thư mục gốc
    os.chdir('Functions')  # Đổi lại thư mục Functions
    return traffic
