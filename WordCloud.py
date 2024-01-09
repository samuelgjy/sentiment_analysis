import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
#word cloud function
def wordcloud(review_df, review_colname, color, title):
    text = review_df[review_colname].tolist()
    text_str = ' '.join(text)
    
    wordcloud = WordCloud(collocations = False,
                         background_color = color,
                         width = 1600,
                         height = 800,
                         margin = 2,
                         min_font_size = 20).generate(text_str)

    plt.figure(figsize= (10,5),facecolor='#395B64')
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis("off")
    plt.figtext(.5,.9, title, fontsize = 20, ha = 'center')
  
    
def ShowWordCloudPositive(data):
    wordcloud(data.loc[data['RATING'] > 3], 'REVIEW', 'white', 'Positive Reviews')
    # save figure
    filename='wordcloudpositive.png'
  
    dir_path = os.path.dirname(os.path.realpath(__file__))
    plt.savefig(dir_path+'/static/'+filename,bbox_inches = 'tight',
    pad_inches = 0)
    plt.clf()
    return os.path.join('static', filename)
def ShowWordCloudNegative(data):
    wordcloud(data.loc[data['RATING']  < 3], 'REVIEW', 'black', 'Negative Reviews')
    # save figure
    filename='wordcloudnegative.png'
  
    dir_path = os.path.dirname(os.path.realpath(__file__))
    plt.savefig(dir_path+'/static/'+filename,bbox_inches = 'tight',
    pad_inches = 0)
    plt.clf()
    return os.path.join('static', filename)
