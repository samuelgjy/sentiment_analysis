
from textblob import TextBlob
import plotly
import orca
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from base64 import b64encode
import os

def subjectivity(x): 
    return TextBlob(x).sentiment.subjectivity

def polarity(x): 
    return TextBlob(x).sentiment.polarity

def sentimentbubble(data):
    #Create two new columns
    data['SUBJECTIVITY'] = data['REVIEW'].apply(subjectivity)
    data['POLARITY'] = data['REVIEW'].apply(polarity)

    #Create a function to compute the negative, neutral and positive analysis
    def getAnalysis(score):
        if score <0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    data['ANALYSIS'] = data['POLARITY'].apply(getAnalysis)

    # plot the polarity and subjectivity
    figure = px.scatter(data,x='POLARITY',y='SUBJECTIVITY',color = 'ANALYSIS',size='SUBJECTIVITY',width = 800, height = 400)

    #add a vertical line at x=0 for Netural Reviews
    figure.update_layout(title='Sentiment Analysis',
                    shapes=[dict(type= 'line',
                                yref= 'paper', y0= 0, y1= 1, 
                                xref= 'x', x0= 0, x1= 0)])
    
    # direc="static/bubble.png"
    direc="templates/bubble.html"
    #must download orca.exe from https://github.com/plotly/orca/releases
    plotly.io.orca.config.executable= r"C:\Users\glady\AppData\Local\Programs\orca\orca.exe"
    plotly.io.orca.config.save()
 
    figure.write_html(direc)
    # figure.write_image(direc,"png",engine="orca") if want to save as static image use this else writehtml as interactive
    
   
    



    # figure.write_image(direc,"png",engine='orca')
    # return '/static/bubble.png'
   