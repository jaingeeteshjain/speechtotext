# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 00:50:19 2016

@author: prathmesh.savale
"""
#!/usr/bin/env python3

import speech_recognition as sr

#AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "english.wav")
#AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "test2.wav")
AUDIO_FILE = '/home/cloudera/git/speechtotext/pyscripts/sample3.wav'
# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source) # read the entire audio file

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    