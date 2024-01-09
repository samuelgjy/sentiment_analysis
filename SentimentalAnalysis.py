import nltk
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

nltk.download("vader_lexicon")
nltk.download("stopwords")


# conduct sentiment analysis on reviews and append sentiment score column to data
def vader_sentimental_analysis(data):
    analyzer = SentimentIntensityAnalyzer()
    vader_scores = []

    # analyse review and get VADER compound score for each review
    for row, review in enumerate(data['REVIEW']):
        sentiment_scores = analyzer.polarity_scores(review)
        vader_scores.append(sentiment_scores['compound'])

    print("Analysis completed")

    # add VADER compound score to SENTIMENT column in data
    data = data.assign(SENTIMENT=vader_scores)

    return data


def filter_sentiments_in_reviews(data):
    # filter out and return positive reviews
    is_positive_sentiment = data['SENTIMENT'] > 0
    positive_reviews_data = data[is_positive_sentiment]

    # group the positive reviews by every month and count the number of positive reviews each month
    positive_reviews_data = positive_reviews_data.groupby('DATE', group_keys=False)['SENTIMENT'].count().reset_index()
    positive_reviews_data.columns = ['DATE', 'POSITIVE_COUNT']

    # filter out and return negative reviews
    is_negative_sentiment = data['SENTIMENT'] < 0
    negative_reviews_data = data[is_negative_sentiment]

    # group the negative reviews by every month and count the number of negative reviews each month
    negative_reviews_data = negative_reviews_data.groupby('DATE', group_keys=False)['SENTIMENT'].count().reset_index()
    negative_reviews_data.columns = ['DATE', 'NEGATIVE_COUNT']

    # filter out and return neutral reviews
    is_neutral_sentiment = data['SENTIMENT'] == 0
    neutral_reviews_data = data[is_neutral_sentiment]

    # group the neutral reviews by every month and count the number of neutral reviews each month
    neutral_reviews_data = neutral_reviews_data.groupby('DATE', group_keys=False)['SENTIMENT'].count().reset_index()
    neutral_reviews_data.columns = ['DATE', 'NEUTRAL_COUNT']

    return positive_reviews_data, negative_reviews_data, neutral_reviews_data


# combine neutral, positive and negative sentiment reviews data
def combine_sentiment_count_data(data1, data2, data3):
    # merge neutral, positive and negative review counts data into 1 dataframe
    data = data1.merge(data2, on='DATE', how='outer')
    data = data.merge(data3, on='DATE', how='outer')

    # remove NaN from data and change the data types to integer
    try:
        data['NEGATIVE_COUNT'] = data['NEGATIVE_COUNT'].fillna(0).astype(int)
        data['NEUTRAL_COUNT'] = data['NEUTRAL_COUNT'].fillna(0).astype(int)
        data['POSITIVE_COUNT'] = data['POSITIVE_COUNT'].fillna(0).astype(int)
    except:
        pass

    return data


# plot overall sentiment histogram
def plot_overall_sentiment_histogram(data):
    # create empty plot
    figure = plt.subplots(figsize=(10, 9), facecolor='#395B64')
    plt.rcParams['text.color'] = 'black'

    # label and configure graph
    plt.hist(data['SENTIMENT'])
    plt.title('SENTIMENT POLARITY SCORE HISTOGRAM')
    plt.ylabel('FREQUENCY')
    plt.xlabel('POLARITY SCORE')

    # save graph as png with path
    filename = 'overall_sentiment_histogram_graph.png'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    plt.savefig(dir_path + '/static/' + filename)
    plt.clf()

    return os.path.join('static', filename)


# plot average sentiment over time graph
def plot_average_sentiment_graph(data):
    # group the data by month and calculate the average sentiment polarity score per month
    data = data.groupby('DATE', group_keys=False)['SENTIMENT'].mean().reset_index()
    data.columns = ['DATE', 'SENTIMENT']

    # set date as index
    data = data.set_index("DATE")

    # plot graph for both positive and negative reviews count over time
    figure = plt.subplots(figsize=(14, 9), facecolor='#395B64')
    plt.rcParams['text.color'] = 'black'
    plt.plot(data["SENTIMENT"], marker='o')

    # label and configure graph
    plt.xlabel("TIME")
    plt.ylabel("AVERAGE SENTIMENT")
    plt.title("AVERAGE SENTIMENT OVER TIME LINE GRAPH")
    plt.xticks(rotation=90)
    
    # save graph as png with path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = 'avg_sentiment.png'
    plt.savefig(dir_path + '/static/' + filename)
    plt.clf()
    return os.path.join('static', filename)


# plot total review sentiment over time bar graph
def plot_total_sentiment_bar_graph(data):
    # filter reviews from data and get total number of positive, negative and neutral reviews grouped by month
    positive_reviews, negative_reviews, neutral_reviews = filter_sentiments_in_reviews(data)
    review_sentiment_data = combine_sentiment_count_data(positive_reviews, negative_reviews, neutral_reviews).sort_values('DATE').set_index('DATE')

    # change data type of index to period by month
    review_sentiment_data.index = (pd.to_datetime(review_sentiment_data.index)).to_period(freq='M')

    # get first and last month of the dataset
    min_date = review_sentiment_data.index.min()
    max_date = review_sentiment_data.index.max()

    # fill in missing months and assign 0 to positive, negative and neutral review counts for those months
    review_sentiment_data = review_sentiment_data.reindex(pd.period_range(min_date, max_date), fill_value=0)

    # prepare data for plotting
    dates = list(review_sentiment_data.index.astype(str))
    positive_reviews = np.array(review_sentiment_data['POSITIVE_COUNT'])
    negative_reviews = np.array(review_sentiment_data['NEGATIVE_COUNT'])
    neutral_reviews = np.array(review_sentiment_data['NEUTRAL_COUNT'])

    # create empty plot
    figure = plt.subplots(figsize=(16, 9), facecolor='#395B64')
    plt.rcParams['text.color'] = 'black'

    # plot positive, negative and neutral number of reviews per month
    pos_bar = plt.bar(dates, positive_reviews, 0.65)
    neg_bar = plt.bar(dates, negative_reviews, 0.65,
                     bottom=positive_reviews)
    neu_bar = plt.bar(dates, neutral_reviews, 0.65,
                     bottom=negative_reviews + positive_reviews)

    # display values on graph
    for i in range(0, len(dates)):
        if negative_reviews[i] != 0:
            plt.annotate(negative_reviews[i], (i, negative_reviews[i] / 2 + positive_reviews[i]), ha="center")
        if neutral_reviews[i] != 0:
            plt.annotate(neutral_reviews[i], (i, neutral_reviews[i] / 2 + positive_reviews[i] + negative_reviews[i]),
                         ha="center")
        if positive_reviews[i] != 0:
            plt.annotate(positive_reviews[i], (i, positive_reviews[i] / 2), ha="center")

    # label and configure graph
    plt.title('TOTAL SENTIMENT COUNT OVER TIME BAR GRAPH')
    plt.legend((pos_bar[0], neg_bar[0], neu_bar[0]), ('Positive Reviews', 'Negative Reviews', 'Neutral Reviews'),
               fontsize=10, facecolor='yellow')
    plt.xlabel('TIME')
    plt.xticks(rotation=90)
    plt.ylabel('NUMBER OF REVIEWS')
    plt.yticks(np.arange(0, (review_sentiment_data['POSITIVE_COUNT'].max() + review_sentiment_data['NEGATIVE_COUNT'].max() + review_sentiment_data[
        'NEUTRAL_COUNT'].max()), 10))
    
    # save graph as png with path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = 'sentimentbar.png'
    plt.savefig(dir_path + '/static/' + filename)
    plt.clf()
    return os.path.join('static', filename)