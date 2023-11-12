# -*- coding: utf-8 -*-
"""
Created on Wed May 19 12:50:30 2021

@author: Ali ŞENOL
"""
import numpy as np
import pandas as pd
import numpy_indexed as npi
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import scipy as sy
import kdtree
import vptree
from scipy.spatial import KDTree
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from itertools import islice
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import silhouette_score
import math
import matplotlib
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D


class KDARStream:
    N=int()
    TN=int()
    r=float()
    r_threshold=int()
    r_max=float()
    d=int()
    buffered_data=np.array([]) # buffered data and its info.
    Clusters=np.array([]) #Cluster labels with centers etc
    deleted_data=np.array([]) #deleted data with assigned cluster labels
    
    
    def  __init__(self,X, N,TN,r,r_threshold,r_max,d,plot=False):
        #algorithm parameters###########################################
        self.X=X
        self.N = N
        # self.t = t
        self.TN=TN
        self.r=r
        self.r_threshold=r_threshold
        self.r_max=r_max
        self.plot=plot
        ##################################################################
        self.d=d
        self.buffered_data=np.empty((0,d+3),float) #[index | clusterNo | isActive | features={d1,d2,d3...}]
        self.Clusters=np.empty((0,d+5),float) #[clusterNo | #of data it has | isActive | shell_radius | kernel_radius | centerCoordinates={d1,d2,d3,...}]
        self.deleted_data=np.empty((0,d+3),float) #[index | features={d1,d2,d3...} | predictedclusterLabel]
        for i in range(self.X.shape[0]):  
            self.addNode(X[i])
            self.NewClusterAppear()
            self.findandAddClosestCluster()
            self.splitClusters()
            self.mergeClusters()
            self.updateRadius()
            self.updateCenters()
            self.flagActiveClusters()
            if plot==True and self.d==2:
                self.plotData()
        self.dataset_=np.append(self.deleted_data[:,3:],self.buffered_data[:,3:],axis=0)
        self.labels_=np.append(self.deleted_data[:,1],self.buffered_data[:,1],axis=0)
    def calculate_cluster_center(self,X):
        return X.mean(axis=0)
    
    def calculateRadius(self,data,center):        
        dists = euclidean_distances(center.reshape(1,self.d),data)
        std=np.mean(np.std(data,axis=0))
        return dists.max()
    
    def euclidean(self,p1, p2):
        return np.sqrt(np.sum(np.power(p2 - p1, 2)))   

    def is_far_enough_to_all_clusters(self,X):
        flag=True
        for i in range(len(self.Clusters)):
            dist = np.linalg.norm(self.Clusters[i,5:] - X)
            if (self.Clusters[i,3]+self.r_max)>dist:
                flag=False
        return flag   
    def addNode(self,data): # add new data to buffered_data, and delete old ones 
        new_Node=np.empty((0,self.d+3),float)
        new_Node=np.hstack([np.array([len(self.buffered_data)+len(self.deleted_data),0,0]),np.array(data)])    
    
        self.buffered_data=np.append(self.buffered_data,[new_Node],axis=0)
        if(len(self.buffered_data)>self.TN):
            data=self.buffered_data[0:-self.TN,:]
            self.buffered_data=self.buffered_data[-self.TN:, :] 
            self.deleted_data=np.vstack([self.deleted_data,data])

    def NewClusterAppear(self):
        X=self.buffered_data[self.buffered_data[:,1]==0,3:]#data that do not belong to any cluster
        tree=kdtree.create(X.tolist()) #construct kdtree
        for i in range(len(X)): # for each data of tree do reangeserach
            points=tree.search_nn_dist(X[i,:], self.r) 
            center=self.calculate_cluster_center(np.array(points))
            if len(points)>=self.N:
                if(self.Clusters.size==0):
                    self.Clusters=np.vstack([self.Clusters,np.hstack([1,len(points),1,self.r,np.mean(np.std(points,axis=0)),center])])
                    indices=np.isin(self.buffered_data[:,3:], points)[:,0]
                    self.buffered_data[indices==True,1]=1
                    print("Cluster #1 is defined.")
                    # print(points)
                else:
                    flag=self.is_far_enough_to_all_clusters(center)
                    if (flag):
                        # print(points)
                        # print(np.mean(np.std(points,axis=0)))
                        new_cluster_label=self.Clusters.shape[0]+1
                        self.Clusters=np.vstack([self.Clusters,np.hstack([new_cluster_label,len(points),1,self.r,np.mean(np.std(points,axis=0)),center])])
                        indices=np.isin(self.buffered_data[:,3:], points)[:,0]
                        self.buffered_data[indices==True,1]=new_cluster_label
                        self.buffered_data[indices==True,2]=1         
                        print("Cluster #%d is defined."%len(self.Clusters))
                        # print(points)       
         
    def findandAddClosestCluster(self):
        for i in range(len(self.buffered_data)): # for each data
            clusterNo=0
            distance=float("inf")
            for k in range(len(self.Clusters[:,0])):
                dist = euclidean_distances(self.Clusters[k,5:].reshape(1,self.d),self.buffered_data[i,3:].reshape(1,self.d))
                if float(dist)<=(float(self.Clusters[k,3])+self.r_threshold):
                    if dist<distance:
                        distance=dist
                        clusterNo=self.Clusters[k,0] 
            self.buffered_data[i,1]=clusterNo
                    
    def updateRadius(self):        
        for k in self.Clusters:
            data=self.buffered_data[self.buffered_data[:,1]==k[0],3:]
            if len(data)>0:
                dists = euclidean_distances(k[5:].reshape(1,self.d),data)
                self.Clusters[self.Clusters[:,0]==k[0],3]=dists.max()
                self.Clusters[self.Clusters[:,0]==k[0],4]=np.mean(np.std(data,axis=0)) 
            else:
                self.Clusters[self.Clusters[:,0]==k[0],3]=self.r/2
                self.Clusters[self.Clusters[:,0]==k[0],4]=self.r/100 
    def updateCenters(self):
        for k in range(len(self.Clusters[:,0])):
            X=self.buffered_data[self.buffered_data[:,1]==self.Clusters[k,0],3:]
            if len(X)>=self.N:
                self.Clusters[k,5:]=X.mean(axis=0)
            else:
                Y=self.deleted_data[self.deleted_data[:,1]==self.Clusters[k,0],3:]
                X=np.append(X,Y,axis=0)
                X=X[-self.N:,:]
                self.Clusters[k,5:]=X.mean(axis=0)
    
    def flagActiveClusters(self): #Checking for active clusters
        for k in range(len(self.Clusters[:,0])):
            self.Clusters[k,1]=len(self.buffered_data[self.buffered_data[:,1]==self.Clusters[k,0],0]) 
            if  int(self.Clusters[k,1])>=self.N:
                if self.Clusters[k,2]==0:
                    print("Cluster #%d is activated."%self.Clusters[k,0])
                self.Clusters[k,2]=1 
            else:
                if self.Clusters[k,2]==1:
                    print("Cluster #%d is deactivated."%self.Clusters[k,0])
                self.Clusters[k,2]=0 
    def splitClusters(self):  
        for k in range(len(self.Clusters[:,0])): #For every cluster
            if  self.Clusters[k,1]>=2*self.N: # and self.Clusters[k,2]>2*self.r:   #If # of data that cluster has is greater than N
                 X=self.buffered_data[self.buffered_data[:,1]==self.Clusters[k,0],3:]#data cluster k
                 tree=kdtree.create(X.tolist()) #construct kdtree with data of cluster k
                 for l in range(len(X[:,0])): # for each data of cluster k
                     points=tree.search_nn_dist(X[l,:], self.r) # find number of data in radius r for data l
                     if len(points)>=self.N:    # if # of data in area is greater than N
                         center=self.calculate_cluster_center(np.array(points)) # calculate centroid of candidate cluster
                         indices = npi.indices(X, points, missing='ignore') #find data in the all data of cluster k
                         points2=np.delete(X, indices, 0)   # find remaining data of cluster k
                         if len(points2)>=self.N:
                             center2=self.calculate_cluster_center(np.array(points2))
                             dis=euclidean_distances([center],[center2])
                             r1=self.calculateRadius(points,center)
                             r2=self.calculateRadius(points2,center2)
                             if float(dis)>r1+r2+0.5*self.r:
                                 new_cluster_label=self.Clusters.shape[0]+1
                                 self.Clusters=np.vstack([self.Clusters,np.hstack([new_cluster_label,len(points),1,self.r,np.mean(np.std(points,axis=0)),center])])
                                 indices=np.isin(self.buffered_data[:,3:], points)[:,0]
                                 self.buffered_data[indices==True,1]=new_cluster_label
                                 self.buffered_data[indices==True,2]=1         
                                 print("Cluster #%d is split."%(self.Clusters[k,0]))
                                 break
    # def splitClusters(self):  
    #     for k in range(len(self.Clusters[:,0])): #For every cluster
    #         if  self.Clusters[k,1]>=2*self.N: # and self.Clusters[k,2]>2*self.r:   #If # of data that cluster has is greater than N
    #              X=self.buffered_data[self.buffered_data[:,1]==self.Clusters[k,0],3:]#data cluster k
    #              # tree=kdtree.create(X.tolist()) #construct kdtree with data of cluster k
    #              tree=vptree.VPTree(X.tolist(), self.euclidean)
    #              for l in range(len(X[:,0])): # for each data of cluster k
    #                  # points=tree.search_nn_dist(X[l,:], self.r) # find number of data in radius r for data l
    #                  points=tree.get_all_in_range(X[l,:], self.r)
    #                  A=np.empty((1,len(points[0][1])),float)
    #                  for ii in range(len(points)):
    #                     A=np.append(A,[points[ii][1]],axis=0)
    #                  points=A
    #                  if len(points)>=self.N:    # if # of data in area is greater than N
    #                      center=self.calculate_cluster_center(np.array(points)) # calculate centroid of candidate cluster
    #                      indices = npi.indices(X, points, missing='ignore') #find data in the all data of cluster k
    #                      points2=np.delete(X, indices, 0)   # find remaining data of cluster k
    #                      if len(points2)>=self.N:
    #                          center2=self.calculate_cluster_center(np.array(points2))
    #                          dis=euclidean_distances([center],[center2])
    #                          r1=self.calculateRadius(points,center)
    #                          r2=self.calculateRadius(points2,center2)
    #                          if float(dis)>r1+r2+0.5*self.r:
    #                              new_cluster_label=self.Clusters.shape[0]+1
    #                              self.Clusters=np.vstack([self.Clusters,np.hstack([new_cluster_label,len(points),1,self.r,np.mean(np.std(points,axis=0)),center])])
    #                              indices=np.isin(self.buffered_data[:,3:], points)[:,0]
    #                              self.buffered_data[indices==True,1]=new_cluster_label
    #                              self.buffered_data[indices==True,2]=1         
    #                              print("Cluster #%d is split."%(self.Clusters[k,0]))
    #                              break
    def mergeClusters(self):  
         for k in range(len(self.Clusters[:,0])): #For every cluster
             for l in range(k+1,len(self.Clusters[:,0])):
                  if self.Clusters[k,2]==1 and self.Clusters[l,2]==1: # if both clusters are active ones
                     dis=euclidean_distances([self.Clusters[k,5:]],[self.Clusters[l,5:]])
                     if dis <= (self.Clusters[k,3]+self.Clusters[l,4]) or dis <= (self.Clusters[k,4]+self.Clusters[l,3]):
                         print("Cluster #%d and #%d are merged"%(self.Clusters[k,0],self.Clusters[l,0]))
                         self.buffered_data[self.buffered_data[:,1]==self.Clusters[l,0],1]=self.Clusters[k,0]
                         self.Clusters = np.delete(self.Clusters, l, 0)
                         break                   
                            
    def generate_colormap(self,N):
        # np.argmax(self.Clusters[:,0])+1
        if N<=30:
            N=30
        
            
        arr = np.arange(N)/N
        N_up = int(math.ceil(N/7)*7)
        arr.resize(N_up)
        arr = arr.reshape(7,N_up//7).T.reshape(-1)
        ret = matplotlib.cm.hsv(arr)
        n = ret[:,3].size
        a = n//2
        b = n-a
        for i in range(3):
            ret[0:n//2,i] *= np.arange(0.2,1,0.8/a)
        ret[n//2:,3] *= np.arange(1,0.1,-0.9/b)
        ret[0,:]=[0,0,0,1]
        # print(ret)
        return ret

                  
    def plotData(self): 
        # ax = plt.gca()
        fig, ax=plt.subplots(figsize=(5,6), dpi=100)
        if len(self.Clusters[:,0])>0: 
            colors = [plt.cm.Spectral(each)
                      for each in np.linspace(0, 1, len(self.Clusters[:,0]))]
            colors=np.append([[0,0,0,1]],colors,axis=0)
            for i in range(len(self.buffered_data[:,0])):
                if self.buffered_data[i,1]==0:
                    mrk='o'
                    colr=np.array([0,0,0,1])
                else:
                    mrk='*'
                    colr=colors[int(self.buffered_data[i,1]-1),:]
                plt.plot(self.buffered_data[i,3],self.buffered_data[i,4],
                          c=colr,marker=mrk, markersize=10)
            for k in self.Clusters:
                    #plot shell circle
                    plt.plot(k[5],k[6],
                              c=[0,1,1],marker='d',markeredgecolor='k', markersize=5)
                    circle3 = plt.Circle((k[5], k[6]), k[3], 
                                          color='red', clip_on=False,fill=False)
                    ax.add_patch(circle3)
                    #plot kernel circle
                    plt.plot(k[5],k[6],
                              c=[0,1,1],marker='d',markeredgecolor='k', markersize=5)
                    circle2 = plt.Circle((k[5], k[6]), k[4], 
                                          color='red', clip_on=False,fill=False)
                    ax.add_patch(circle2)
        else:
            for i in range(len(self.buffered_data[:,0])):
                col=np.array([0,0,0,1])
                mrk='o'
                plt.plot(self.buffered_data[i,3],self.buffered_data[i,4],
                          c=col,marker=mrk, markersize=10)
        title=str("KD-AR Stream with (W=%d, N=%d,r=%.4f,\nr_thr.=%0.4f,r_max=%0.4f)"%(self.TN,self.N,self.r,self.r_threshold,self.r_max))
        plt.title(title)   
        plt.xlim([-0.1,1.2])
        plt.ylim([-0.1,1.2])   
        plt.grid()
        # plt.axis('equal')
        plt.show()
        # plt.clf()
        
    def purity_score(self,y_true, y_pred):
        # compute contingency matrix (also called confusion matrix)
        contingency_matrix = metrics.cluster.contingency_matrix(y_true, y_pred)
        # return purity
        return np.sum(np.amax(contingency_matrix, axis=0)) / np.sum(contingency_matrix) 
             

    







