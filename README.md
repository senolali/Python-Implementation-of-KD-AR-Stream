# Python-Implementation-of-KD-AR-Stream

This is python implementation of KD-AR Stream clsutering algorithm.
<br><br>
<b>Purpose:</b><br> The aim of this article to propose a new data stream clustering algorithm, which has an adaptive
radius, can adapt itself to the evolutionary structure of streaming data and works in a fully online manner.<br><br>
<b>Theory and Methods:</b><br>
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
