import pandas as pd
import matplotlib.pyplot as plt
import gensim.corpora as corpora
from gensim.corpora import Dictionary
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn
import pickle
from pathlib import Path

#Create a function to build the optimal LDA model
def ideal_model(dataframe, column_name):
    '''
    INPUTS:
        dataframe - dataframe that contains the reviews
        column_name: name of column that contains reviews
        
    OUTPUTS:
        lda_tfidf - Latent Dirichlet Allocation (LDA) model
        dtm_tfidf - document-term matrix in the tfidf format
        tfidf_vectorizer - word frequency in the reviews
        A graph comparing LDA Model Performance Scores with different params
    '''
    text_raw = dataframe[column_name].tolist()
    for n in range(len(text_raw)):
        if type(text_raw[n])==float:
            text_raw[n]=str(text_raw[n])
        else:
            continue

    #***********   Step 1: Convert to document-term matrix   ************#

    #Transform text to vector form using the vectorizer object 
    text_vectorizer = CountVectorizer(strip_accents = 'unicode',
                                    stop_words = 'english',
                                    lowercase = True,
                                    token_pattern = r'\b[a-zA-Z]{3,}\b', # num chars > 3 to avoid some meaningless words
                                    max_df = 0.9,                        # discard words that appear in > 90% of the reviews
                                    min_df = 10)                         # discard words that appear in < 10 reviews    

    #apply transformation
    text_matrix_tfidf = TfidfVectorizer(**text_vectorizer.get_params())

    #convert to document-term matrix
    dtm_text_matrix = text_matrix_tfidf.fit_transform(text_raw)  

    print("The shape of the tfidf is {}, meaning that there are {} {} and {} tokens made through the filtering process.".\
              format(dtm_text_matrix.shape,dtm_text_matrix.shape[0], column_name, dtm_text_matrix.shape[1]))

    
    #*******   Step 2: GridSearch & parameter tuning to find the optimal LDA model   *******#

    # Define the range of values for each parameter in which to determine optimal parameters from
    test_params = {'n_components': [4, 8, 12, 16, 20, 24, 28],
                     'learning_decay': [.5, .7, .9]}

    # Initialize the Model
    lda = LatentDirichletAllocation()

    # Init Grid Search Class
    model = GridSearchCV(lda, param_grid=test_params)
    # Do the Grid Search
    model.fit(dtm_text_matrix)


    #*****  Step 3: Output the optimal lda model and its parameters  *****#

    # Best Model
    optimal_lda_model = model.best_estimator_

    # Model Parameters
    print("Optimal Model's Params: ", model.best_params_)

    # Log Likelihood Score: Higher the better
    print("Model Log Likelihood Score: ", model.best_score_)

    # Perplexity: Lower the better. Perplexity = exp(-1. * log-likelihood per word)
    print("Model Perplexity: ", optimal_lda_model.perplexity(dtm_text_matrix))


    #***********   Step 4: Compare LDA Model Performance Scores   ***********#

    #Get Log Likelyhoods from Grid Search Output
    gscore=model.fit(dtm_text_matrix).cv_results_
    n_topics = [4, 8, 12, 16, 20, 24, 28]

    log_likelihood_dec5 = [gscore['mean_test_score'][gscore['params'].index(v)] for v in gscore['params'] if v['learning_decay']==0.5]
    log_likelihood_dec7 = [gscore['mean_test_score'][gscore['params'].index(v)] for v in gscore['params'] if v['learning_decay']==0.7]
    log_likelihood_dec9 = [gscore['mean_test_score'][gscore['params'].index(v)] for v in gscore['params'] if v['learning_decay']==0.9]

    # Show graph
    plt.figure(figsize=(20, 12))
    plt.plot(n_topics, log_likelihood_dec5, label='0.5')
    plt.plot(n_topics, log_likelihood_dec7, label='0.7')
    plt.plot(n_topics, log_likelihood_dec9, label='0.9')
    plt.title("Choosing Optimal LDA Model")
    plt.xlabel("Num Topics")
    plt.ylabel("Log Likelihood Scores")
    plt.legend(title='Learning decay', loc='best')
    plt.show()
    
    return optimal_lda_model, dtm_text_matrix, text_matrix_tfidf


def lda(data):

    # Combine data of all customer reviews into a single column for easier data extraction
    rev = data[["TITLE","REVIEW"]]
    rev["feedback"]=rev["TITLE"]+" "+rev["REVIEW"]
    
    # Obtain Optimal Model & Proccessed Data
    optimal_lda_model, dtm_text_matrix, text_matrix_tfidf = ideal_model(rev, "feedback")
    
    # Visaulise Topics of Data and top 30 words of each topic
    optimal_model_vis = pyLDAvis.sklearn.prepare(optimal_lda_model, dtm_text_matrix, text_matrix_tfidf)
    
    # Save topics to html file to be loaded onto website
    pyLDAvis.save_html(optimal_model_vis, 'templates/pickle_lda_model_sklearn.html')
   