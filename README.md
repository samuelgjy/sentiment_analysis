**Sentiment Analysis for Hotel Guest Reviews**

Our project aims to provide a comprehensive understanding of hotel guest reviews through various machine learning techniques, including topic modeling and sentiment analysis. We evaluate the efficacy of our solution using customer reviews from the Fullerton Hotel dataset.


WhereToStay is a web-based platform that scrapes reviews from TripAdvisor.com, summarizes evaluations, and applies sentiment analysis, emotion recognition, and topic modeling to hotel reviews. This online platform allows users to easily find hotels and read the opinions of previous clients, streamlining the decision-making process. Businesses can leverage this data to gain insights and a competitive advantage.

System Diagram
![image](https://github.com/samuelgjy/sentiment_analysis/assets/110824653/bb4fa8b6-168a-41e6-a588-a2fe40d04925)

Text Sentiment Analysis with VADER:

We utilized the Valence Aware Dictionary for Sentiment Reasoning (VADER) Sentiment Intensity Analyzer from the Natural Language Toolkit library for text sentiment analysis. VADER assigns a sentiment score to each review, ranging from -1 (negative) to 1 (positive).

![image](https://github.com/samuelgjy/sentiment_analysis/assets/110824653/44f932db-4d8a-4407-ba03-20a77062ebd5)

VADER Average Sentiment Over Time:

![image](https://github.com/samuelgjy/sentiment_analysis/assets/110824653/aeafb481-a9f9-4ef6-98db-74e97474e15c)

Sentiment Analysis with Textblob:

We conducted sentiment analysis using the Textblob library, visualizing the subjectivity to polarity ratio and overall emotional polarity. This complements and validates the credibility of VADER and its accuracy.

![image](https://github.com/samuelgjy/sentiment_analysis/assets/110824653/9b20e65c-02b4-44d6-8ec0-5dfd3e62eda3)

Latent Dirichlet Analysis (LDA):

We applied Latent Dirichlet Analysis to uncover topics within the dataset.

![image](https://github.com/samuelgjy/sentiment_analysis/assets/110824653/fec833ba-2375-4bde-94c7-b2e527ab4a75)
