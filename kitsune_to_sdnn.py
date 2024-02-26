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
from keras.optimizers import Adam
from keras import backend as K
from sklearn.preprocessing import Normalizer
import h5py
from keras import callbacks
from keras import metrics
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger


# Read the data from the CSV file
def label_encode_csv(filename):
    file_path = filename;  
    df = pd.read_csv(file_path)
    non_categorical_fields = ['frame.time_epoch', 'frame.len',"Attack Category","Flow ID"] 
    categorical_fields = [col for col in df.columns if col not in non_categorical_fields]
    label_encoder = LabelEncoder()
    for col in categorical_fields:
        df[col] = label_encoder.fit_transform(df[col].astype(str))

    output_file = filename[:-4] + 'converted.csv'  # Name for the new CSV file
    df.to_csv(output_file, index=False)
    return output_file

def train(orig_file_name,conv_filename,num_training):
    df_all = pd.read_csv(conv_filename)
    num_features = len(df_all.columns) - 1
    traindata = df_all.iloc[:num_training,:]
    testdata = df_all.iloc[num_training:,:]
    temp_path = "results/"+orig_file_name+"/dnn3layer/"
    X = traindata.iloc[:,:-1]
    Y = traindata.iloc[:,-1]
    C = testdata.iloc[:,-1]
    T = testdata.iloc[:,:-1]
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
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    checkpointer = callbacks.ModelCheckpoint(filepath=temp_path+"/checkpoint-{epoch:02d}.hdf5", verbose=1, save_best_only=True, monitor='loss')
    csv_logger = CSVLogger(temp_path+'/training_set_dnnanalysis.csv',separator=',', append=False)
    model.fit(X_train, y_train,  batch_size=batch_size, epochs=100, callbacks=[checkpointer,csv_logger])
    model.save(temp_path+"/dnn3layer_model.hdf5")

def test(orig_file_name,conv_filename,num_training):
    df_all = pd.read_csv(conv_filename)
    num_features = len(df_all.columns) - 1
    traindata = df_all.iloc[:num_training,:]
    testdata = df_all.iloc[num_training:,:]
    temp_path = "results/"+orig_file_name+"/dnn3layer/"
    X = traindata.iloc[:,:-1]
    Y = traindata.iloc[:,-1]
    C = testdata.iloc[:,-1]
    T = testdata.iloc[:,:-1]
    scaler = Normalizer().fit(X)
    trainX = scaler.transform(X)

    scaler = Normalizer().fit(T)
    testT = scaler.transform(T)

    y_train = np.array(Y)
    y_test = np.array(C)


    X_train = np.array(trainX)
    X_test = np.array(testT)


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

    '''
    # try using different optimizers and different optimizer configs
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    checkpointer = callbacks.ModelCheckpoint(filepath="kddresults/dnn3layer/checkpoint-{epoch:02d}.hdf5", verbose=1, save_best_only=True, monitor='loss')
    csv_logger = CSVLogger('kddresults/dnn3layer/training_set_dnnanalysis.csv',separator=',', append=False)
    model.fit(X_train, y_train,  batch_size=batch_size, nb_epoch=100, callbacks=[checkpointer,csv_logger])
    model.save("kddresults/dnn3layer/dnn3layer_model.hdf5")
    '''

    score = []
    name = []
    from sklearn.metrics import confusion_matrix
    import os
    for file in os.listdir(temp_path):
        model.load_weights(temp_path+file)
        y_train1 = y_test
        # Below deprecated, replaced with updated
        # y_pred = model.predict_classes(X_test)
        y_pred = (model.predict(X_test) > 0.5).astype("int32")
        accuracy = accuracy_score(y_train1, y_pred)
        recall = recall_score(y_train1, y_pred , average="binary")
        precision = precision_score(y_train1, y_pred , average="binary")
        f1 = f1_score(y_train1, y_pred, average="binary")
        print("----------------------------------------------")
        print("accuracy")
        print("%.3f" %accuracy)
        print("recall")
        print("%.3f" %recall)
        print("precision")
        print("%.3f" %precision)
        print("f1score")
        print("%.3f" %f1)
        score.append(accuracy)
        name.append(file)


    model.load_weights(temp_path+name[score.index(max(score))])
    # Below deprecated, replaced with following 2 lines
    # pred = model.predict_classes(X_test)
    # proba = model.predict_proba(X_test)
    pred = (model.predict(X_test) > 0.5).astype("int32")
    proba = model.predict(X_test)
    np.savetxt(temp_path+"dnnres/dnn3predicted.txt", pred)
    np.savetxt(temp_path+"dnnres/dnn3probability.txt", proba)

    accuracy = accuracy_score(y_test, pred)
    recall = recall_score(y_test, pred , average="binary")
    precision = precision_score(y_test, pred , average="binary")
    f1 = f1_score(y_test, pred, average="binary")


    print("----------------------------------------------")
    print("accuracy")
    print("%.3f" %accuracy)
    print("precision")
    print("%.3f" %precision)
    print("recall")
    print("%.3f" %recall)
    print("f1score")
    print("%.3f" %f1)
    np.savetxt(temp_path+"dnnres/results.txt",[accuracy,recall,precision,f1])

def train_and_test(orig_file_name,conv_filename,num_training):
    train(orig_file_name,conv_filename,num_training)
    test(orig_file_name,conv_filename,num_training)


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) < 3:
        print("Usage: script.py <Input_file> <num_training_rows>")
        sys.exit(1)

    input_file = sys.argv[1]
    num_training = int(sys.argv[2])
    new_file = label_encode_csv(input_file)
    train_and_test(input_file,new_file,num_training)
