#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 20:35:41 2018

@author: oanainel
"""

import pandas as pd
import numpy as np
import re
import time

'''
crowd = pd.read_csv("crowdflower/causal_relations_preliminary.csv")

crowd["pair1_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair2_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair3_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair4_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair5_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair6_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["relations_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)

for i in xrange(len(crowd.index)):
    print(i)
    if pd.isnull(crowd["pair1"].iloc[i]) != True :
        newValue = crowd["pair1"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        newValue = re.sub("(_[0-9]+)", "", newValue)
        newValueComp = newValue.split(", ")
        newComp = sorted(newValueComp, key=str.lower)
        crowd["pair1_noOffset"].iloc[i] = ", ".join(newComp).lower()
    else:
        crowd["pair1_noOffset"].iloc[i] = crowd["pair1"].iloc[i]
        
    if pd.isnull(crowd["pair2"].iloc[i]) != True :
        newValue = crowd["pair2"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        newValue = re.sub("(_[0-9]+)", "", newValue)
        newValueComp = newValue.split(", ")
        newComp = sorted(newValueComp, key=str.lower)
        crowd["pair2_noOffset"].iloc[i] = ", ".join(newComp).lower()
    else:
        crowd["pair2_noOffset"].iloc[i] = crowd["pair2"].iloc[i]
        
    if pd.isnull(crowd["pair3"].iloc[i]) != True :
        newValue = crowd["pair3"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        newValue = re.sub("(_[0-9]+)", "", newValue)
        newValueComp = newValue.split(", ")
        newComp = sorted(newValueComp, key=str.lower)
        crowd["pair3_noOffset"].iloc[i] = ", ".join(newComp).lower()
    else:
        crowd["pair3_noOffset"].iloc[i] = crowd["pair3"].iloc[i]
        
    if pd.isnull(crowd["pair4"].iloc[i]) != True :
        newValue = crowd["pair4"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        newValue = re.sub("(_[0-9]+)", "", newValue)
        newValueComp = newValue.split(", ")
        newComp = sorted(newValueComp, key=str.lower)
        crowd["pair4_noOffset"].iloc[i] = ", ".join(newComp).lower()
    else:
        crowd["pair4_noOffset"].iloc[i] = crowd["pair4"].iloc[i]
        
    if pd.isnull(crowd["pair5"].iloc[i]) != True :
        newValue = crowd["pair5"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        newValue = re.sub("(_[0-9]+)", "", newValue)
        newValueComp = newValue.split(", ")
        newComp = sorted(newValueComp, key=str.lower)
        crowd["pair5_noOffset"].iloc[i] = ", ".join(newComp).lower()
    else:
        crowd["pair5_noOffset"].iloc[i] = crowd["pair5"].iloc[i]
        
    if pd.isnull(crowd["pair6"].iloc[i]) != True :
        newValue = crowd["pair6"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        newValue = re.sub("(_[0-9]+)", "", newValue)
        newValueComp = newValue.split(", ")
        newComp = sorted(newValueComp, key=str.lower)
        crowd["pair6_noOffset"].iloc[i] = ", ".join(newComp).lower()
    else:
        crowd["pair6_noOffset"].iloc[i] = crowd["pair6"].iloc[i]
        
    if (crowd["relations"].iloc[i] == "no_relation"):
        crowd["relations_noOffset"].iloc[i] = "no_relation"
    else:
        newValue = crowd["relations"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        crowdPairs = re.sub("(_[0-9]+)", "", newValue).split("\n")
        pairs = []
        for pair in crowdPairs:
            pair = pair.lower()
            if '-r-' in str(pair):
                newPairComp = pair.split("-r-")
                newPairCompSorted = sorted(newPairComp, key=str.lower)
                if (newPairComp[0].lower() == newPairCompSorted[0].lower()) == True:
                    pairs.append(newPairComp[0] + "-r-" + newPairComp[1])
                else:
                    pairs.append(newPairComp[1] + "--" + newPairComp[0])
            elif '--' in str(pair):
                newPairComp = pair.split('--')
                newPairCompSorted = sorted(newPairComp, key=str.lower)
                if (newPairComp[0].lower() == newPairCompSorted[0].lower()) == True:
                    pairs.append(newPairComp[0] + "--" + newPairComp[1])
                else:
                    pairs.append(newPairComp[1] + "-r-" + newPairComp[0])
            else:
                pairs.append(pair)
        crowd["relations_noOffset"].iloc[i] = "\n".join(pairs).lower()
        
        #time.sleep(35)

    
crowd.to_csv("crowdflower/causal_relations_preliminary_noOffset.csv", quotechar='"', index=False)
'''


crowd = pd.read_csv("crowdflower/causal_relations_main.csv")

crowd["pair1_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair2_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair3_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair4_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair5_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair6_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["relations_noOffset"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)

for i in xrange(len(crowd.index)):
    print(i)
    if pd.isnull(crowd["pair1"].iloc[i]) != True :
        newValue = crowd["pair1"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        newValue = re.sub("(_[0-9]+)", "", newValue)
        newValueComp = newValue.split(", ")
        newComp = sorted(newValueComp, key=str.lower)
        crowd["pair1_noOffset"].iloc[i] = ", ".join(newComp).lower()
    else:
        crowd["pair1_noOffset"].iloc[i] = crowd["pair1"].iloc[i]
        
    if pd.isnull(crowd["pair2"].iloc[i]) != True :
        newValue = crowd["pair2"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        newValue = re.sub("(_[0-9]+)", "", newValue)
        newValueComp = newValue.split(", ")
        newComp = sorted(newValueComp, key=str.lower)
        crowd["pair2_noOffset"].iloc[i] = ", ".join(newComp).lower()
    else:
        crowd["pair2_noOffset"].iloc[i] = crowd["pair2"].iloc[i]
        
    if pd.isnull(crowd["pair3"].iloc[i]) != True :
        newValue = crowd["pair3"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        newValue = re.sub("(_[0-9]+)", "", newValue)
        newValueComp = newValue.split(", ")
        newComp = sorted(newValueComp, key=str.lower)
        crowd["pair3_noOffset"].iloc[i] = ", ".join(newComp).lower()
    else:
        crowd["pair3_noOffset"].iloc[i] = crowd["pair3"].iloc[i]
        
    if pd.isnull(crowd["pair4"].iloc[i]) != True :
        newValue = crowd["pair4"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        newValue = re.sub("(_[0-9]+)", "", newValue)
        newValueComp = newValue.split(", ")
        newComp = sorted(newValueComp, key=str.lower)
        crowd["pair4_noOffset"].iloc[i] = ", ".join(newComp).lower()
    else:
        crowd["pair4_noOffset"].iloc[i] = crowd["pair4"].iloc[i]
        
    if pd.isnull(crowd["pair5"].iloc[i]) != True :
        newValue = crowd["pair5"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        newValue = re.sub("(_[0-9]+)", "", newValue)
        newValueComp = newValue.split(", ")
        newComp = sorted(newValueComp, key=str.lower)
        crowd["pair5_noOffset"].iloc[i] = ", ".join(newComp).lower()
    else:
        crowd["pair5_noOffset"].iloc[i] = crowd["pair5"].iloc[i]
        
    if pd.isnull(crowd["pair6"].iloc[i]) != True :
        newValue = crowd["pair6"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        newValue = re.sub("(_[0-9]+)", "", newValue)
        newValueComp = newValue.split(", ")
        newComp = sorted(newValueComp, key=str.lower)
        crowd["pair6_noOffset"].iloc[i] = ", ".join(newComp).lower()
    else:
        crowd["pair6_noOffset"].iloc[i] = crowd["pair6"].iloc[i]
        
    if (crowd["relations"].iloc[i] == "no_relation"):
        crowd["relations_noOffset"].iloc[i] = "no_relation"
    else:
        newValue = crowd["relations"].iloc[i].replace('"', '')
        newValue = newValue.replace("'", "")
        crowdPairs = re.sub("(_[0-9]+)", "", newValue).split(",")
        pairs = []
        for pair in crowdPairs:
            pair = pair.lower()
            if '-r-' in str(pair):
                newPairComp = pair.split("-r-")
                newPairCompSorted = sorted(newPairComp, key=str.lower)
                if (newPairComp[0].lower() == newPairCompSorted[0].lower()) == True:
                    pairs.append(newPairComp[0] + "-r-" + newPairComp[1])
                else:
                    pairs.append(newPairComp[1] + "--" + newPairComp[0])
            elif '--' in str(pair):
                newPairComp = pair.split('--')
                newPairCompSorted = sorted(newPairComp, key=str.lower)
                if (newPairComp[0].lower() == newPairCompSorted[0].lower()) == True:
                    pairs.append(newPairComp[0] + "--" + newPairComp[1])
                else:
                    pairs.append(newPairComp[1] + "-r-" + newPairComp[0])
            else:
                pairs.append(pair)
        crowd["relations_noOffset"].iloc[i] = "\n".join(pairs)
        
        #time.sleep(35)

    
crowd.to_csv("crowdflower/causal_relations_main_noOffset.csv", quotechar='"', index=False)
