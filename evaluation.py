import pandas as pd
import math
import os
from collections import defaultdict
from statistics import mean
from bm25 import bm25
from VSM_code_v2 import vsm
from baseline import baseline

def eval_single(rel_dict, pooled_path, take_mean=True):
    
    # Read in pooled data relevance annotations. Will be a file with the document ID and a number for the relevance.
    pooled_data = pd.read_csv(pooled_path)
    pooled_data["Document"] = pooled_data['Document'].str.replace("\\'",'')
    pooled_data["Document"] = pooled_data['Document'].str.replace("\\‘",'')
    pooled_data["idcg_rank"] = pooled_data.groupby("Query")["Relevance"].rank(ascending=False, method="first")
    
    # Handling getting a ranking for the dictionary with relevance judgements, only consider docs in pooled data
    ranking_dict = {}
    for query, value in rel_dict.items():
        ranking_dict[query] = {key: rank for rank, key in enumerate(sorted(value, key=value.get, reverse=True), 1)}
    
    # Convert pooled data to relevance and ideal ranking dictionaries
    pooled_dict = defaultdict(dict)
    ideal_dict = defaultdict(dict)
    for i, row in pooled_data.iterrows():
        pooled_dict[row.Query][row.Document] = row.Relevance
        ideal_dict[row.Query][row.Document] = row.idcg_rank
        
            
    # Now to compute the Discounted Cumulative Gain and Ideal DCG contribution for each query and document pair
    dcg_dict = defaultdict(dict)
    idcg_dict = defaultdict(dict)
    for query, doc_rel in pooled_dict.items():
        for doc, relevance in doc_rel.items():
            dcg_dict[query][doc] = relevance/math.log2(ranking_dict[query][doc]+1)
            idcg_dict[query][doc] = relevance/math.log2(ideal_dict[query][doc]+1)
    
    # Calculating the nDCG for each query        
    ndcg_dict = {}
    for query, doc_val in dcg_dict.items():
        ndcg_dict[query] = sum(doc_val.values())/sum(idcg_dict[query].values())
    
    if take_mean:
        return(mean(ndcg_dict.values()))
    
    return ndcg_dict

def all_eval():
    # Filenames
    directory = os.getcwd()
    doc_nostem_nostop = directory+"/Preprocessed&Translation/PPTranslatedAbstract_Title_WithoutStopWithoutStem.csv"
    doc_nostem_stop = directory+"/Preprocessed&Translation/PPTranslatedAbstract_Title_WithStopWithoutStem.csv"
    doc_stem_nostop = directory+"/Preprocessed&Translation/PPTranslatedAbstract_Title_WithoutStopWithStem.csv"
    doc_stem_stop = directory+"/Preprocessed&Translation/PPTranslatedAbstract_Title_WithStopWithStem.csv"
    query_stem = directory+"/Preprocessed&Translation/PPTranslatedQueryWithStem.csv"
    query_nostem = directory+"/Preprocessed&Translation/PPTranslatedQueryWithoutStem.csv"
    pooled_path = directory+"/pooling_judgements.csv"
    
    output = pd.DataFrame(columns=['nostem_nostop','nostem_stop','stem_nostop','stem_stop'],
                          index=['baseline', 'bm25', 'vsm'])
    
    # VSM
    output.loc[["vsm"],["nostem_nostop"]]=eval_single(vsm(doc_nostem_nostop, query_nostem), pooled_path)
    output.loc[["vsm"],["nostem_stop"]]=eval_single(vsm(doc_nostem_stop, query_nostem), pooled_path)
    output.loc[["vsm"],["stem_nostop"]]=eval_single(vsm(doc_stem_nostop, query_stem), pooled_path)
    output.loc[["vsm"],["stem_stop"]]=eval_single(vsm(doc_stem_stop, query_stem), pooled_path)
    
    # Read in files for baseline and BM25
    docnono = pd.read_csv(filepath_or_buffer=doc_nostem_nostop, converters={"Preprocessed_Abstract": lambda x: x.strip("[]").replace("'","").split(", ")})
    docnoyes = pd.read_csv(filepath_or_buffer=doc_nostem_stop, converters={"Preprocessed_Abstract": lambda x: x.strip("[]").replace("'","").split(", ")})
    docyesno = pd.read_csv(filepath_or_buffer=doc_stem_nostop, converters={"Preprocessed_Abstract": lambda x: x.strip("[]").replace("'","").split(", ")})
    docyesyes = pd.read_csv(filepath_or_buffer=doc_stem_stop, converters={"Preprocessed_Abstract": lambda x: x.strip("[]").replace("'","").split(", ")})
    queryyes = pd.read_csv(filepath_or_buffer=query_stem, converters={"Preprocessing": lambda x: x.strip("[]").replace("'","").split(", "), "candidates": lambda x: x.strip("[]").replace("'","").split(", ")})
    queryno = pd.read_csv(filepath_or_buffer=query_nostem, converters={"Preprocessing": lambda x: x.strip("[]").replace("'","").split(", "), "candidates": lambda x: x.strip("[]").replace("'","").split(", ")})
    
    # Baseline
    output.loc[["baseline"],["nostem_nostop"]]=eval_single(baseline(docnono, queryno), pooled_path)
    output.loc[["baseline"],["nostem_stop"]]=eval_single(baseline(docnoyes, queryno), pooled_path)
    output.loc[["baseline"],["stem_nostop"]]=eval_single(baseline(docyesno, queryyes), pooled_path)
    output.loc[["baseline"],["stem_stop"]]=eval_single(baseline(docyesyes, queryyes), pooled_path)
    
    # BM25
    output.loc[["bm25"],["nostem_nostop"]]=eval_single(bm25(docnono, queryno), pooled_path)
    output.loc[["bm25"],["nostem_stop"]]=eval_single(bm25(docnoyes, queryno), pooled_path)
    output.loc[["bm25"],["stem_nostop"]]=eval_single(bm25(docyesno, queryyes), pooled_path)
    output.loc[["bm25"],["stem_stop"]]=eval_single(bm25(docyesyes, queryyes), pooled_path)
    
    return output
    

    
