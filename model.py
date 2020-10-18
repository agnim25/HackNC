import json
import numpy as np
from tensorflow.python.keras import models
import re
import pickle
def load_model():

    # Model reconstruction from JSON file
    with open('model_architecture.json', 'r') as f:
        model = models.model_from_json(f.read())

    # Load weights into the new model
    model.load_weights('model_weights.h5')

    return model
def generate_recommendations(text):
    model = load_model()
    with open('objs.pkl', 'rb') as f: 
        contractions, vocab_to_int, int_news, min_price, max_price = pickle.load(f)

    clean_news = clean_text(text, contractions)
    int_news = news_to_int(clean_news, vocab_to_int)
    pad_news = padding_news(int_news, vocab_to_int)
    pad_news = np.array(pad_news).reshape((1,-1))
    pred = model.predict([pad_news,pad_news])
    price_change = unnormalize(pred, min_price, max_price)
    return price_change

def clean_text(text, contractions, remove_stopwords = True):
    text = text.lower()
    
    if True:
        text = text.split()
        new_text = []
        for word in text:
            if word in contractions:
                new_text.append(contractions[word])
            else:
                new_text.append(word)
        text = " ".join(new_text)
    
    text = re.sub(r'&amp;', '', text) 
    text = re.sub(r'0,0', '00', text) 
    text = re.sub(r'[_"\-;%()|.,+&=*%.,!?:#@\[\]]', ' ', text)
    text = re.sub(r'\'', ' ', text)
    text = re.sub(r'\$', ' $ ', text)
    text = re.sub(r'u s ', ' united states ', text)
    text = re.sub(r'u n ', ' united nations ', text)
    text = re.sub(r'u k ', ' united kingdom ', text)
    text = re.sub(r'j k ', ' jk ', text)
    text = re.sub(r' s ', ' ', text)
    text = re.sub(r' yr ', ' year ', text)
    text = re.sub(r' l g b t ', ' lgbt ', text)
    text = re.sub(r'0km ', '0 km ', text)

    return text
def news_to_int(news, vocab_to_int):
    '''Convert your created news into integers'''
    ints = []
    for word in news.split():
        if word in vocab_to_int:
            ints.append(vocab_to_int[word])
        else:
            ints.append(vocab_to_int['<UNK>'])
    return ints

def padding_news(news, vocab_to_int):
    '''Adjusts the length of your created news to fit the model's input values.'''
    padded_news = news
    max_daily_length = 200
    if len(padded_news) < max_daily_length:
        for i in range(max_daily_length-len(padded_news)):
            padded_news.append(vocab_to_int["<PAD>"])
    elif len(padded_news) > max_daily_length:
        padded_news = padded_news[:max_daily_length]
    return padded_news
def unnormalize(price, min_price, max_price):
    '''Revert values to their unnormalized amounts'''
    price = price*(max_price-min_price)+min_price
    return(price)