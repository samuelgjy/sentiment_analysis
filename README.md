# sentiment_analysis
To create an understandable depiction of a significant amount of hotel guest reviews, our project uses a number of machine learning techniques, such as topic modelling and sentiment analysis. To assess the efficacy and viability of our solution, we test it against customer reviews from Fullerton Hotel dataset.

WhereToStay, a web-based platform that implements review scraping from TripAdvisor.com,  summarises those evaluations, apply sentiment analysis, emotion recognition, and topic modelling to hotel reviews. It is a comprehensive online website that allows users to look for a hotel as well as read the general opinion and feelings of previous clients of the establishment. Because of this, there won't be any need to look through a bunch of different reviews before deciding anything. Businesses will be able to profit from the results of the attitudes survey by gaining insight into what their customers want and using this information to gain a competitive advantage over their rivals.

System Diagram:
![image](https://github.com/samuelgjy/sentiment_analysis/assets/110824653/bb4fa8b6-168a-41e6-a588-a2fe40d04925)


For Text Sentiment Analysis, our team ran the pre-processed dataset through an instance of the Valence Aware Dictionary for Sentiment Reasoning (VADER) Sentiment Intensity Analyzer provided in the Natural Language Toolkit library. VADER is a lexical method of sentimental analysis whose lexicon is built on the combined ratings of a number of human raters. The Sentiment Intensity Analyzer will calculate the emotional polarity of each review and return a rating, ranging from -1 for negative to 1 for positive which will be appended to the dataset.
![image](https://github.com/samuelgjy/sentiment_analysis/assets/110824653/44f932db-4d8a-4407-ba03-20a77062ebd5)


VADER average sentiment over time.
![image](https://github.com/samuelgjy/sentiment_analysis/assets/110824653/aeafb481-a9f9-4ef6-98db-74e97474e15c)


Conducted sentiment analysis using Textblob library, visualising the subjectivity to polarity ratio, and showing the overall emotional polarity to complement and validate the credibility of VADER and its accuracy.
![image](https://github.com/samuelgjy/sentiment_analysis/assets/110824653/9b20e65c-02b4-44d6-8ec0-5dfd3e62eda3)


Conducted Latent Dirichlet Analysis
![image](https://github.com/samuelgjy/sentiment_analysis/assets/110824653/fec833ba-2375-4bde-94c7-b2e527ab4a75)
