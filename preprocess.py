import pandas as pd
from collections import Counter
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.models import Word2Vec
from transformers import BertTokenizer, BertModel
import torch

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

df_1 = pd.read_csv('data.csv')
df_2 = pd.read_csv('data_1.csv')
df_3 = pd.read_csv('data_2.csv')

rename = {'Reviewer Name': 'reviewer_name',
          'Review Title':'review_title',
          'Place of Review':'place_of_review',
          'Up Votes':'up_votes',
          'Down Votes': 'down_votes',
          'Review text':'review_text',
          'Month':'month',
          'Ratings': 'ratings'
          }
df_1 = df_1.rename(columns= rename)

rename ={'Reviewer_Name':'reviewer_name',
         'Reviewer_Rating':'ratings',
         'Review_Title': "review_title",
         'Review_Text': 'review_text',
         'Place_of_Review':'place_of_review',
         'Date_of_Review':'date_of_review',
         'Up_Votes':'up_votes',
         'Down_Votes': 'down_votes'}
df_2 = df_2.rename(columns= rename)

rename ={'Date_of_review':'date_of_review',
         'Down_votes': 'down_votes',
         'reviewer_rating':'ratings'}

df_3 = df_3.rename(columns= rename)

columns_to_drop = ['month']
df_1.drop(columns=columns_to_drop, inplace=True)
columns_to_drop = ['date_of_review']
df_2.drop(columns=columns_to_drop, inplace=True)
df_3.drop(columns=columns_to_drop, inplace=True)

merge_df = pd.concat([df_1, df_2, df_3], ignore_index =  True)

merge_df.dropna()

df=merge_df

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    cleaned_text = ' '.join(tokens)
    return cleaned_text

df['cleaned_review_text'] = df['review_text'].apply(clean_text)

# Bag-of-Words (BoW)
bow_vectorizer = CountVectorizer()
bow_matrix = bow_vectorizer.fit_transform(df['cleaned_review_text'])

# TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['cleaned_review_text'])

tokenized_text = df['cleaned_review_text'].apply(word_tokenize)

w2v_model = Word2Vec(vector_size=100, window=5, min_count=1, workers=4)
w2v_model.build_vocab(tokenized_text)
w2v_model.train(tokenized_text, total_examples=w2v_model.corpus_count, epochs=10)


df['sentiment'] = df['ratings'].apply(lambda x: 'Positive' if x > 3 else 'Negative')

df.to_csv('cleaned_data.csv', index=False)