import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

import os
def pie_chart(data):
    labels = ['Negative Reviews', 'Positive Review'] 
    values = [len(data.loc[data['RATING'] <= 3]), len(data.loc[data['RATING'] > 3])] 
    #colors 
    colors = ['#ff9999','#99ff99'] 
    
    fig1, ax1 = plt.subplots(figsize=(7,7),facecolor='#395B64') 
    plt.rcParams['text.color'] = 'white'
    ax1.pie(values, colors = colors, labels=labels, autopct='%1.0f%%', startangle=170) 
    #draw circle 

    centre_circle = plt.Circle((0,0),0.70,fc='#395B64') 
    fig = plt.gcf() 
    fig.gca().add_artist(centre_circle) 

    # Equal aspect ratio ensures that pie is drawn as a circle 
    ax1.axis('equal')   
    plt.tight_layout()
   
    plt.figtext(.5,.95, "Positive Reviews vs Negative Reviews", fontsize = 10, ha = 'center',color='#FFFFFF')

    #save chart as png
    filename="Overall_Review_in_Pie_Chart.png"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    plt.savefig(dir_path+'/static/'+filename,bbox_inches = 'tight',
    pad_inches = 0)
    plt.clf()
    return os.path.join('static', filename)
