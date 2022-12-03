import pandas as pd
import math
from collections import defaultdict
from statistics import mean

def eval_single(rel_dict, pooled_path):
    
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
            print(ranking_dict[query][doc]+1)
            idcg_dict[query][doc] = relevance/math.log2(ideal_dict[query][doc]+1)
    
    # Calculating the nDCG for each query        
    ndcg_dict = {}
    for query, doc_val in dcg_dict.items():
        print(doc_val.values(), " and ", idcg_dict[query].values())
        ndcg_dict[query] = sum(doc_val.values())/sum(idcg_dict[query].values())
    
    return(mean(ndcg_dict.values()))

