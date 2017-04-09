
# coding: utf-8

# In[57]:

from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models.doc2vec import TaggedLineDocument
from gensim.models import doc2vec
from gensim.models import Doc2Vec
from gensim import models


# In[58]:

fh = open("user.txt",'r')
counter=1
sentences = []
for line in fh:
    line=line.strip()
    sentences.append(doc2vec.LabeledSentence(words=line.split(' '),tags=[str(counter)]))
    counter+=1


for i in sentences:
    print i


# In[59]:

class LabeledLineSentence(object):
    def __init__(self, filename):
        self.filename = filename
    def __iter__(self):
        for uid, line in enumerate(open(filename)):
            yield LabeledSentence(words=line.split(), labels=['SENT_%s' % uid])


# In[60]:

model = models.Doc2Vec(alpha=.025, min_alpha=.025, min_count=1)
model.build_vocab(sentences)


# In[61]:

for epoch in range(10):
    model.train(sentences)
    model.alpha -= 0.002  # decrease the learning rate`
    model.min_alpha = model.alpha  # fix the learning rate, no decay


# In[62]:

model.save("my_model.doc2vec")
model_loaded = models.Doc2Vec.load('my_model.doc2vec')


# In[63]:

print model.docvecs.most_similar(["2"])
print model['what is the address phone number and type of food']
print model_loaded.docvecs.most_similar(["2"])


# In[ ]:



