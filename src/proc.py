from gensim.models import KeyedVectors
pathToBinVectors = '~/GoogleNews-vectors-negative300.bin'

print ("Loading the data file... Please wait...")
model1 = KeyedVectors.load_word2vec_format(pathToBinVectors, binary=True)
print ("Successfully loaded 3.6 G bin file!")
model1.save('/mnt/ram-disk/Google-vectors.bin')
