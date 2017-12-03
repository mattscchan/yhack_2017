from gensim.models import KeyedVectors

pathToBinVectors = '/home/mattchan/yhacks_2017/GoogleNews-vectors-negative300.bin'

print ("Loading the data file... Please wait...")
model1 = KeyedVectors.load_word2vec_format(pathToBinVectors, binary=True)
print ("Successfully loaded 3.6 G bin file!")

with open('/mnt/ram-disk/word2vec', 'w') as f:
	f.write(model1)