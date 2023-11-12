import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import silhouette_score
from KD_ARStream_v2 import KDARStream # import class KDARStream from same directory
from IPython import get_ipython
import warnings
warnings.filterwarnings("ignore")
get_ipython().magic('reset -sf')
get_ipython().magic('clear all -sf')



plot=False
selected_dataset=4

print("Selected Dataset",selected_dataset)
if selected_dataset==1:  
    dataset = np.loadtxt("Datasets/ExclaStar.txt", dtype=float,delimiter=',')
    X=dataset[:,1:3]
    labels_true=dataset[:,3]
    dataset_name="2_ExclaStar"
    N= 9
    TN= 59
    r= 0.4
    r_threshold= 0.08
    r_max= 0.53
elif selected_dataset==2:
    dataset = np.loadtxt("Datasets/iris.txt", dtype=float,delimiter=',')
    X=dataset[:,0:4]
    labels_true=dataset[:,4]
    X = StandardScaler().fit_transform(X)
    dataset_name="3_Fisheriris"
    N= 18
    TN= 40
    r= 0.67
    r_threshold= 0.03
    r_max= 0.74
elif selected_dataset==3:
    dataset = np.loadtxt("Datasets/Breast_Cancer.txt", dtype=float,delimiter=',')
    labels_true = dataset[:,10]
    X = dataset[:,1:10]
    dataset_name="4_BreastCancer_"
    N= 21
    TN= 65
    r= 0.1
    r_threshold= 0.1
    r_max= 0.33
elif selected_dataset==4:
    data = np.loadtxt("Datasets/Aggregation2.txt",delimiter=',', dtype=float)
    X=data[:,0:2]
    labels_true = data[:,2]
    labels_true=np.ravel(labels_true)
    r= 0.07
    r_threshold= 0.01
    r_max=0.24
    N= 8
    TN= 74
    dataset_name="10_aggregation_"
    
####MinMaxNormalization#######################################################
scaler = MinMaxScaler()
scaler.fit(X)
MinMaxScaler()
X=scaler.transform(X)


kds=KDARStream(X,N,TN,r,r_threshold,r_max,X.shape[1],plot)
labels=kds.labels_
labels_true=labels_true.reshape(len(labels))

ARI=adjusted_rand_score(labels_true, labels)
Purity=kds.purity_score(labels_true, labels)
Silhouette=silhouette_score(X,labels)

 
print("ARI=",ARI)
print("Purity=",Purity)
print("Silhouette=",Silhouette)

    
    
    
    
    
    
    
    
    
