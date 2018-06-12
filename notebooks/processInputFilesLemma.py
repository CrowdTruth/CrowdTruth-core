#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 10:05:56 2018

@author: oanainel
"""

import pandas as pd
import numpy as np

from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')


crowd = pd.read_csv("crowdflower/causal_relations_main_noOffset.csv")

crowd["pair1_lemma"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair2_lemma"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair3_lemma"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair4_lemma"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair5_lemma"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["pair6_lemma"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)
crowd["relations_lemma"] = pd.Series(np.random.randn(len(crowd.index)), index=crowd.index)

#st = StanfordPOSTagger('english-bidirectional-distsim.tagger')
#st.tag('What is the airspeed of an unladen swallow ?'.split())

for i in range(len(crowd.index)):
    print(i)
    if pd.isnull(crowd["pair1_noOffset"].iloc[i]) != True :
        newValueComp = crowd["pair1_noOffset"].iloc[i].split(", ")
        lemmas = ""
        output1 = nlp.annotate(newValueComp[0], properties={
                'annotators': 'lemma',
                'outputFormat': 'json'
                })
        output2 = nlp.annotate(newValueComp[1], properties={
                'annotators': 'lemma',
                'outputFormat': 'json'
                })
        lemma1 = []
        for term1 in output1['sentences']:
            for tokens in term1['tokens']:
                lemma1.append(tokens['lemma'])
                
        lemma2 = []
        for term2 in output2['sentences']:
            for tokens in term2['tokens']:
                lemma2.append(tokens['lemma'])
                
        lemmas = " ".join(lemma1) + ", " + " ".join(lemma2)
    
        crowd["pair1_lemma"].iloc[i] = lemmas
    else:
        crowd["pair1_lemma"].iloc[i] = crowd["pair1_noOffset"].iloc[i]
        
    if pd.isnull(crowd["pair2_noOffset"].iloc[i]) != True :
        newValueComp = crowd["pair2_noOffset"].iloc[i].split(", ")
        lemmas = ""
        output1 = nlp.annotate(newValueComp[0], properties={
                'annotators': 'lemma',
                'outputFormat': 'json'
                })
        output2 = nlp.annotate(newValueComp[1], properties={
                'annotators': 'lemma',
                'outputFormat': 'json'
                })
        lemma1 = []
        for term1 in output1['sentences']:
            for tokens in term1['tokens']:
                lemma1.append(tokens['lemma'])
                
        lemma2 = []
        for term2 in output2['sentences']:
            for tokens in term2['tokens']:
                lemma2.append(tokens['lemma'])
                
        lemmas = " ".join(lemma1) + ", " + " ".join(lemma2)
    
        crowd["pair2_lemma"].iloc[i] = lemmas
    else:
        crowd["pair2_lemma"].iloc[i] = crowd["pair2_noOffset"].iloc[i]
        
    if pd.isnull(crowd["pair3_noOffset"].iloc[i]) != True :
        newValueComp = crowd["pair3_noOffset"].iloc[i].split(", ")
        lemmas = ""
        output1 = nlp.annotate(newValueComp[0], properties={
                'annotators': 'lemma',
                'outputFormat': 'json'
                })
        output2 = nlp.annotate(newValueComp[1], properties={
                'annotators': 'lemma',
                'outputFormat': 'json'
                })
        lemma1 = []
        for term1 in output1['sentences']:
            for tokens in term1['tokens']:
                lemma1.append(tokens['lemma'])
                
        lemma2 = []
        for term2 in output2['sentences']:
            for tokens in term2['tokens']:
                lemma2.append(tokens['lemma'])
                
        lemmas = " ".join(lemma1) + ", " + " ".join(lemma2)
    
        crowd["pair3_lemma"].iloc[i] = lemmas
    else:
        crowd["pair3_lemma"].iloc[i] = crowd["pair3_noOffset"].iloc[i]
        
    if pd.isnull(crowd["pair4_noOffset"].iloc[i]) != True :
        newValueComp = crowd["pair4_noOffset"].iloc[i].split(", ")
        lemmas = ""
        output1 = nlp.annotate(newValueComp[0], properties={
                'annotators': 'lemma',
                'outputFormat': 'json'
                })
        output2 = nlp.annotate(newValueComp[1], properties={
                'annotators': 'lemma',
                'outputFormat': 'json'
                })
        lemma1 = []
        for term1 in output1['sentences']:
            for tokens in term1['tokens']:
                lemma1.append(tokens['lemma'])
                
        lemma2 = []
        for term2 in output2['sentences']:
            for tokens in term2['tokens']:
                lemma2.append(tokens['lemma'])
                
        lemmas = " ".join(lemma1) + ", " + " ".join(lemma2)
    
        crowd["pair4_lemma"].iloc[i] = lemmas
    else:
        crowd["pair4_lemma"].iloc[i] = crowd["pair4_noOffset"].iloc[i]
        
    if pd.isnull(crowd["pair5_noOffset"].iloc[i]) != True :
        newValueComp = crowd["pair5_noOffset"].iloc[i].split(", ")
        lemmas = ""
        output1 = nlp.annotate(newValueComp[0], properties={
                'annotators': 'lemma',
                'outputFormat': 'json'
                })
        output2 = nlp.annotate(newValueComp[1], properties={
                'annotators': 'lemma',
                'outputFormat': 'json'
                })
        lemma1 = []
        for term1 in output1['sentences']:
            for tokens in term1['tokens']:
                lemma1.append(tokens['lemma'])
                
        lemma2 = []
        for term2 in output2['sentences']:
            for tokens in term2['tokens']:
                lemma2.append(tokens['lemma'])
                
        lemmas = " ".join(lemma1) + ", " + " ".join(lemma2)
    
        crowd["pair5_lemma"].iloc[i] = lemmas
    else:
        crowd["pair5_lemma"].iloc[i] = crowd["pair5_noOffset"].iloc[i]
        
    if pd.isnull(crowd["pair6_noOffset"].iloc[i]) != True :
        newValueComp = crowd["pair6_noOffset"].iloc[i].split(", ")
        lemmas = ""
        output1 = nlp.annotate(newValueComp[0], properties={
                'annotators': 'lemma',
                'outputFormat': 'json'
                })
        output2 = nlp.annotate(newValueComp[1], properties={
                'annotators': 'lemma',
                'outputFormat': 'json'
                })
        lemma1 = []
        for term1 in output1['sentences']:
            for tokens in term1['tokens']:
                lemma1.append(tokens['lemma'])
                
        lemma2 = []
        for term2 in output2['sentences']:
            for tokens in term2['tokens']:
                lemma2.append(tokens['lemma'])
                
        lemmas = " ".join(lemma1) + ", " + " ".join(lemma2)
    
        crowd["pair6_lemma"].iloc[i] = lemmas
    else:
        crowd["pair6_lemma"].iloc[i] = crowd["pair6_noOffset"].iloc[i]
        
    if (crowd["relations"].iloc[i] == "no_relation"):
        crowd["relations_lemma"].iloc[i] = "no_relation"
    else:
        crowdPairs = crowd["relations_noOffset"].iloc[i].split("\n")
        pairs = []
        for pair in crowdPairs:
            #pair = pair.lower()
            if '-r-' in str(pair):
                newPairComp = pair.split("-r-")
                lemmas = ""
                output1 = nlp.annotate(newPairComp[0], properties={
                        'annotators': 'lemma',
                        'outputFormat': 'json'
                        })
                output2 = nlp.annotate(newPairComp[1], properties={
                        'annotators': 'lemma',
                        'outputFormat': 'json'
                        })
                lemma1 = []
                for term1 in output1['sentences']:
                    for tokens in term1['tokens']:
                        lemma1.append(tokens['lemma'])
                        
                lemma2 = []
                for term2 in output2['sentences']:
                    for tokens in term2['tokens']:
                        lemma2.append(tokens['lemma'])
                        
                lemmas = " ".join(lemma1) + "-r-" + " ".join(lemma2)
                pairs.append(lemmas)
            elif '--' in str(pair):
                newPairComp = pair.split("--")
                lemmas = ""
                output1 = nlp.annotate(newPairComp[0], properties={
                        'annotators': 'lemma',
                        'outputFormat': 'json'
                        })
                output2 = nlp.annotate(newPairComp[1], properties={
                        'annotators': 'lemma',
                        'outputFormat': 'json'
                        })
                lemma1 = []
                for term1 in output1['sentences']:
                    for tokens in term1['tokens']:
                        lemma1.append(tokens['lemma'])
                        
                lemma2 = []
                for term2 in output2['sentences']:
                    for tokens in term2['tokens']:
                        lemma2.append(tokens['lemma'])
                        
                lemmas = " ".join(lemma1) + "--" + " ".join(lemma2)
                pairs.append(lemmas)
            else:
                pairs.append(pair)
        crowd["relations_lemma"].iloc[i] = "\n".join(pairs)
        
        #time.sleep(35)

    
crowd.to_csv("crowdflower/causal_relations_main_noOffset_lemma.csv", quotechar='"', index=False)
