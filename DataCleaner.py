'''importing libraries'''
#if using visual studio must use pip3 install in terminal first eg, "pip3 install pandas", jupyter notebook doesnt need to
import pandas as pd
pd.options.mode.chained_assignment = None
import re
import nltk
#pip install --modulename-- if needed
import spacy
#python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')
from nltk.stem import WordNetLemmatizer
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
from Contractions import Contraction_dict
from nltk.corpus import stopwords
import unicodedata


def data_cleaning():
    '''functions'''
    #converts accented words
    def convert_accented(words):
        normaltext = unicodedata.normalize('NFKD',words).encode('ascii','ignore').decode('utf-8','ignore')
        return normaltext

    #expand contractions eg: I'll -> I will
    def expand_contractions(words, contraction_mapping=Contraction_dict):
        #identifies by pattern
        contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                        flags=re.IGNORECASE|re.DOTALL)
        #check if contraction matches data and expands it
        def expand_match(contraction):
            #matching word with existing data in dictionary
            match = contraction.group(0)
            first_char = match[0]
            #expands contration
            expanded = contraction_mapping.get(match)\
                                    if contraction_mapping.get(match)\
                                    else contraction_mapping.get(match.lower()) 
            
            expanded = first_char+expanded[1:]
            return expanded
            
        expanded_text = contractions_pattern.sub(expand_match, words)
        #add the expanded part to the back of the word and removes "'"from word
        expanded_text = re.sub("'", "", expanded_text)
        return expanded_text

    #removes emoji
    def remove_emoji(text):
        return text.encode('ascii', 'ignore').decode('ascii')

    '''main code'''

    #csv location
    data=pd.read_csv("Fullerton.csv",sep=',')

    #drop rows with NaN values
    data=data.dropna()

    #convert columns into str variables
    data['TITLE'] = data['TITLE'].astype(str) 
    data['REVIEW'] = data['REVIEW'].astype(str) 



    #remove special letters

    spec_chars = ["!",'"',"#","%","'","(",")",
                "*","+",",","-",".","/",":",";","<",
                "=",">","?","@","[","\\","]","^","_",
                "`","{","|","}","~","–"]
    for char in spec_chars:
        for columns in data:
            for rows in data.index:
            
            
                try:
                    #using extra try except specifically for Typeerrors when expanding contractions, if other there are any other errors do not skip.
                    try:
                        #expand contractions 
                        data.loc[rows,columns]= expand_contractions(data.loc[rows,columns])
                        #if strings are encoded then decode with utf8 to make the unicodes readable
                    except TypeError:
                        data.loc[rows,columns]= expand_contractions(data.loc[rows,columns].decode('utf8'))

                    #replace all punctuations and special characters with ' '
                    data.loc[rows,columns] = data.loc[rows,columns].replace(char, ' ')

                    #replace all & with "and"

                    data.loc[rows,columns] = data.loc[rows,columns].replace('&', 'and')

                    #convert accented words 
                    data.loc[rows,columns]=convert_accented(data.loc[rows,columns])

                    #remove emoji
                    data[columns] = data[columns].apply(lambda text: remove_emoji(text))

                    #remove any unicode chars, other types of punctuation not listed,url
                    data.loc[rows,columns] = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", data.loc[rows,columns])

                    #change everything to lower case
                    data.loc[rows,columns] = data.loc[rows,columns].lower()
                    

                    #converts rating to single digit from eg, 50.0 to 5.0

                    if data.loc[rows,"RATING"] > 5:
                        data.loc[rows,"RATING"] = data.loc[rows,"RATING"]/10

                    
                except:
                    pass
    print('clean')
    #once finished converting ratings to single digit, convert to int then str (int removes .0 from number)
    data['RATING'] = data['RATING'].astype(int)
    data['RATING'] = data['RATING'].astype(str)

    #removing 'date of stay' from Date Column
    data['DATE'] = data['DATE'].str.replace('date of stay ', '')

    #converts Date from sept 2022 -> 2022-09
    data['DATE'] = pd.to_datetime(data['DATE'])
    data['DATE'] = data['DATE'].apply(lambda x: x.strftime('%Y-%m'))
    print('converted')
    #try except for specifically Attributeerror as anything other than str cannot be stripped, isdigit() will throw attributeerror for date column

    for columns in data:
        for rows in data.index:
                try:
                    #get rid of whitespaces
                    data.loc[rows,columns] = data.loc[rows,columns].strip()

                    #removing stopwords
                    stop_words = stopwords.words('english')
                    #check if strings are words

                    if data.loc[rows,columns].isdigit() == False:
                    #calls each column and stop remove words.
                        data[columns] = data[columns].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))
                     #calls each column and lemmatizes sentences   
                        data[columns] = data[columns].apply(lambda row: " ".join([w.lemma_ for w in nlp(row)]))
                except AttributeError:
                    pass


    #remove \n \t
    data = data.replace(r'\n',  ' ', regex=True)
    print('fully cleaned')
   
    data.to_csv('Fullerton_Cleaned.csv')

