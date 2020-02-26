import os
import re
import numpy as np
import pandas as pd
from flair.data import Sentence
from flair.models import SequenceTagger
from segtok.segmenter import split_single
from keras.models import load_model
from lazy_load import lazy_class
from pysoul.resnet_tune import resnet_detection


@lazy_class
class DetectPHI():
    def __init__(self):
        #loading the models.. very heavy :(
        self.tagger = SequenceTagger.load('ner-ontonotes-fast')
        self.resnet = load_model('model.h5')

    
    def detect_phi(self):
        dirs = [name for name in os.listdir('content') if os.path.isdir(os.path.join('content', name))]
        for directory in dirs:
            flair = []
            match = []
            path = 'content/'+directory
            for file in os.listdir(path):
                if file.endswith('.txt'):
                    f = open(path+'/'+file, "r")
                    text = f.read()
                    sentences = [Sentence(sent, use_tokenizer=True) for sent in split_single(text)]
                    self.tagger.predict(sentences)
                    match.append(re.findall(r'\S+@\S+\.\S+',text))
                    match.append(re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',text))
                    match.append(re.findall(r'^[0-9]{9,18}$',text)) 
                    match.append(re.findall(r'^\d{4}\s\d{4}\s\d{4}$',text))

                    for sentence in sentences:
                        identified = sentence.to_dict(tag_type='ner')
                        if len(identified['entities']):
                            for entity in identified['entities']:
                                flair.append([entity['text'],entity['type'],entity['confidence']])
            flair = pd.DataFrame(flair)
            flair.columns = ['text','type', 'confidence']
            match = pd.DataFrame(np.hstack((match)))
            match['type'] = 'REGEX'
            match['confidence'] = 1.0
            match.columns =['text','type', 'confidence']
            flair = pd.concat([flair,match])
            flair.to_csv(path+'/'+'flair.csv',index=None)
        #start applying resnet model
        resnet_detection(self.resnet)     

detect = DetectPHI()