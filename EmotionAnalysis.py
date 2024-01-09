from nrclex import NRCLex
import json
import pandas as pd
import plotly
import plotly.express as px
from plotly.graph_objs import *


def emotionalanalysis(data):
    # converting df to json format
    json = data.to_json()

    # instantiate NRCLex object in json format
    text_object = NRCLex(json)

    # utilise the library to extract raw emotion score from data
    emotion = text_object.raw_emotion_scores

    # converting emotion scores into a data frame
    emotion_df = pd.DataFrame.from_dict(emotion, orient='index')
    emotion_df = emotion_df.reset_index()
    emotion_df = emotion_df.rename(columns={'index': 'Emotion Classification', 0: 'Emotion Count'})
    emotion_df = emotion_df.sort_values(by=['Emotion Count'], ascending=False)
    # sorting and visualising the scores into a bar graph
    fig = px.bar(emotion_df, x='Emotion Classification', y='Emotion Count', color='Emotion Classification',
                 orientation='v', width=800, height=400)

    # direc="static/bubble.png"

    direc = "templates/emotions.html"
    plotly.io.orca.config.executable = r"C:\Users\glady\AppData\Local\Programs\orca\orca.exe"
    plotly.io.orca.config.save()

    fig.write_html(direc)
    # figure.write_image(direc,"png",engine="orca")
