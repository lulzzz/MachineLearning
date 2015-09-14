import os
import scipy as sp
import sys
import sklearn.datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk.stem

class StemmedTfidfVectorizer(TfidfVectorizer):
	def build_analyzer(self):
		analyzer = super(TfidfVectorizer, self).build_analyzer()
		return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

all_data = sklearn.datasets.fetch_20newsgroups(subset='all')
groups = ['comp.graphics','comp.os.ms-windows.misc','comp.sys.ibm.pc.hardware','comp.sys.mac.hardware','comp.windows.x','sci.space']
train_data = sklearn.datasets.fetch_20newsgroups(subset='train', categories=groups)
test_data = sklearn.datasets.fetch_20newsgroups(subset='test', categories=groups)
english_stemmer = nltk.stem.SnowballStemmer('english')
vectorizer = StemmedTfidfVectorizer(min_df=10, max_df=0.5, stop_words='english', decode_error='ignore')
vectorized = vectorizer.fit_transform(train_data.data)
num_samples, num_features = vectorized.shape
num_clusters = 50
km = KMeans(n_custers=num_clusters, init='random', n_init=1, verbose=1, random_state=3)
km.fit(vectorized)
print("#samples: %d, #features: %d" % (num_samples, num_features))
print(km.labels)
print(km.labels_shape)