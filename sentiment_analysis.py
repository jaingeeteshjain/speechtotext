# -*- coding: utf-8 -*-
"""
Created on Tue Oct 4 00:58:13 2016

@author: prathmesh.savale
"""


import glob
#import ctypes
import speech_recognition as sr
import os, os.path, codecs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
import numpy as np
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import speech_recognition as sr
import nltk
from nltk.corpus import brown





filenames = glob.glob('/home/cloudera/Desktop/speechtotext/segmentedwavfiles/*.wav')

for i in range(0,len(filenames)):
    print(filenames[i])
    
    AUDIO_FILE = filenames[i]
    
    test = filenames[i].split('/', 6)[6]
    
    test2 = test.split('_',2)[2]
    test3 = test2.split('_',2)[1]
    speaker_name = test3.split('.',2)[0]
    #print(speaker_name)
    
    filename = filenames[i].split('/',6)[6]
    foldername = filename.split('_',2)[0]
    
    filename = foldername +speaker_name+ '.txt'
    #print(filename)
    
   
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source) # read the entire audio file




    #try:
       # with open(filename) as file:
            #f=open(filename,"a")
        # do whatever
            
            
    #except IOError:
    if not os.path.exists("transcribed_files/"+foldername):
        os.makedirs("transcribed_files/"+foldername)        
        
        
    if i == 0:
	
        if os.path.isfile("transcribed_files/"+foldername+"/"+filename):
            os.remove("transcribed_files/"+foldername+"/"+filename)
        
            
    f = open("transcribed_files/"+foldername+"/"+filename,"a")
    #f.write(speaker_name+" spoke:")
        #f.write(speaker_name + " said: ")
    try:
            
        f.write(r.recognize_google(audio))
        f.write("\n\n")
            #print(r.recognize_google(audio))
    except sr.UnknownValueError:
        f.write("Google Speech Recognition could not understand audio")
        f.write("\n\n")
    except sr.RequestError as e:
        f.write("Could not request results from Google Speech Recognition service; {0}".format(e))
        f.write("\n\n")
    f.close()
    
    


brown_train = brown.tagged_sents(categories='news')

regexp_tagger = nltk.RegexpTagger(

    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),

     (r'(-|:|;)$', ':'),

     (r'\'*$', 'MD'),

     (r'(The|the|A|a|An|an)$', 'AT'),

     (r'.*able$', 'JJ'),

     (r'^[A-Z].*$', 'NNP'),

     (r'.*ness$', 'NN'),

     (r'.*ly$', 'RB'),

     (r'.*s$', 'NNS'),

     (r'.*ing$', 'VBG'),

     (r'.*ed$', 'VBD'),

     (r'.*', 'NN')

])

unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)

bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)

#############################################################################





# This is our semi-CFG; Extend it according to your own needs

#############################################################################

cfg = {}

cfg["NNP+NNP"] = "NNP"

cfg["NN+NN"] = "NNI"

cfg["NNI+NN"] = "NNI"

cfg["JJ+JJ"] = "JJ"

cfg["JJ+NN"] = "NNI"

#############################################################################





class NPExtractor(object):



    def __init__(self, sentence):

        self.sentence = sentence



    # Split the sentence into singlw words/tokens

    def tokenize_sentence(self, sentence):

        tokens = nltk.word_tokenize(sentence)

        return tokens



    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")

    def normalize_tags(self, tagged):

        n_tagged = []

        for t in tagged:

            if t[1] == "NP-TL" or t[1] == "NP":

                n_tagged.append((t[0], "NNP"))

                continue

            if t[1].endswith("-TL"):

                n_tagged.append((t[0], t[1][:-3]))

                continue

            if t[1].endswith("S"):

                n_tagged.append((t[0], t[1][:-1]))

                continue

            n_tagged.append((t[0], t[1]))

        return n_tagged



    # Extract the main topics from the sentence

    def extract(self):



        tokens = self.tokenize_sentence(self.sentence)

        tags = self.normalize_tags(bigram_tagger.tag(tokens))



        merge = True

        while merge:

            merge = False

            for x in range(0, len(tags) - 1):

                t1 = tags[x]

                t2 = tags[x + 1]

                key = "%s+%s" % (t1[1], t2[1])

                value = cfg.get(key, '')

                if value:

                    merge = True

                    tags.pop(x)

                    tags.pop(x)

                    match = "%s %s" % (t1[0], t2[0])

                    pos = value

                    tags.insert(x, (match, pos))

                    break



        matches = []

        for t in tags:

            if t[1] == "NNP" or t[1] == "NNI":

            #if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":

                matches.append(t[0])

        return matches





# Main method, just run "python np_extractor.py"

    
filenames = glob.glob('/home/cloudera/Desktop/speechtotext/transcribed_files/'+foldername+'/*.txt')


#print(filenames)

for i in range(0,len(filenames)):
    
    test = filenames[i].split('/', 7)[7]
    
    foldername = filenames[i].split('/', 7)[6]
#    print(test)    
#    print("\n")
    file_speaker_name = test.split('.',2)[0]
#    print(file_speaker_name)
    
    
    filename = file_speaker_name+ '.txt'
#    print(filename)
    
    
    with open('/home/cloudera/Desktop/speechtotext/transcribed_files/'+foldername+'/'+filename, 'r') as myfile:
        #data=myfile.read().replace('\n', '')
        data=myfile.read()
    	
    
    	
    sentence = data
    
    
    x = sentence
    
    blob = TextBlob(x)
    
    
    
    blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
    
                        #  ('threat', 'NN'), ('of', 'IN'), ...]
    
    
    
    blob.noun_phrases   # WordList(['titular threat', 'blob',
    
                        #            'ultimate movie monster',
    
                        #            'amoeba-like mass', ...])
    
    
    
    for sentence in blob.sentences:
#        print(sentence)
        #print(sentence.sentiment.polarity)
        
        #print(sentence.sentiment)
        
        
    
        if sentence.sentiment.polarity == 0.0:
    
#            print("Neutral")
    
            a = "Neutral"
    
        if sentence.sentiment.polarity < 0.0:
    
#            print("Negative")
    
            a = "Negative"
    
        if sentence.sentiment.polarity > 0.0:
    
#            print("Positive")
    
            a = "Positive"
    
       
    
    	
    
      
    
        np_extractor = NPExtractor(str(sentence))
    
        result = np_extractor.extract()
    
        
        
#        print ("This sentence is about: %s" % ", ".join(result))
        
        if not os.path.exists("sentiment/"+foldername):
            os.makedirs("sentiment/"+foldername) 
        
        
        if os.path.isfile("sentiment/"+foldername+'/'+test):
            os.remove("sentiment/"+foldername+'/'+test)
            
        
        with open("sentiment/"+foldername+'/'+test, 'a') as f:                   #write to csv
            f.write("The general sentiment of the transcript is: "+a)
            f.write("\n\n")
 
            f.write("This sentence is about: %s" % ", ".join(result))
            
            
            
        
    #
    #    
        
    #    
    #    with open('sentiment.csv', 'a') as f:                   #write to csv
    #    
    #        f.write(a)
    
    
    
    #    with open('inputfile.txt', 'r') as myfile:
    #        #data=myfile.read().replace('\n', '')
    #        data=myfile.read()
    #
    #	
    #d
    #    sentence = data
    #
    #    np_extractor = NPExtractor(sentence)
    #
    #    result = np_extractor.extract()
    #
    #    
    #    
    #    print ("This sentence is about: %s" % ", ".join(result))
    #
    #l
    #
    #    with open('keyword.csv', 'a') as f:                   #write to csv
    #
    #        f.write("This sentence is about: %s" % ", ".join(result))
    
    
    
    
