#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 3 16:02:00 2022

@author: simonkral
"""


def vsm(document_csv_file, query_csv_file):
    ######## IMPORT LIBRARIES #########

    import pandas as pd
    import numpy as np
    from numpy.linalg import norm
    import nltk

    ######## IMPORT DATA #########

    d_raw_df = pd.read_csv(document_csv_file)
    q_raw_df = pd.read_csv(query_csv_file)

    q_df = q_raw_df.get(['qid:', 'Preprocessed_Query'])
    q_df.rename(columns={'qid:': 'qid'}, inplace=True)
    q_df.rename(columns={'Preprocessed_Query': 'qstr'}, inplace=True)

    d_df = d_raw_df.get(['qid:', 'candidates', 'Preprocessed_Abstract', 'Preprocessed_Title'])
    d_df.rename(columns={'qid:': 'qid'}, inplace=True)
    d_df.rename(columns={'candidates': 'docid'}, inplace=True)
    d_df.rename(columns={'Preprocessed_Abstract': 'abstract'}, inplace=True)
    d_df.rename(columns={'Preprocessed_Title': 'title'}, inplace=True)

    ######## PREPARING DICTIONARIES #########

    # Initialize conf_dict dictionary for query-document confidence scores: conf_dict[qid][docid] = conf_score

    # Query dictionary q_dict: qid -> qstr,
    # Document dictionary d_dict: docid -> abstract
    # Title dictionary: docid -> title

    conf_dict = dict()

    q_dict = dict()
    d_dict = dict()
    t_dict = dict()

    for i in range(len(d_df)):
        ## conf_dict ##
        if d_df.qid[i] in list(conf_dict.keys()):
            conf_dict[d_df.qid[i]].update({d_df.docid[i]: 0})
        else:
            conf_dict[d_df.qid[i]] = {d_df.docid[i]: 0}

        ## d_dict & t_dict ##
        d_dict[d_df.docid[i]] = eval(d_df.abstract[i])
        t_dict[d_df.docid[i]] = eval(d_df.title[i])

    ## q_dict ##
    for i in range(len(q_df)):
        q_dict[q_df.qid[i]] = eval(q_df.qstr[i])

    ######## VSM-RANKING (FOR ABSTRACT) #########

    f_td = 0  # number of occurences of word t in doc d
    max_f_td = 0  # number of occurences of the most frequent word in doc d

    for q_id in list(q_dict.keys()):
        if len(q_dict[q_id]) == 1:  # diff. of cases: 1w query -> tf-value
            qstr = q_dict[q_id][0]
            for doc_id in list(conf_dict[q_id].keys()):

                f_td = d_dict[doc_id].count(qstr)  # get raw frequency of query

                allWordDist = nltk.FreqDist(d_dict[doc_id])
                # get 10 most frequent words in document
                mostCommon = allWordDist.most_common(10)

                try:
                    # get raw frequency of most frequent word
                    max_f_td = mostCommon[0][1]
                except:
                    max_f_td = 0
                    conf_dict[q_id][doc_id] = -1

                if f_td > 0:
                    conf_dict[q_id][doc_id] = (1 + np.log10(f_td))/(1 + np.log10(max_f_td))  # calc. & save tf-value

                # idf-value in this case irrelevant, as we rank according to the tf-value (idf-multiplier identical
                # for all tf-values)
        else:  # diff. of cases: mult. w query -> cos. sim. btw tf-idf-vecs
            # initialize idf_vector = (0,...,0)
            idf_vec = np.zeros(len(q_dict[q_id]))
            # set query_vector = (1,...,1)
            query_vec = np.ones(len(q_dict[q_id]))

            # loop over documents & query terms
            for doc_id in list(conf_dict[q_id].keys()):
                conf_dict[q_id][doc_id] = np.zeros(len(q_dict[q_id]))

                for i, q_t in enumerate(q_dict[q_id]):
                    f_td = d_dict[doc_id].count(q_t)

                    allWordDist = nltk.FreqDist(d_dict[doc_id])
                    mostCommon = allWordDist.most_common(10)

                    try:
                        max_f_td = mostCommon[0][1]
                    except:
                        max_f_td = 0

                    if f_td > 0:
                        # count occurrences of query term over the whole doc. collection
                        idf_vec[i] += 1
                        conf_dict[q_id][doc_id][i] = (1 + np.log10(f_td))/(1 + np.log10(max_f_td))  # collect tf-vector

            for i in range(len(q_dict[q_id])):
                if idf_vec[i] != 0:
                    # calc. actual idf-vector
                    idf_vec[i] = np.log10(100/idf_vec[i])

            for doc_id in list(conf_dict[q_id].keys()):
                conf_dict[q_id][doc_id] = conf_dict[q_id][doc_id] * idf_vec  # calc. tf-idf-vector

                # calc. cosine similarity btw. query vector & tf-idf-vector
                if (norm(query_vec)*norm(conf_dict[q_id][doc_id])) == 0:
                    conf_dict[q_id][doc_id] = 0
                else:
                    conf_dict[q_id][doc_id] = np.dot(
                        conf_dict[q_id][doc_id], query_vec)/(norm(query_vec)*norm(conf_dict[q_id][doc_id]))

                if len(d_dict[doc_id]) == 0:
                    conf_dict[q_id][doc_id] = -1

    ######## VSM-RANKING (FOR TITLE - IF NO ABSTRACT) #########

    f_td = 0  # number of occurences of word t in title of doc d
    max_f_td = 0  # number of occurences of the most frequent word in title of doc d
    
    for q_id in list(q_dict.keys()):
        if len(q_dict[q_id]) == 1:  # diff. of cases: 1w query -> tf-value
            qstr = q_dict[q_id][0]
            for doc_id in list(conf_dict[q_id].keys()):

                if len(d_dict[doc_id]) == 0:
                    # get raw frequency of query
                    f_td = t_dict[doc_id].count(qstr)

                    allWordDist = nltk.FreqDist(t_dict[doc_id])
                    # get 10 most frequent words in title
                    mostCommon = allWordDist.most_common(10)

                    try:
                        # get raw frequency of most frequent word
                        max_f_td = mostCommon[0][1]
                    except:
                        max_f_td = 0
                        conf_dict[q_id][doc_id] = -1

                    if f_td > 0:
                        conf_dict[q_id][doc_id] = 0.00001*(1 + np.log10(f_td))/(1 + np.log10(max_f_td))  # calc. & save tf-value

                # idf-value in this case irrelevant, as we rank according to the tf-value (idf-multiplier identical
                # for all tf-values)
        else:  # diff. of cases: mult. w query -> cos. sim. btw tf-idf-vecs
            # initialize idf_vector = (0,...,0)
            idf_vec = np.zeros(len(q_dict[q_id]))
            # set query_vector = (1,...,1)
            query_vec = np.ones(len(q_dict[q_id]))

            # loop over titles & query terms
            for doc_id in list(conf_dict[q_id].keys()):
                
                if len(d_dict[doc_id]) == 0:
                    conf_dict[q_id][doc_id] = np.zeros(len(q_dict[q_id]))
                
                for i, q_t in enumerate(q_dict[q_id]):
                    f_td = t_dict[doc_id].count(q_t)

                    allWordDist = nltk.FreqDist(t_dict[doc_id])
                    mostCommon = allWordDist.most_common(10)

                    try:
                        max_f_td = mostCommon[0][1]
                    except:
                        max_f_td = 0

                    if f_td > 0:
                        # count occurrences of query term over the whole doc. collection
                        idf_vec[i] += 1
                        if len(d_dict[doc_id]) == 0:
                            conf_dict[q_id][doc_id][i] = (1 + np.log10(f_td))/(1 + np.log10(max_f_td))  # collect tf-vector
                
            for i in range(len(q_dict[q_id])):
                if idf_vec[i] != 0:
                    # calc. actual idf-vector
                    idf_vec[i] = np.log10(100/idf_vec[i])

            for doc_id in list(conf_dict[q_id].keys()):
                if len(d_dict[doc_id]) == 0:
                    # calc. tf-idf-vector
                    conf_dict[q_id][doc_id] = conf_dict[q_id][doc_id]*idf_vec
    
                    # calc. cosine similarity btw. query vector & tf-idf-vector
                    if (norm(query_vec)*norm(conf_dict[q_id][doc_id])) == 0:
                        conf_dict[q_id][doc_id] = 0
                    else:
                        conf_dict[q_id][doc_id] = 0.00001*np.dot(conf_dict[q_id][doc_id], query_vec)/(norm(query_vec)*norm(conf_dict[q_id][doc_id]))
                    
                    if len(t_dict[doc_id]) == 0:
                        conf_dict[q_id][doc_id] = -1
                    
    return(conf_dict)