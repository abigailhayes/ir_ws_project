# Read in pooled data relevance annotations. Will be a file with the document ID and a number for the relevance.
pooled_data

# Then want to loop through the ranked dictionary produced by one of the methods to add on the ranking.
for key, value in ranking_dict:
    if key in pooled_data["id"]:
        pooled_data["ranking"] = value
        
# Now to compute the Discounted Cumulative Gain
pooled_data["dcg_work"] = pooled_data["relevance"]/log(pooled_data["ranking"]+1, base=2)

# The Ideal DCG is just based on the pooled data
pooled_data["idcg_rank"] = pooled_data["relevance"].rank(ascending=False)
pooled_data["idcg_work"] = pooled_data["relevance"]/log(pooled_data["idcg_rank"]+1, base=2)

# Now can calculated the normalised DCG
pooled_data["ndcg"] = pooled_data["dcg_work"]/pooled_data["idcg_work"]
