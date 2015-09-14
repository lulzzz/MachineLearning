
from __future__ import print_function # adopt the python3 syntax for printing
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3
import csv
import sys
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')


infile = 'atos_txt.csv'
outfile = 'atos_cluster.csv'
docids = []
descriptions = []
years = []
cluster_out = []

# load nltk's English stopwords as variable called 'stopwords'
stopwords = nltk.corpus.stopwords.words('english')
# take out generic public sector tendering words
stopwords.extend(['tender','tenders','require','required','requires','invite','supply','supplier','invited','deliver','delivery','provide','provides','provided','contract','contractor','services','service','services','including','public','council','councils','management','business','provision','maintenance', 'nuts', 'framework','place','main','uk','category','national','tendering','include','new'])
#extend common words in the analysis
#stopwords.extend(['security', 'services', 'building', 'controls']) 
# load nltk's SnowballStemmer as variabled 'stemmer'
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")


# Below I define two functions:
# tokenize_and_stem: tokenizes (splits the synopsis into a list of its respective words (or tokens) and also stems each token
# tokenize_only: tokenizes the synopsis only
# I use both these functions to create a dictionary which becomes important in case I want to use stems for an algorithm, 
# but later convert stems back to their full words for presentation purposes. Guess what, I do want to do that!

# here I define a tokenizer and stemmer which returns the set of stems in the text that it is passed

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


with open(infile, 'rb') as fp_in, open(outfile, 'wb') as fp_out:
    reader = csv.reader(fp_in, delimiter=",")
    writer = csv.writer(fp_out, delimiter=";") # set delimiter so that we just get a single string as the cluster 

    for row in reader:
    	if row[2] is not None:  # filters out tenders without a description
        	desc = str(row[3])
        	desc = desc.lower()
        	desc = "".join(i for i in desc if i not in ('!','.',':',';','-','"',"'",'}','{','#','*')) # go through each letter and remove punctuation

        	desc_list = desc.split() # split into words
        	desc_clean = ' '.join([i for i in desc_list if i not in stopwords]) # remove stopwords

        	docids.append(row[1])
        	years.append(row[2])
        	descriptions.append(desc_clean)

    #not super pythonic, no, not at all.
    #use extend so it's a big flat list of vocab
    totalvocab_stemmed = []
    totalvocab_tokenized = []
    for i in descriptions:
        allwords_stemmed = tokenize_and_stem(i) #for each item in 'synopses', tokenize/stem
        totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
    
        allwords_tokenized = tokenize_only(i)
        totalvocab_tokenized.extend(allwords_tokenized)

        # Using these two lists, I create a pandas DataFrame with the stemmed vocabulary as the index and the tokenized words as the column. 
        # The benefit of this is it provides an efficient way to look up a stem and return a full token. The downside here is that stems to tokens are one to many: 
        # the stem 'run' could be associated with 'ran', 'runs', 'running', etc. For my purposes this is fine--I'm perfectly happy returning the first token 
        # associated with the stem I need to look up.
        vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
        #print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')

    print(vocab_frame.head())
    print()
    print()



    from sklearn.feature_extraction.text import TfidfVectorizer
    #define vectorizer parameters
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, max_features=200000,
    	min_df=0.05, stop_words='english',
    	use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,2))

    tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions) #fit the vectorizer to synopses
    print(tfidf_matrix.shape)

    terms = tfidf_vectorizer.get_feature_names()

    from sklearn.metrics.pairwise import cosine_similarity
    dist = 1 - cosine_similarity(tfidf_matrix)
    print()
    print()

    from sklearn.cluster import KMeans
    num_clusters = 1
    km = KMeans(n_clusters=num_clusters)
    km.fit(tfidf_matrix)
    clusters = km.labels_.tolist()

    from sklearn.externals import joblib


    #uncomment the below to save your model 
    #since I've already run my model I am loading from the pickle

    joblib.dump(km,  'atos_cluster.pkl')
    km = joblib.load('atos_cluster.pkl')
    clusters = km.labels_.tolist()

    tenders = { 'docid': docids, 'year': years, 'description': descriptions, 'cluster': clusters }
    frame = pd.DataFrame(tenders, index = [clusters] , columns = ['docid', 'cluster', 'year'])

    print(frame['cluster'].value_counts()) #number of films per cluster (clusters from 0 to 4)


    print("Top terms per cluster:")
    print()
    #sort cluster centers by proximity to centroid
    order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

    for i in range(num_clusters):
    	print("Cluster %d words:" % i, end='')

    	for ind in order_centroids[i, :60]: #replace 6 with n words per cluster
    		cluster_word = vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore')
    		cluster_out.append(cluster_word)

    	writer.writerow(cluster_out)
    	print(cluster_out)
	
		#print("Cluster %d docids:" % i, end='')
		#for docid in frame.ix[i]['docid'].values.tolist():
		#	print(' %s,' % docid, end='')
		#print() #add whitespace
		#print() #add whitespace
    

         