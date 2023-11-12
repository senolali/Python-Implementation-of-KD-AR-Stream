# Python-Implementation-of-KD-AR-Stream

This is python implementation of KD-AR Stream clsutering algorithm.
<br><br>
<b>Purpose:</b><br> The aim of this article to propose a new data stream clustering algorithm, which has an adaptive
radius, can adapt itself to the evolutionary structure of streaming data and works in a fully online manner.<br><br>



<b>Theory and Methods:</b><br>

     The method we propose basically receives its power from Kd-trees that support multidimensionality. Kd-trees are utilized in the processes of forming a new cluster and splitting the existing clusters. The process of range search with a determined radius (r) is performed on data placed into the tree. Two kinds of radius values are kept in KD-AR Stream: 
	The distance of farthest element of the cluster to the gravity center of the cluster (C_Radius).
	The average standard deviation in all dimensions (C_Std) and it is used to decide whether or not the clusters would be merged. 
     Proposed method supports evolution of data streams as mentioned in E-Stream algorithm [19]. In the E-Stream algorithm, there are five types of evolution. These are appearing of a new cluster, disappearing of an existing cluster, splitting of an existing cluster to two clusters, merging of two clusters and self-evolution of a cluster. In our approach, we supports inactivation of an active cluster and reactivation of an inactive cluster instead of disappearing (deletion). Figure 6 provides an outline of KD-AR Stream. We can sum up the evolutionary steps of the proposed model as follows:
	Appear: If sufficient amount of data, which is sufficiently far away from all clusters, are formed in the light of new received data, forming a new cluster by combining them;
	Activation-Inactivation: If amount of data in an active cluster drops below threshold value this cluster is inactived. On the contrary, an inactive cluster reactived if the number of elements exceeds threshold value when a new element is added to it;
	Merge: If the distances between centers of two or more clusters drop below the predetermined threshold value, these clusters merge (See Figure 3); 
	Split: If sufficient amount of data in an active cluster has a sufficient distance from the center of the cluster, this cluster is split (See Figure 4);
	Self-evolution: Behaviors of an existing cluster like radius, owned data and position can change over time according to evolution of data stream. Our approach adapts to the evolution in fast way.
 ![Clusters](img/Fig1.png) 
Fig. 1. Example of KD-AR Stream. Blue and red coloured data represent clusters, black data represent data which not belong to any cluster; green point in red cluster and red point in blue cluster represent cluster centers.


In this study, kd-tree is used to forming and splitting clusters, adaptive radius approach is used to support
increasing and decreasing the size of clusters, active/inactive status of clusters is used to adapt to the
evolutionary structure of streaming data and all the operations are done online. In order to create a new cluster,
the data that does not belong to any cluster are placed in a kd-tree, and the rangesearch operation is performed
on those data according to predefined variables r (the radius of candidate cluster) and N (the number of data
must be in the area). After forming the clusters, the radius of each cluster could be increased or decreased over
time if necessary. Some clusters may be split and some may be merged over time because of dynamically
changing structure of streaming data. Inactivation and reactivation of the status of clusters is used to allow for
the identification of clusters formed in the same region at a different time interval with same cluster labels in
accordance with the nature of the streaming data contrary to literature. This feature increases clustering quality
of the proposed method. A summarization method that consist of time window and sliding window is used to
support time based summarization without reduce performance.<br><br>
<b>Results:</b><br>
To verify the effectiveness of KD-AR Stream algorithm, it is compared with SE-Stream, DPStream, and
CEDAS on a variety of well-known datasets in terms of clustering quality and run-time complexity. The results
show that KD-AR Stream outperforms other algorithms with a higher clustering success in a reasonable time
as shown in Fig. A.<br>

![Accuracy](img/FigureA1.png) 
![Run-time](img/FigureA2.png) 

<br><br>
<b>Conclusion:</b><br>
The aim of this study is to propose a novel data stream clustering algorithm that adapts to the dynamic structure
of the streaming data. The aim achieved by using the five evolutionary process which are appearance,
activation/inactivation, self-evolution, merge, and split. According to the results, the proposed method is very
successful in terms of clustering quality and run-time complexity. 
<br>
If you use the code, please cite the article shared below:<br><br>
Şenol, A. & Karacan, H. (2020). K-boyutlu ağaç ve uyarlanabilir yarıçap (KD-AR Stream) tabanlı gerçek zamanlı akan veri kümeleme . Gazi Üniversitesi Mühendislik Mimarlık Fakültesi Dergisi , 35 (1) , 337-354 . DOI: 10.17341/gazimmfd.467226
