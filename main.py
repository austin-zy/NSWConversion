######################################################
# Author by Austin Goh, Azim Rosmadi, Sufia Zulhimi, 
#           Loh Yoong Keat, Dyana, Teoh Wei Jin
# WAES2108 - Natural Language Processing
# NSW Processor
# Development environment: WingIDE, Ubuntu Linux
# Function: get .txt as input and convert nsw to sw
######################################################

import os
import sys
import fileinput
from Tkinter import Tk
from tkFileDialog import askopenfilename
import csv


def makestructure(filename):
    #####################################
    #     Recognize user and message    #
    #####################################
    # Read from source file
    with open(filename) as f:
        text = f.read()
    # Split text according to lines into arrays/tuples
    paragraph = text.split('\n')
    # Initialize structured as empty array
    structured = []
    # Loop through to clear noise (Like and comment part) and 
    # Pass result into structured[]
    for i in range(len(paragraph)):
        if paragraph[i].find("Like")< 0:
            structured.append(paragraph[i])
    # Initialize members and conversation as empty arry
    members=[]
    conversation = []
    # Loop through denoised etxt
    for s in structured:
        # To get group member who is contributing in chat
        # Get all strng which is smaller than 25 chars
        if len(s)<=25:
            # Clear whatever empty line
            if not s == "\r":
                if s not in members:
                    # Clear nise with \r and \n adn append to members[]
                    s = s.strip('\r')
                    s = s.strip('\n')
                    members.append(s)
    # Get members from the text and write into text file  
        elif len(s)>25:
            conversation.append(s)  
    # Write into list of text(.txt) to be processed in the future
    f = open('members.txt', "w")
    for m in members:
        f.writelines(m+"\n")    
    f.close()
    return conversation
    

def readmembers():
    # Get array from members.txt
    f = open('members.txt')
    line=f.readlines()
    lines = []
    for l in line:
        lines.append(l.strip('\n'))
    return lines
       
def split(sentence):
    # Split long strings with space to form arrays of words
    word = sentence.split(' ')
    return word

def openlib(file):
    # Get nsw>sw conversion library from local directory
    dict = []    
    with open(file, 'rb') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader:
            dict.append(row)
    return dict

def replaceword(sentence,dict):
    #############################
    # Perform nsw>sw conversion #
    #############################
    # Split long string to arrays of words
    word = split(sentence)
    i = 0  
    for w in word:
        for d in dict:
            if w==d[0]:
                #print w+" is replaced by "+d[1]
                word[i] = d[1]
        i = i+1
    # Join arrays of words to form string
    edited = ' '.join(word)   
    return edited

def wordreplacement(sentence):
    # initialize dictionary
    dict_abbr = openlib('abbr.csv')
    dict_acro = openlib('acronym.csv')
    dict_combined = openlib('combined.csv')
    dict_english = openlib('english.csv')
    dict_interjection = openlib('interjection.csv')
    dict_misspelled = openlib('misspelled.csv')
    dict_slang = openlib('slang.csv')    
    #####################################
    #    Word Replacement Processing    #
    #####################################
    ## Replace abbreviations
    edited = replaceword(sentence,dict_abbr)
    #print "finish editing abbreviation"
    ## Replace acronym
    edited = replaceword(edited,dict_acro)
    #print "finish editing acronym"
    ## Replace combined
    edited = replaceword(edited,dict_combined)
    #print "finish editing combination words"
    ## Replace English words
    edited = replaceword(edited,dict_english)
    #print "finish editing English words"
    ## Replace Interjection
    edited = replaceword(edited,dict_interjection)
    #print "finish editing Interjection"
    ## Replace Misspelled Word
    edited = replaceword(edited,dict_misspelled)
    #print "finish editing Misspelled words"
    ## Replace slang
    edited = replaceword(edited,dict_slang)
    #print "finish editing slang"
    return edited

def convertConversation(conversation):
    ###########################################
    # Conversion from arrays to .txt and .csv #
    ###########################################
    # initalize processedtext as empty array/tuple
    processedtext = []
    # Open txt for writing
    f = open('conversation.txt','wb')
    # Open csv for writing
    with open('chat.csv', 'w') as csvfile:
        # Initialize header & CSV process
        fieldnames = ['user', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Loop through conversation to get user and ther message
        for c in conversation:
            # Perform nsw>sw operation after splitting to words and lowercase
            # Join the array of words as long string and append to processedtext
            processedtext.append(" ".join(wordreplacement(c.lower()).split(' ')))
            for p in processedtext:
                user =''
                # If first few character match n user library pass, declare user and their message
                for m in members:
                    if p[:len(m)]== m.lower():
                        user = p[:len(m)]
                        message = p[len(m):]
                        break;
            # If user and message is not empty, write as usual as %user : %message format
            if not user == '' and not message=='':
                writer.writerow({'user': user.title(), 'message': message})    
                f.writelines(user.title()+ ": "+message+"\n\n")
            # else if user is empty, regard as the message from previous user
            elif user=='' and not message=='':
                writer.writerow({'user': user.title(), 'message': message})    
                f.writelines("\t\t"+message+"\n\n")   
            # else dont do anything
    f.close()
    # close filewiter here

####################################################
#                MAIN FUNCTION                     #
####################################################
# HEADER
print "NSW translator"
print "---------------"
print "File to perform processing"

# GUI to get filename for process
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
# read text file

#####################################
#           Preprocessing           #
#####################################
conversation = makestructure(filename)
members = readmembers()
#####################################
#         Text Processing           #
#####################################
convertConversation(conversation)
print "CSV file done writed"
print "Text file done writed"
print "Process completed"                
