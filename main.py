'''importing libraries'''
#if using visual studio must use pip3 install in terminal first eg, "pip3 install pandas", jupyter notebook doesnt need to
import pandas as pd

from SentimentBubble import sentimentbubble
from EmotionAnalysis import emotionalanalysis
pd.options.mode.chained_assignment = None
import numpy as np 
import re
import nltk
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googlesearch import search
nltk.download("vader_lexicon")
import os
import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('omw-1.4')
from Contractions import Contraction_dict
from nltk.corpus import stopwords
import unicodedata
import response
import DataCleaner
import HotelSearch
import Scraper
import SentimentalAnalysis
import AverageRating
import SentimentBubble
import EmotionAnalysis
import LDA
import WordCloud
import RatingDonutChart
#first create virtual environment using py -3 -m venv .venv using windows cmd in the desired folder, afterwards .venv\scripts\activate to activate the venv
from flask import Flask, render_template , request,redirect,url_for

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    rating=0

    return render_template('index.html',rating=rating)
    
@app.route('/search', methods=['GET','POST'])
def search():
    #take in user input form requested form (during demo unblock but for css purposes the entire data collection is commented out)
    searchinput = request.form['searchinput']
    #validate if user entered a hotel from singapore else ask user to input again
    if HotelSearch.find_hotel_review_page(searchinput)==None:
         searchinput='Please try entering a hotel from Singapore'
         #return back to index.html and return 'Please try entering a hotel from Singapore
         return render_template('index.html',searchinput = searchinput, posandneg = None, sentinmentovertime = None, rating=0)
    else:
    #assign hotel as url using using user input
        hotel = HotelSearch.find_hotel_review_page(searchinput)

    #call scraper function
    Scraper.scraper(hotel)
    # call data cleaning function
    DataCleaner.data_cleaning()
    
    #data analysis
    data = pd.read_csv("Fullerton_Cleaned.csv", sep=',')
    
    data = SentimentalAnalysis.vader_sentimental_analysis(data)
    totalsentimentbar = SentimentalAnalysis.plot_total_sentiment_bar_graph(data)
    
    #posandneg variable to be used as img src path for positive and negative review graph
    #get average rating from reviews
    rating = AverageRating.get_average_rating(data)
    #setimentovertime variable used as img src path for sentimentovertime graph png
    sentimentovertime = SentimentalAnalysis.plot_average_sentiment_graph(data)
    Histogram = SentimentalAnalysis.plot_overall_sentiment_histogram(data)
    #return to index.html to await for user input again and return all variables needed.
    SentimentBubble.sentimentbubble(data)
    EmotionAnalysis.emotionalanalysis(data)
    LDA.lda(data)
    Pros  = WordCloud.ShowWordCloudPositive(data)
    Cons = WordCloud.ShowWordCloudNegative(data)
    piechart= RatingDonutChart.pie_chart(data)
    return render_template('index.html',piechart=piechart,searchinput = searchinput,  totalsentimentbar = totalsentimentbar, sentimentovertime=sentimentovertime, rating=rating, Histogram=Histogram, Pros=Pros, Cons=Cons)


@app.route('/lda', methods=['GET', 'POST'])
def lda():
    if request.method == 'POST':
        

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('link.html')
@app.errorhandler(404)
def page_not_found(e):
   # note that we set the 404 status explicitly
    return render_template('404.html'), 404
if __name__== '__main__':
    app.run(debug=True,host="127.0.0.1", port=80)


