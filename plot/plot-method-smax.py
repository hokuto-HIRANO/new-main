import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os



# データの読み込み
df = pd.read_csv('dataset/dataset-all.csv')

f = open('dataset/dataset_1/params.json', 'r')
json = json.load(f)

network_list = json['network']
interact_list = json['interact']
method_list = ['sparcc', 'rebacca', 'spiec-easi', 'cclasso',
               'flac-pea', 'flac-spe', 'flac-ppea', 'flac-pspe', 'flac-mic']
smax_list = json['s-max']
kave_list = [2, 4, 6, 8]
nn_list = [20, 50, 100]
sampling_list = [100, 300, 500]



# 表示関数

def show(df, auc_type, network, interact, kave, nn, sampling, dir_path):
    
    d_use = df[(df['auc-type'] == auc_type) &
               (df['network'] == network) &
               (df['interact'] == interact) &
               (df['k-ave'] == kave) &
               (df['nn'] == nn) &
               (df['sampling'] == sampling)]

    for method in method_list:
        x = d_use.loc[d_use['calc-method'] == method, 's-max'].unique()
        y = d_use.loc[d_use['calc-method'] == method, 'mean']

        # flactionデータの場合は点線
        if method.find('flac') > -1:
            plt.plot(x, y, label=method, linewidth=1, linestyle='dashed', marker="o", markersize=1)
        else:
            plt.plot(x, y, label=method, linewidth=1, marker="o", markersize=1)
        
        plt.legend(bbox_to_anchor=(1, 0), loc='lower right', borderaxespad=1, fontsize=8)
    
    if auc_type == 'roc':
        plt.ylim([0.4,1])
    elif auc_type == 'prc':
        plt.ylim([-0.01,1])
    
    plt.xlim([0, np.max(x)*1.05])
    
    plt.title('network:{} | interact:{} \nkave:{} | nn:{} | sampling:{} | \nsmax:{}'.format(network, interact, kave, nn, sampling, x))

    plt.xlabel('smax')
    plt.ylabel('{}-auc'.format(auc_type))

    plt.savefig('{}/k{}-n{}-sp{}.png'.format(dir_path, kave, nn, sampling))
    plt.close()



# === メイン ===

for network in network_list:
    for interact in interact_list:

        # 途中結果
        print('=== {} - {} ==='.format(network, interact))

        # 保存用ディレクトリ作成
        dir_path = 'img/show-method-smax/st-{}/in-{}'.format(network, interact)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        for kave in kave_list:
            for nn in nn_list:
                for sampling in sampling_list:

                    #show(df, 'roc', network, interact, kave, nn, sampling, dir_path)

                    show(df, 'prc', network, interact, kave, nn, sampling, dir_path)