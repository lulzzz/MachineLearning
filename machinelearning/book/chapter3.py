import os
from sklearn.feature_extraction.text import CountVectorizer
import scipy as sp
import sys
import nltk.stem

def dist_norm(v1, v2):
	v1_normalized = v1/sp.linalg.norm(v1.toarray())
	v2_normalized = v2/sp.linalg.norm(v2.toarray())
	delta = v1_normalized-v2_normalized
	return sp.linalg.norm(delta.toarray())

class StemmedCountVectorizer(CountVectorizer):
	"""docstring for ClassName"""
	def build_analyzer(self):
		analyzer = super(StemmedCountVectorizer, self).build_analyzer()
		return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))


DIR = 'data'
posts = [open(os.path.join(DIR, f)).read() for f in os.listdir(DIR)]
del posts[0]
english_stemmer = nltk.stem.SnowballStemmer('english')

vectorizer = StemmedCountVectorizer(min_df=1, stop_words='english')
X_train = vectorizer.fit_transform(posts)
num_samples, num_features = X_train.shape
print("#samples: %d, #features: %d" % (num_samples, num_features))
print(vectorizer.get_feature_names())

new_post = "imaging databases"
new_post_vec = vectorizer.transform([new_post])

best_doc = None
best_dist = sys.maxint
best_i = None

for i, post in enumerate(posts):
	if post == new_post:
		continue
	post_vec = X_train.getrow(i)
	d = dist_norm(post_vec, new_post_vec)
	print("==== Post %i with dist=%.2f: %s" %(i, d, post))
	if d<best_dist:
		best_dist = d
		best_i = i
	
print("Best post is %i with dist=%.2f"%(best_i, best_dist))


