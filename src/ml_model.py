import argparse
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize, sent_tokenize          
from nltk.stem.porter import PorterStemmer
from nltk import trigrams, bigrams
from collections import Counter
from nltk.corpus import stopwords as StopWords
import numpy as np
from gensim.models import word2vec

pathToBinVectors = '../../GoogleNews-vectors-negative300.bin'

class StemTokenizer(object):
     def __init__(self):
         self.wnl = PorterStemmer()
     def __call__(self, doc):
         return [self.wnl.stem(t) for t in word_tokenize(doc)]

def preprocess(file_list, tf=False, stopwords=False):
	sent_list = []
	words_sent = []
	bigram_sent = []
	trigram_sent = []
	gram_probs = Counter()
	total_features = 0

	# don't remove stopwords because probably important when talking about fake news
	# we can try tf vs simple unigram/bigram count
	if tf:
		tf_vectorizer = TfidfVectorizer(analyzer="word",
										ngram_range=(1,2),
										tokenizer=StemTokenizer(),
										string="english")
	else: 
		stemmer = PorterStemmer()
		punct = [',', '.', '"']

		for file in file_list:

			# split the files into sentences and score the difference of the sentences
			sent_list = sent_tokenize(file)

			for sentence in sent_list:
				# clean all the strings and standardize
				word_list = word_tokenize(sentence)
				word_list = [stemmer.stem(word) for word in word_list if word not in punct]
				word_list = [word.lower() for word in word_list]

				# get n_grams
				ngrams_3 = trigrams(word_list) 
				ngrams_2 = bigrams(word_list)

				# clean out stopwords after we get n_grams split them into the sentences to calc prob
				if stopwords:
					word_list = [word for word in word_list if word not in StopWords.words('english')]
				words_sent.append(word_list)

				for el in ngrams_3:
					trigram_sent.append(el)

				for el in ngrams_2:
					bigram_sent.append(el)

				# count occurences
				gram_probs.update(ngrams_3)
				gram_probs.update(ngrams_2)
				gram_probs.update(word_list)

	# turn all the counts into probabilities
	for key in gram_probs.keys():
		total_features += gram_probs[key]
		
	for key in gram_probs.keys():
		gram_probs[key] /= (float) (total_features)

	return words_sent, bigram_sent, trigram_sent, sent_list, gram_probs

def score_sentences(words_sent, bigram_sent, trigram_sent, sent_list, gram_probs):
	sent_probs = []

	for i in range(0, len(sent_list)):
		total_prob = 0
		feature_num = 0
		for j in range(0, len(words_sent[i])):
			total_prob += gram_probs[words_sent[i][j]]
			feature_num += 1
		for j in range(0, len(bigram_sent[i])):
			total_prob += gram_probs[bigram_sent[i][j]]
			feature_num += 1
		for j in range(0, len(trigram_sent[i])):
			total_prob += gram_probs[trigram_sent[i][j]]
			feature_num += 1
		sent_probs.append(total_prob/feature_num)

	return sent_probs

def get_highlight_sentences(sent_list, sent_probs, min_num=2, percent=0.2):
	sentence_num = (int)(len(sent_list)*0.2)
	highlights = []

	if min_num > sentence_num:
		sentence_num = min_num

	for i in range(0, sentence_num):
		max_index = np.argmax(sent_probs)
		highlights.append(sent_list[max_index]) 
		sent_probs[max_index] = 0

	return highlights

def write_json(highlights):
	obj = {"payload": highlights}

	with open("output.json", 'w') as f:
		line = json.dump(obj, f)
		f.write('\n')

def parse_json(filename):
	with open(filename, 'r') as f:
		json_obj = json.load(f)

	return [json_obj['target']], json_obj['cluster_list']

def main(args):
	# target_article, cluster_list = parse_json(args.filename) 
	
	# words_sent, bigram_sent, trigram_sent, sent_list, gram_probs = preprocess(target_article)
	# sent_probs = score_sentences(words_sent, bigram_sent, trigram_sent, sent_list, gram_probs)
	# target_highlights = get_highlight_sentences(sent_list, sent_probs)

	# words_sent, bigram_sent, trigram_sent, sent_list, gram_probs = preprocess(cluster_list)
	# sent_probs = score_sentences(words_sent, bigram_sent, trigram_sent, sent_list, gram_probs)
	# cluster_highlights = get_highlight_sentences(sent_list, sent_probs)

	print "Loading the data file... Please wait..."
	model1 = word2vec.Word2Vec.load_word2vec_format(pathToBinVectors, binary=True)
	print "Successfully loaded 3.6 G bin file!"

	write_json(highlights)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Let's find some fake news!")
	parser.add_argument("filename")
	args = parser.parse_args()
	main(args)