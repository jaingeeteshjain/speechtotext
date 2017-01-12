#!/usr/bin/env python2
'''
# ================================================================================#
#-- PROJECT NAME : MR Robot
#-- TASK : Accept a wav file as input and use Google Speech API to 
			transcribe the entire audio to text

#-- Author : Neeratyoy Mallik
#-- Date : August 17th, 2016
#-- Modified : August 26th 2016
# ================================================================================#
'''


import speech_recognition as sr 
from scipy.io import wavfile as wave
import math
import uuid
from subprocess import call
import sys
import time
import re

# Defines a dictionary of words that need to be replaced with values being the occurences to be replaced and the key being the replacement
dict_of_words = {'mustream':['new stream','new scream'],
                'raspberrypi':['raspberry pie'],
                'muflow':['new flow'],
                'muesp':['e s p', 'esp','new esp','new e s p',],
                'musigma':['new sigma','new stigma','mu sigma']}

def incorporate_heuristics(dict_of_words, transcribed_lines):
    
    '''Function to incorporate heuristics into the speech to text algorithm. Converting "new stream" to  "muStream" and so on. 
    A pessimist might call it hard-coding; an optimist might call it incorporating contextual information. Im on the fence.
    
    Takes as input 
        1) a lower case dictionary of words with key as a MuSigma context word (eg. muStream) and 
        associated value is a list of possible ways speech recognition might mastakenly output it as (eg "new stream")
        2) transcribed lines
    '''
    
    for keyword, poss_values in dict_of_words.items():
         
         # Separate the entries with a '|' so that regex can search together 
         reg_ex_to_search = '|'.join(poss_values)
         
         # Create a reg ex object to help with the search
         reg_ex_object = re.compile('('+reg_ex_to_search+')',re.IGNORECASE)
         
         # Substitute any occurence of any element of poss_values with keyword
         transcribed_lines = reg_ex_object.sub(keyword, transcribed_lines)

    return transcribed_lines


def extract(fileName, output = None, rate=16000):
	'''
	Input: fileName takes in the wav file name as input (if in the same directory) or its absolute path
		   output contains the name of the text file to which the transcription will be written
	       rate by default is 16000 but needs to passed during a call if 44100
	Output: A long string separated by new lines containing the transcriptions for the input wav file
	'''
	r = sr.Recognizer()
	d = wave.read(fileName)
	rate = d[0]
	length = len(d[1])
	# uid = str(uuid.uuid4())
	jumps = rate * 10        #determines the 10 second jump size			
	j = 0
	k = math.ceil(length*1.0/jumps)
	i = jumps
	transcriptions = []
	while j<k:
		uid = str(uuid.uuid4())
		sample = d[1][i-jumps:min(i,length)]
		wave.write('sample'+uid+'.wav',rate,sample)
		call('flac sample'+uid+'.wav', shell=True)
		call('rm sample'+uid+'.wav', shell=True)
		i += jumps
		j += 1
		with sr.AudioFile('sample'+uid+'.flac') as source:
			r.adjust_for_ambient_noise(source)
			audio = r.record(source)
			try:
				text = r.recognize_google(audio)
				transcriptions.append(text)
				print text
                        # In case the audio is unintelligeble, it will throw an error. Catch it and append " " to the transcription
			except sr.UnknownValueError as e:
				print '\nException : '+str(e)+'\n'
				transcriptions.append(" ")
                        except sr.RequestError as re:
                                print "Unable to connect to Google"
                                print "\nException:",str(re),"\n"
                                i -= jumps
                                j -= 1 #To read the same chunk again. 
                                time.sleep(5)
                                
		time.sleep(1)
		call('rm sample'+uid+'.flac', shell=True)

	transcriptions = '\n'.join(transcriptions)
        transcriptions = incorporate_heuristics(dict_of_words, transcriptions)

	if output is not None:
		f = open(output, 'w')
		f.writelines(transcriptions)
		f.close()

	return transcriptions
	

if __name__ == "__main__":
	extract(sys.argv[1])
