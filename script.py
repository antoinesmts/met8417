#Nom des restaurants - Sentiment analysis des commentaires laissés sur Google Maps
#Version 3 - 12/04/2020
#Import data from XLS file -> Sentiment analysis in Panda frames -> Export to MYSQL Database
#Basée sur la bibliothèque VADER

#Import the libraries
# > Pandas
import pandas as pd

# > Google file upload
from google.colab import files
import io

# ­> Excel
!pip install xlrd

# > Natural Language Toolkit - VADER & Stopwords
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
import numpy as np

# > mySQL Database
!pip install PyMySQL
import pymysql
from sqlalchemy import create_engine

#Import the Excel file
uploaded = files.upload()

reviews = pd.read_excel(io.BytesIO(uploaded['Reviews.xlsx']))

#Seeing number of col and rows
reviews.shape

#Putting the data in a DataFrame called df
df = pd.DataFrame(reviews)

#Cleaning the duplicates
df = df.drop_duplicates()

#Deleting rows with empty review
df = df.replace("", np.nan)
df = df.replace(" ", np.nan)
df = df.dropna()

#Delete "(Translated by Google) string and 
df["Review"] = df["Review"].str.replace("\(Translated by Google\)", "")
df["Review"] = df["Review"].str.split("\(Original\)").str[0]

df

#Sentiment analysis by VADER Library
analyzer = SentimentIntensityAnalyzer()
sentiment = df['Review'].apply(lambda x: analyzer.polarity_scores(x))
df = pd.concat([df,sentiment.apply(pd.Series)],1)

df

#Positive - Neutral - Negative sentiment
#Compound < -0.2 = Negative 
#Compound > 0.2 = Positive
#Else = Neutral

df["Sentiment"] = "Neutre"

df.loc[df["compound"] > 0.2, "Sentiment"] = "Positif"
df.loc[df["compound"] < -0.2, "Sentiment"] = "Négatif"
df.head()

#Register the results in MySQL Database
engine = create_engine("db_mysql"
                       .format(user="username",
                               pw="password",
                               db="db_name"))
df.to_sql('sentiment_analysis', con = engine, if_exists = 'replace')

#Cleaning of the data for words cloud

#Cleaning the data
df["Review"] = df["Review"].astype(str)

#Tokenize and remove punctuations 
stop_words = stopwords.words('english')
tokenizer = RegexpTokenizer(r'\w+')

def process_text(review):
    tokens = []
    for line in review:
        toks = tokenizer.tokenize(line)
        toks = [t.lower() for t in toks if t.lower() not in stop_words]
        tokens.extend(toks)
    
    return tokens

#Frequency distribution positive
df_pos = pd.DataFrame(data=df[df["Sentiment"]=="Positif"])
pos_lines = list(df_pos.Review)
pos_tokens = process_text(pos_lines)
pos_freq = nltk.FreqDist(pos_tokens)
df_freq_pos = pd.DataFrame(pos_freq.items(), columns = ["Mots","Fréquence"])
df_freq_pos["Sentiment"] = "Positif"

df_freq_pos

#Frequency distribution neutre
df_neu = pd.DataFrame(data=df[df["Sentiment"]=="Neutre"])
neu_lines = list(df_neu.Review)
neu_tokens = process_text(neu_lines)
neu_freq = nltk.FreqDist(neu_tokens)
df_freq_neu = pd.DataFrame(neu_freq.items(), columns = ["Mots","Fréquence"])
df_freq_neu["Sentiment"] = "Neutre"

#Frequency distribution négatif
df_neg = pd.DataFrame(data=df[df["Sentiment"]=="Négatif"])
neg_lines = list(df_neg.Review)
neg_tokens = process_text(neg_lines)
neg_freq = nltk.FreqDist(neg_tokens)
df_freq_neg = pd.DataFrame(neg_freq.items(), columns = ["Mots","Fréquence"])
df_freq_neg["Sentiment"] = "Négatif"

#Join in one data frame
df_distribution = pd.concat([df_freq_pos, df_freq_neu, df_freq_neg])
df_distribution

#Register the results in MySQL Database
engine = create_engine("db_mysql"
                       .format(user="username",
                               pw="password",
                               db="db_name"))
df_distribution.to_sql('word_distribution', con = engine, if_exists = 'replace')