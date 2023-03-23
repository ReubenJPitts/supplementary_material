

### 0 ### necessary imports

# import pandas
import pandas as pd

# import the CEIPoM csv files
links = pd.read_csv("CEIPoM/links.csv",encoding="utf-16")
texts = pd.read_csv("CEIPoM/texts.csv",encoding="utf-16")
sentences = pd.read_csv("CEIPoM/sentences.csv",encoding="utf-16")
tokens = pd.read_csv("CEIPoM/tokens.csv",encoding="utf-16")
analysis = pd.read_csv("CEIPoM/analysis.csv",encoding="utf-16")


### 1 ### merge a single CEIPoM dataframe

# get a single link per Trismegistos ID
linkstemp = links.drop_duplicates(subset="Text_ID")
linkstemp = linkstemp.drop_duplicates(subset="Trismegistos_ID")

# merge the CEIPoM files together
corpus = tokens.merge(analysis, on="Token_ID", how="left", suffixes=("","_delete"))
corpus = corpus.merge(sentences, on="Sentence_ID", suffixes=("","_delete"))
corpus = corpus.merge(texts, on="Text_ID", suffixes=("","_(text)"))
corpus = corpus.merge(linkstemp, on="Text_ID", how="left", suffixes=("","_delete"))


### 2 ### sort the dataframe out

# delete duplicate columns
columns = [i for i in list(corpus.columns) if i.find("delete")==-1]
corpus = corpus[columns]

# sort the dataframe and fill NaN values
corpus = corpus.sort_values(by=["Text_ID","Sentence_position","Token_position"])
corpus["Trismegistos_ID"] = corpus["Trismegistos_ID"].fillna(0).astype(int)
CEIPoM = corpus.fillna("")

# drop duplicate morphological analyses
CEIPoM = CEIPoM.drop_duplicates(subset="Token_ID")
CEIPoM["Token_IDs"] = CEIPoM["Token_ID"]
CEIPoM = CEIPoM.set_index('Token_IDs')
CEIPoM.index.name = None


### 3 ### assign a chronological stratification to the Iguvine Tables

dbefore = list(CEIPoM["Date_before"])
dafter = list(CEIPoM["Date_after"])
for i in range(len(CEIPoM)):
	if str(CEIPoM.iloc[i]["Section"]).find("Latin alphabet") > -1:
		dbefore[i] = -150
		dafter[i] = -100
CEIPoM = CEIPoM.copy()
CEIPoM["Date_before"] = dbefore
CEIPoM["Date_after"] = dafter
CEIPoM = CEIPoM.copy()

