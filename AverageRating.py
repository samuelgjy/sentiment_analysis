import pandas as pd


# calculate the average rating of the reviews
def get_average_rating(data):
    return round((data['RATING'].mean() * 2)) / 2