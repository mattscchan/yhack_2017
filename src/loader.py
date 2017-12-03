from gensim.models import KeyedVectors
from threading import Semaphore
model = KeyedVectors.load('/mnt/ram-disk/Google-vectors.bin',mmap='r')
model.syn0norm = model.syn0  # prevent recalc of normed vectors
model.most_similar('stuff')
Semaphore(0).acquire()
