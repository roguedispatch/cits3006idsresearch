import torch
import numpy as np
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset
from sklearn.model_selection import train_test_split
from utils import *

import argparse
import warnings

warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--dataset", type=str, default='nsl')
parser.add_argument("--epochs", type=int, default=4)
parser.add_argument("--epoch_1", type=int, default=1)
parser.add_argument("--percent", type=float, default=0.8)
parser.add_argument("--flip_percent", type=float, default=0.2)
parser.add_argument("--sample_interval", type=int, default=2000)
parser.add_argument("--cuda", type=str, default="0")

args = parser.parse_args()
dataset = args.dataset
epochs = args.epochs
epoch_1 = args.epoch_1
percent = args.percent
flip_percent = args.flip_percent
sample_interval = args.sample_interval
cuda_num = args.cuda

tem = 0.02
bs = 128
seed = 5009
seed_round = 5

if dataset not in ['nsl', 'unsw', 'kddcup99', 'mirai', 'cicids2017', 'botiot', 'ctu13']:
    raise ValueError("Invalid dataset name.")

if dataset == 'nsl':
    KDDTrain_dataset_path   = "NSL_pre_data/PKDDTrain+.csv"
    KDDTest_dataset_path    = "NSL_pre_data/PKDDTest+.csv"

    KDDTrain   =  load_data(KDDTrain_dataset_path)
    KDDTest    =  load_data(KDDTest_dataset_path)

    # 'labels2' means normal and abnormal, 'labels9' means 'attack_seen', 'attack_unseen', and normal
    # Create an instance of SplitData for 'nsl'
    splitter_nsl = SplitData(dataset='nsl')
    # Transform the data
    x_train, y_train = splitter_nsl.transform(KDDTrain, labels='labels2')
    x_test, y_test = splitter_nsl.transform(KDDTest, labels='labels2')

    input_dim = x_train.shape[1]
elif dataset == 'unsw':
    UNSWTrain_dataset_path   = "UNSW_pre_data/UNSWTrain.csv"
    UNSWTest_dataset_path    = "UNSW_pre_data/UNSWTest.csv"

    UNSWTrain   =  load_data(UNSWTrain_dataset_path)
    UNSWTest    =  load_data(UNSWTest_dataset_path)

    # Create an instance of SplitData for 'unsw'
    splitter_unsw = SplitData(dataset='unsw')

    # Transform the data
    x_train, y_train = splitter_unsw.transform(UNSWTrain, labels='label')
    x_test, y_test = splitter_unsw.transform(UNSWTest, labels='label')

    input_dim = x_train.shape[1]

elif dataset == 'kddcup99':

    KDDCupTrain_dataset_path   = "../DATASETS/KDDCup99/train.csv"
    KDDCupTest_dataset_path    = "../DATASETS/KDDCup99/test.csv"

    KDDCupTrain   =  load_data(KDDCupTrain_dataset_path)
    KDDCupTest    =  load_data(KDDCupTest_dataset_path)

    # Create an instance of SplitData for 'kddcup99'
    splitter_kdd = SplitData(dataset='kddcup99')

    # Transform the data
    x_train, y_train = splitter_kdd.transform(KDDCupTrain, labels='label')
    x_test, y_test = splitter_kdd.transform(KDDCupTest, labels='label')

    input_dim = x_train.shape[1]

    print(pd.Series(y_train).value_counts())
    print(pd.Series(y_test).value_counts())
    
elif dataset == 'mirai':
    MIRAI_dataset_path = "../DATASETS/Mirai/FLOWS/AOC-IDS.csv"
    MIRAIDataset  =  load_data(MIRAI_dataset_path)
    
    MIRAITrain, MIRAITest = train_test_split(MIRAIDataset, test_size=0.2, random_state=seed)

    splitter_mirai = SplitData(dataset='mirai')
    
    # Transform the data
    x_train, y_train = splitter_mirai.transform(MIRAITrain, labels='label')
    x_test, y_test = splitter_mirai.transform(MIRAITest, labels='label')

    input_dim = x_train.shape[1]

    print(pd.Series(y_train).value_counts())
    print(pd.Series(y_test).value_counts())
    
elif dataset == 'cicids2017':
    CICIDS2017_dataset_path = "../DATASETS/CICIDS2017_Fixed/FLOWS/AOC-IDS_undersampled.csv"
    CICIDS2017Dataset  =  load_data(CICIDS2017_dataset_path)
    CICIDSTrain, CICIDSTest = train_test_split(CICIDS2017Dataset, test_size=0.2, random_state=seed, stratify=CICIDS2017Dataset['label'])
    
    splitter_cicids = SplitData(dataset='cicids2017')
    x_train, y_train = splitter_cicids.transform(CICIDSTrain, labels='label')
    x_test, y_test = splitter_cicids.transform(CICIDSTest, labels='label')

    input_dim = x_train.shape[1]

    print(pd.Series(y_train).value_counts())
    print(pd.Series(y_test).value_counts())
elif dataset == 'botiot':
    BOTIOT_dataset_path = "../DATASETS/BOT-IoT/FLOWS/AOC-IDS_undersampled_extra.csv"
    BOTIOTDataset  =  load_data(BOTIOT_dataset_path)
    BOTIOTTrain, BOTIOTTest = train_test_split(BOTIOTDataset, test_size=0.2, random_state=seed, stratify=BOTIOTDataset['label'])
    
    splitter_botiot = SplitData(dataset='botiot')
    x_train, y_train = splitter_botiot.transform(BOTIOTTrain, labels='label')
    x_test, y_test = splitter_botiot.transform(BOTIOTTest, labels='label')

    input_dim = x_train.shape[1]

    print(pd.Series(y_train).value_counts())
    print(pd.Series(y_test).value_counts())
elif dataset == 'ctu13':
    CTU13_dataset_path = "../DATASETS/CTU13/FLOWS/AOC-IDS_undersampled_extra.csv"
    CTU13Dataset  =  load_data(CTU13_dataset_path)

    CTU13Dataset = pd.get_dummies(CTU13Dataset, columns=['State', 'Proto'], drop_first=False)

    CTU13Train, CTU13Test = train_test_split(CTU13Dataset, test_size=0.2, random_state=seed, stratify=CTU13Dataset['label'])
    
    splitter_ctu13 = SplitData(dataset='ctu13')
    x_train, y_train = splitter_ctu13.transform(CTU13Train, labels='label')
    x_test, y_test = splitter_ctu13.transform(CTU13Test, labels='label')

    input_dim = x_train.shape[1]

    print(x_train.shape)
    print(x_test.shape)

    print(pd.Series(y_train).value_counts())
    print(pd.Series(y_test).value_counts())
else:
    raise ValueError("Invalid dataset name.")

# Convert to torch tensors
x_train, y_train = torch.FloatTensor(x_train), torch.LongTensor(y_train)
x_test, y_test = torch.FloatTensor(x_test), torch.LongTensor(y_test)

device = torch.device("cuda:"+cuda_num if torch.cuda.is_available() else "cpu")

criterion = CRCLoss(device, tem)

average_accuracy = 0
average_precision = 0
avereage_recall = 0
average_f1 = 0
num_classes = len(np.unique(y_train))
total_cm = np.zeros((num_classes, num_classes))

for i in range(seed_round):
    # Set the seed for the random number generator for this iteration
    setup_seed(seed+i)

    online_x_train, online_x_test, online_y_train, online_y_test = train_test_split(x_train, y_train, test_size=percent, random_state=seed+i)
    train_ds = TensorDataset(online_x_train, online_y_train)
    train_loader = torch.utils.data.DataLoader(
        dataset=train_ds, batch_size=bs, shuffle=True)
    
    num_of_first_train = online_x_train.shape[0]

    model = AE(input_dim).to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr= 0.001)

    model.train()
    for epoch in range(epochs):
        print('seed = ', (seed+i), ', first round: epoch = ', epoch)
        for j, data in enumerate(train_loader, 0):
            inputs, labels = data
            inputs = inputs.to(device)

            labels = labels.to(device)
            optimizer.zero_grad()

            features, recon_vec = model(inputs)
            loss = criterion(features,labels) + criterion(recon_vec,labels)

            loss.backward()
            optimizer.step()

    x_train = x_train.to(device)
    x_test = x_test.to(device)
    online_x_train, online_y_train  = online_x_train.to(device), online_y_train.to(device)

    x_train_this_epoch, x_test_left_epoch, y_train_this_epoch, y_test_left_epoch = online_x_train.clone(), online_x_test.clone().to(device), online_y_train.clone(), online_y_test.clone()

####################### start online training #######################

    count = 0
    y_train_detection = y_train_this_epoch
        
    total_test_epochs = len(x_test_left_epoch)

    while len(x_test_left_epoch) > 0:
        print('seed = ', (seed+i), ', i = ', count)
        print(f"seed = {seed+i}, i = {count} / {total_test_epochs}")
        count += 1
        
        if len(x_test_left_epoch) < sample_interval:
            x_test_this_epoch = x_test_left_epoch.clone()
            x_test_left_epoch.resize_(0)
        else:
            x_test_this_epoch = x_test_left_epoch[:sample_interval].clone()
            x_test_left_epoch = x_test_left_epoch[sample_interval:]

        test_features = F.normalize(model(x_test_this_epoch)[0], p=2, dim=1)

        # must compute the normal_temp and normal_recon_temp again, because the model has been updated
        normal_temp = torch.mean(F.normalize(model(online_x_train[(online_y_train == 0).squeeze()])[0], p=2, dim=1), dim=0)
        normal_recon_temp = torch.mean(F.normalize(model(online_x_train[(online_y_train == 0).squeeze()])[1], p=2, dim=1), dim=0)
        predict_label = evaluate(normal_temp, normal_recon_temp, x_train_this_epoch, y_train_detection, x_test_this_epoch, 0, model)

        y_test_pred_this_epoch = predict_label
        y_train_detection = torch.cat((y_train_detection.to(device), torch.tensor(y_test_pred_this_epoch).to(device)))
        num_zero = int(flip_percent * y_test_pred_this_epoch.shape[0])
        zero_indices = np.random.choice(y_test_pred_this_epoch.shape[0], num_zero, replace=False)
        y_test_pred_this_epoch[zero_indices] = 1 - y_test_pred_this_epoch[zero_indices]

        x_train_this_epoch = torch.cat((x_train_this_epoch.to(device), x_test_this_epoch.to(device)))
        y_train_this_epoch_temp = y_train_this_epoch.clone()
        y_train_this_epoch = torch.cat((y_train_this_epoch_temp.to(device), torch.tensor(y_test_pred_this_epoch).to(device)))

        train_ds = TensorDataset(x_train_this_epoch, y_train_this_epoch)
        
        train_loader = torch.utils.data.DataLoader(
            dataset=train_ds, batch_size=bs, shuffle=True)
        model.train()
        for epoch in range(epoch_1):
            print('epoch = ', epoch)
            for j, data in enumerate(train_loader, 0):
                inputs, labels = data
                inputs = inputs.to(device)

                labels = labels.to(device)
                optimizer.zero_grad()

                features, recon_vec = model(inputs)

                loss = criterion(features,labels) + criterion(recon_vec,labels)

                loss.backward()
                optimizer.step()

################### test the performance after online training ###################
    normal_temp = torch.mean(F.normalize(model(online_x_train[(online_y_train == 0).squeeze()])[0], p=2, dim=1), dim=0)
    normal_recon_temp = torch.mean(F.normalize(model(online_x_train[(online_y_train == 0).squeeze()])[1], p=2, dim=1), dim=0)

    res_en, res_de, res_final = evaluate(normal_temp, normal_recon_temp, x_train_this_epoch, y_train_detection, x_test, y_test, model)

    average_accuracy += res_final[0]
    average_precision += res_final[1]
    avereage_recall += res_final[2]
    average_f1 += res_final[3]
    total_cm += res_final[4]

print('average_accuracy = ', average_accuracy / seed_round)
print('average_precision = ', average_precision / seed_round)
print('avereage_recall = ', avereage_recall / seed_round)
print('average_f1 = ', average_f1 / seed_round)

with open(f'{dataset}_results.txt', 'a') as f:
    f.write('dataset = ' + dataset + ', epochs = ' + str(epochs) + ', epoch_1 = ' + str(epoch_1) + ', percent = ' + str(percent) + ', flip_percent = ' + str(flip_percent) + ', sample_interval = ' + str(sample_interval) + ', cuda_num = ' + str(cuda_num) + '\n')
    f.write('average_accuracy = ' + str(average_accuracy / seed_round) + '\n')
    f.write('average_precision = ' + str(average_precision / seed_round) + '\n')
    f.write('avereage_recall = ' + str(avereage_recall / seed_round) + '\n')
    f.write('average_f1 = ' + str(average_f1 / seed_round) + '\n')
    f.write('total_cm = ' + str(total_cm) + '\n')
    f.write('\n')