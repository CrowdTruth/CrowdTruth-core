#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 11:39:03 2018

@author: oanainel
"""

def compute_precision(true_positive, false_positive):
    """ Function to compute Precision"""
    if true_positive == 0:
        return 0
    return float(true_positive) / float(true_positive + false_positive)

def compute_recall(true_positive, false_negative):
    """ Function to compute Recall"""
    if true_positive == 0:
        return 0
    return float(true_positive) / float(true_positive + false_negative)

def compute_accuracy(true_positive, true_negative, false_positive, false_negative):
    """ Function to compute Accuracy"""
    if true_positive + true_negative == 0:
        return 0
    return float(true_positive + true_negative) / \
           float(true_positive + true_negative + false_positive + false_negative)

def compute_f1score(precision, recall):
    """ Function to compute F1 Score"""
    if precision * recall == 0:
        return 0
    return float(2 * precision * recall) / float(precision + recall)

def compute_crowd_performance(df_crowd_results, crowd_score_column, experts_score_column):
    """ Function to evaluate the answers of the crowd at each posible crowd score threshold"""
    rows = []
    header = ["Thresh", "TP", "TN", "FP", "FN", "Precision", "Recall", "Accuracy", "F1-score"]
    rows.append(header)

    precision = 0.0
    recall = 0.0
    accuracy = 0.0
    f1score = 0.0

    for i in range(5, 101, 5):
        row = []
        thresh = i / 100.0

        true_pos, true_neg, false_pos, false_neg = count_positives_and_negatives(df_crowd_results, \
                                                  crowd_score_column, experts_score_column, thresh)

        precision = compute_precision(true_pos, false_pos)
        recall = compute_recall(true_pos, false_neg)
        accuracy = compute_accuracy(true_pos, true_neg, false_pos, false_neg)
        f1score = compute_f1score(precision, recall)

        row = [thresh, true_pos, true_neg, false_pos, false_neg, \
               precision, recall, accuracy, f1score]
        rows.append(row)

    return rows

def compute_majority_vote(df_crowd_results, crowd_score_column, experts_score_column, no_workers):
    """ Function to evaluate the answers of the crowd using majority vote"""

    true_pos, true_neg, false_pos, false_neg = count_positives_and_negatives(df_crowd_results, \
                                            crowd_score_column, experts_score_column, no_workers)

    precision = compute_precision(true_pos, false_pos)
    recall = compute_recall(true_pos, false_neg)
    accuracy = compute_accuracy(true_pos, true_neg, false_pos, false_neg)
    f1score = compute_f1score(precision, recall)

    return true_pos, true_neg, false_pos, false_neg, \
            precision, recall, accuracy, f1score

def count_positives_and_negatives(df_crowd_results, crowd_score_col, experts_score_col, crowd_value):
    """ Help function for reading the crowd results """
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for j in range(len(df_crowd_results.index)):
        if df_crowd_results[crowd_score_col].iloc[j] >= crowd_value:
            if df_crowd_results[experts_score_col].iloc[j] == 1:
                true_positive = true_positive + 1
            else:
                false_positive = false_positive + 1
        else:
            if df_crowd_results[experts_score_col].iloc[j] == 1:
                false_negative = false_negative + 1
            else:
                true_negative = true_negative + 1
    return true_positive, true_negative, false_positive, false_negative
