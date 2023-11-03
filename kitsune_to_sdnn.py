from __future__ import print_function
import pandas as pd
import sys
from sklearn.preprocessing import LabelEncoder
# Replaced below 
# from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.preprocessing import sequence
# from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
from keras.datasets import imdb
# from keras.utils.np_utils import to_categorical
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics
from sklearn.preprocessing import Normalizer
import h5py
from keras import callbacks
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
# Read the data from the CSV file
def label_encode_csv(filename):
    file_path = 'TestConvert.csv'  
    df = pd.read_csv(file_path)
    non_categorical_fields = ['frame.time_epoch', 'frame.len',"Attack Category","Flow ID"] 
    categorical_fields = [col for col in df.columns if col not in non_categorical_fields]
    label_encoder = LabelEncoder()
    for col in categorical_fields:
        df[col] = label_encoder.fit_transform(df[col].astype(str))

    output_file = 'Converted.csv'  # Name for the new CSV file
    df.to_csv(output_file, index=False)

def run_csv_through(orig_file_name,filename,num_training):
    df_all = pd.read_csv('Converted.csv')
    num_features = len(df_all.columns) - 3
    traindata = df_all.iloc[:num_training,:]
    testdata = df_all.iloc[num_training:,:]

    X = traindata.iloc[:,:-3]
    print("X is \n" , X)
    Y = traindata.iloc[:,-3]
    print("Y is \n" , Y)
    C = testdata.iloc[:,-3]
    print("C is \n", C)
    T = testdata.iloc[:,:-3]
    print("T is \n", T)
    scaler = Normalizer().fit(X)
    trainX = scaler.transform(X)

    scaler = Normalizer().fit(T)
    testT = scaler.transform(T)

    y_train = np.array(Y)
    y_test = np.array(C)

    X_train = np.array(trainX)
    X_test = np.array(testT)
    print(y_train)
    print(y_test)
    print(X_train)
    print(X_test)

    batch_size = 64

    # 1. define the network
    model = Sequential()
    model.add(Dense(1024,input_dim=num_features,activation='relu'))  
    model.add(Dropout(0.01))
    model.add(Dense(768,activation='relu'))  
    model.add(Dropout(0.01))
    model.add(Dense(512,activation='relu'))  
    model.add(Dropout(0.01))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    # try using different optimizers and different optimizer configs
    # model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    # checkpointer = callbacks.ModelCheckpoint(filepath="results/"+orig_file_name+"/dnn3layer/checkpoint-{epoch:02d}.hdf5", verbose=1, save_best_only=True, monitor='loss')
    # csv_logger = CSVLogger('results/'+orig_file_name+'/dnn3layer/training_set_dnnanalysis.csv',separator=',', append=False)
    # model.fit(X_train, y_train,  batch_size=batch_size, epochs=100, callbacks=[checkpointer,csv_logger])
    # model.save("results/"+orig_file_name+"/dnn3layer/dnn3layer_model.hdf5")

if __name__ == "__main__":
    print(sys.argv)
    # if len(sys.argv) < 3:
    #     print("Usage: script.py <Input_file> <num_training_rows>")
    #     sys.exit(1)

    # input_file = sys.argv[1]
    # num_training = int(sys.argv[2])
    input_file = "TestConvert.csv"
    num_training = 4
    label_encode_csv(input_file)
    run_csv_through(input_file,"abc",5)
