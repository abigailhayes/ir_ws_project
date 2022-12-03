# Information Retrieval and Web Search project

Link to project info: [https://clef-lilas.github.io](https://clef-lilas.github.io)

## Task description

The goal of Task 1 is supporting researchers find the most relevant documents regarding a head query. Participants are asked to define and implement their ranking approach for a multi-lingual candidate documents list. A good ranking should present users with the most relevant documents regarding a query on top of the result set. Multiple languages can be used to pose the query (e.g. English, German, French); regardless of the language used on the query, the retrieval can include candidate documents in other languages.

## Data

Most of the data for the project is provided in 5gb jsonl files. We processed these on the supercomputer using [final/functions_extract_abstracts.py](functions_extract_abstracts.py). The version we used in the end is from an earlier commit. The data extracted was [output/output_cluster.csv](output_cluster.csv).

The formatting of the cluster output was a bit messy, so [final/cluster_to_useful.py](cluster_to_useful.py) reorganised it to [output/output_narrow.csv](output_narrow.csv).

The abstracts, titles and querys were then preprocessed and translated to give files in the 'Preprocessed' folder.

## Models

We have implemented two models; [bm25.py](bm25.py) and [vsm.py](vsm.py). The vsm function takes filepaths as input, whilst the bm25 needs the files read in first as demonstrated in [run_bm25.py](run_bm25.py).

## Evaluation

For evaluation, we implemented nDCG in [final/evaluation.py](evaluation.py). The first input should be a dictionary of dictionaries. For the bm25, the final part of the function code needs to be commented out to give this. The second input to the evaluation function is a filepath to [pooled_judgements.csv](pooled_judgements.csv).

For pooling, we selected 10 queries and then for each included the top 5 documents from bm25 and vsm. We annotated these by hand.

