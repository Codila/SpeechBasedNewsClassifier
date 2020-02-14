#!/usr/bin/env python
# coding: utf-8
import pickle
import tkinter as tk
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from difflib import SequenceMatcher
from re import search
from tkinter import WORD
 


from nltk.corpus import stopwords
s=set(stopwords.words('english'))

filename = 'model/News_Classifier.pkl'

model = pickle.load(open(filename, 'rb'))
     
#Importing the speech recognition module
import speech_recognition as sr

news_url="https://news.google.com/news/rss"
Client=urlopen(news_url)  
xml_page=Client.read()
Client.close()

soup_page=soup(xml_page,"xml")
news_list=soup_page.findAll("item")
limit=3


def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
 
def news_classifier():
    #Initializing the speech recognizer
    r = sr.Recognizer()
    

    with sr.Microphone() as source:
        print("\nListening :\n")
        r.adjust_for_ambient_noise(source)
	
	#Declaring the listener source
        audio = r.listen(source)
        text = r.recognize_google(audio)
        text_list = text.split()
        text_list = [x.lower() for x in text_list]
        text_list = list(filter(lambda w: not w in s,text_list))
                
        print("\nYou said : {}".format(text))
	
	#Collecting Speech and Classifying
        prediction, _ = model.predict([text.strip()])
        
        news_combined = ''
        for index, news in enumerate(news_list):
            
            break_upNewsText = news.title.text.split()
            break_upNewsText = [x.lower() for x in break_upNewsText]
            
         
            if (intersection(text_list, break_upNewsText) != []):
               news_combined += news.title.text + '\n'
               print(news_combined)     
    try:
        #new =""
        if int(prediction) == 0:
           new = "You spoke about POLITICS"
	   #print('\nYou spoke about POLITICS')
        elif int(prediction) == 1:
           new = "You spoke about TECHNOLOGY"
           #print('\nYou spoke about TECHNOLOGY')
        elif int(prediction) == 2:
           new = "You spoke about Entertainment"
           #print('\nYou spoke about Entertainment')
        elif int(prediction) == 3:
           new = "You spoke about Business"
           #print('\nYou spoke about Business')
        else:
           new = "Not enough trained"
           #print('\nYou spoke about nothing')
    except:
        print("\nSorry could not recognize what you said")

    display= tk.Text(master=window, height = 10, width=25,font =("Times New Roman", 15), wrap=WORD)
    display.grid(column=0,row=2)
    display.insert(tk.END, "\nYou said : {}".format(text))

    entry_field1 = tk.Text(master=window, height = 3, width=25, font =("Courier New", 10, "bold"), wrap=WORD)
    entry_field1.grid(column= 0, row =3)
    entry_field1.insert(tk.END, "\nPrediction Result : {}".format(new))
    
    entry_field2 = tk.Text(master=window, height = 10, width=25, font =("Helvetica", 10, "bold"), wrap=WORD)
    entry_field2.grid(column= 0, row =4)
    entry_field2.insert(tk.END, "\nRecent News :{}".format('\n'+ news_combined))
    
window = tk.Tk()
t = tk.Text()
t.config(wrap=WORD)

window.title("News Predictor In Python")
window.geometry("250x500")

# label

title = tk.Label(text = "News Predictor App", font =("Times New Roman",15))
title.grid(column = 0, row = 0)

# Entry field
#entry_field1 = tk.Entry()
#entry_field1.grid(column= 0, row =2)

#Button
button1 = tk.Button(text= "Record", command =  news_classifier, font =("Times New Roman",15))
button1.grid(column = 0, row =1 )

window.mainloop()


