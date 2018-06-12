#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 09:06:08 2018

@author: oanainel
"""

import pandas as pd
import numpy as np


crowd = pd.read_csv("crowdflower/causal_relations_noOffset_lemma_all.csv")
crowd["topic"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)


for i in range(len(crowd.index)):
    print(i)
    crowd["topic"].iloc[i] = crowd["sentence1_id"].iloc[i].split("_")[0]

crowd.to_csv("crowdflower/causal_relations_noOffset_lemma_all.csv", index=False)


topics = crowd["topic"].unique()

print(topics)

for topic1 in topics:
    
    subset1 = crowd[crowd["topic"] == topic1]
    annotations1 = list(pd.concat([subset1['pair1_lemma'], subset1['pair2_lemma'], 
                         subset1['pair3_lemma'], subset1['pair4_lemma'], 
                         subset1['pair5_lemma'], subset1['pair6_lemma']]).unique())

    cleanedList1 = [x for x in annotations1 if pd.isnull(x) != True]

    for topic2 in topics:
        
        subset2 = crowd[crowd["topic"] == topic2]
        annotations2 = list(pd.concat([subset2['pair1_lemma'], subset2['pair2_lemma'], 
                         subset2['pair3_lemma'], subset2['pair4_lemma'], 
                         subset2['pair5_lemma'], subset2['pair6_lemma']]).unique())

        cleanedList2 = [x for x in annotations2 if pd.isnull(x) != True]
        
        if topic1 != topic2:
            if len(list(set(cleanedList1) & set(cleanedList2))) != 0:
                print(str(topic1) + " - " + str(topic2) + ": " + str(len(list(set(cleanedList1) & set(cleanedList2)))))


topic1 = ['22','32','33','18','16','19','35','12']
topic2 = ['20','37','41','8','4','23']
topic3 = ['13','14','5','1','3','7','30','24']


subset1 = crowd[crowd["topic"].isin(topic1)]
subset1.to_csv("crowdflower/causal_relation_noOffset_lemma_all_batch1.csv", index=False)
subset2 = crowd[crowd["topic"].isin(topic2)]
subset2.to_csv("crowdflower/causal_relation_noOffset_lemma_all_batch2.csv", index=False)
subset3 = crowd[crowd["topic"].isin(topic3)]
subset3.to_csv("crowdflower/causal_relation_noOffset_lemma_all_batch3.csv", index=False)


annotations1 = list(pd.concat([subset1['pair1_noOffset'], subset1['pair2_noOffset'], 
                         subset1['pair3_noOffset'], subset1['pair4_noOffset'], 
                         subset1['pair5_noOffset'], subset1['pair6_noOffset']]).unique())

cleanedList1 = [x for x in annotations1 if pd.isnull(x) != True]


annotations2 = list(pd.concat([subset2['pair1_noOffset'], subset2['pair2_noOffset'], 
                         subset2['pair3_noOffset'], subset2['pair4_noOffset'], 
                         subset2['pair5_noOffset'], subset2['pair6_noOffset']]).unique())

cleanedList2 = [x for x in annotations2 if pd.isnull(x) != True]


annotations3 = list(pd.concat([subset3['pair1_noOffset'], subset3['pair2_noOffset'], 
                         subset3['pair3_noOffset'], subset3['pair4_noOffset'], 
                         subset3['pair5_noOffset'], subset3['pair6_noOffset']]).unique())

cleanedList3 = [x for x in annotations3 if pd.isnull(x) != True]
