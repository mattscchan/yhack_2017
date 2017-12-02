import argparse
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize, sent_tokenize          
from nltk.stem.porter import PorterStemmer
from nltk import trigrams, bigrams
from collections import Counter
from nltk.corpus import stopwords as StopWords
import numpy as np
from gensim.models import KeyedVectors

pathToBinVectors = '../../GoogleNews-vectors-negative300.bin'

def ConvertVectorSetToVecAverageBased(vectorSet, ignore = []):
	if len(ignore) == 0: 
		return np.mean(vectorSet, axis = 0)
	else: 
		return np.dot(np.transpose(vectorSet),ignore)/sum(ignore)

def PhraseToVec(phrase_list):
	vectorSet = []
	for sentence in phrase_list:
		for aWord in wordsInPhrase:
			try:
				wordVector=model1[aWord]
				vectorSet.append(wordVector)
			except:
				pass
	return ConvertVectorSetToVecAverageBased(vectorSet)


def CosineSimilarity(vector1, vector2):
	cosine_similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
	try:
		if math.isnan(cosine_similarity):
			cosine_similarity=0
	except:
		cosine_similarity=0		
	return cosine_similarity

class StemTokenizer(object):
     def __init__(self):
         self.wnl = PorterStemmer()
     def __call__(self, doc):
         return [self.wnl.stem(t) for t in word_tokenize(doc)]

def preprocess(file_list, tf=False, stopwords=False):
	all_sent = []
	all_trigrams = []
	all_bigrams = []
	all_words = []
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
			bigram_sent = []
			trigram_sent = []
			words_sent = []
			sent_list = sent_tokenize(file)
			all_sent.append(sent_list)

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

			all_trigrams.append(trigram_sent)
			all_bigrams.append(bigram_sent)
			all_words.append(word_list)

	# turn all the counts into probabilities
	for key in gram_probs.keys():
		total_features += gram_probs[key]
		
	for key in gram_probs.keys():
		gram_probs[key] /= (float) (total_features)

	return all_words, all_bigrams, all_trigrams, all_sent, gram_probs

def score_sentences(all_words, all_bigrams, all_trigrams, all_sent, gram_probs):
	all_probs = []

	for file in range(0, len(all_sent)):
		sent_probs = []
		for i in range(0, len(all_sent[file])):
			total_prob = 0
			feature_num = 0
			for j in range(0, len(all_words[file][i])):
				total_prob += gram_probs[all_words[file][i][j]]
				feature_num += 1
			for j in range(0, len(all_bigrams[file][i])):
				total_prob += gram_probs[all_bigrams[file][i][j]]
				feature_num += 1
			for j in range(0, len(all_trigrams[file][i])):
				total_prob += gram_probs[all_trigrams[file][i][j]]
				feature_num += 1
			sent_probs.append(total_prob/feature_num)
		all_probs.append(sent_probs)

	return all_probs

def get_highlight_sentences(all_sent, all_words, all_probs, min_num=2, percent=0.2):
	highlights = []
	vector_words = []

	for file in range(0, len(all_sent)):
		sentence_num = (int)(len(all_sent[file])*0.2)
		per_file_highlights = []
		per_file_words = []

		if min_num > sentence_num:
			sentence_num = min_num

		if sentence_num > len(all_sent[file]):
			sentence_num = len(all_sent[file])

		for i in range(0, sentence_num):
			max_index = np.argmax(all_probs[file][i])
			per_file_highlights.append(all_sent[file][max_index]) 
			per_file_words.append(all_words[file][max_index])
			all_probs[file][max_index] = 0

		highlights.append(per_file_highlights)
		vector_words.append(per_file_words)

	return highlights, vector_words

def calculate_similarity(target_builder, cluster_builder, target_highlights):
	vec_scores = []
	max_diff = 100000000
	average_diff = 0
	target_vec = 0

	# populate all the mean scores now find the biggest diff and use as the baseline
	for file in cluster_builder:
		vec = PhraseToVec(file)
		vec_scores.append(vec)

	for i in range(0, len(cluster_builder)):
		for j in range(i+1, len(cluster_builder)):
			cosine_similarity = CosineSimilarity(vec_scores[i], vec_scores[j])
			average_diff += cosine_similarity

			if cosine_similarity < max_diff:
				max_diff = cosine_similarity


	for file in target_builder:
		target_vec = PhraseToVec(file)

	for i in range(0, len(cluster_builder))
		cosine_similarity = CosineSimilarity(vec_scores[i], target_vec)

		if cosine_similarity < max_diff:
			return target_highlights, 1

		if cosine_similarity < average_diff:
			return target_highlights, 0

		return [], -1

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
	print ("Loading the data file... Please wait...")
	model1 = KeyedVectors.load_word2vec_format(pathToBinVectors, binary=True)
	print ("Successfully loaded 3.6 G bin file!")

	target_article, cluster_list = parse_json(args.filename) 
	
	words_sent, bigram_sent, trigram_sent, sent_list, gram_probs = preprocess(target_article)
	sent_probs = score_sentences(words_sent, bigram_sent, trigram_sent, sent_list, gram_probs)
	target_highlights, target_builder = get_highlight_sentences(sent_list, words_sent, sent_probs)

	words_sent, bigram_sent, trigram_sent, sent_list, gram_probs = preprocess(cluster_list)
	sent_probs = score_sentences(words_sent, bigram_sent, trigram_sent, sent_list, gram_probs)
	cluster_highlights, cluster_builder = get_highlight_sentences(sent_list, words_sent, sent_probs)

	highlights, high_confidence = calculate_similarity(target_builder, cluster_builder, target_highlights)
	print(highlights)
	print(high_confidence)
	# write_json(highlights)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Let's find some fake news!")
	parser.add_argument("filename")
	args = parser.parse_args()
	main(args)