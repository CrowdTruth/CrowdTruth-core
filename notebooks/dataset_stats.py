#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 13:50:31 2018

@author: oanainel
"""
import pandas as pd
import numpy as np
'''
crowd = pd.read_csv("crowdflower/causal_relations_noOffset_lemma_all.csv")

crowd["document"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["sentence_index"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)

for i in range(len(crowd.index)):
    print(i)
    info = crowd["sentence1_id"].iloc[i].split("_")
    crowd["sentence_index"].iloc[i] = info[2]
    crowd["document"].iloc[i] = info[1].split("ecb")[0]
'''
'''
print(str(len(crowd["topic"].unique())) + " Topics: " + str(crowd["topic"].unique()))

print("Total number of sentences: " + str(len(crowd["sentence1_id"].unique())))

print("Total number of input units: " +  str(len(crowd["_unit_id"].unique())))


sentences = pd.concat([crowd["sentence1_id"], crowd["sentence1"], crowd["events1"], crowd["topic"], crowd["document"], crowd["sentence_index"]], axis=1, keys=["sentence1_id", "sentence1", "events1", "topic", "document", "sentence_index"])

sentences = sentences.drop_duplicates()

sentences["events_count"] = pd.Series(np.random.randn(len(sentences.index)), index=sentences.index)
sentences["units_count"] = pd.Series(np.random.randn(len(sentences.index)), index=sentences.index)

for i in range(len(sentences.index)):
    sentences["events_count"].iloc[i] = len(sentences["events1"].iloc[i].split("###"))
    if (sentences["events_count"].iloc[i] > 6):
        sentences["units_count"].iloc[i] = (sentences["events_count"].iloc[i] // 6) + 1
    else:
        sentences["units_count"].iloc[i] = 1
'''       


import matplotlib.pyplot as plt
import numpy as np


bins=range(int(sentences["events_count"].min()), int(sentences["events_count"].max()))
plt.hist(sentences["events_count"], bins=bins, align='left', rwidth=1, normed=False)

print(sentences["events_count"].mean())