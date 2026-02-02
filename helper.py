import matplotlib.pyplot as plt
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    #no. of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #no. of links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))



    return num_messages, len(words), num_media_messages,len(links)



def most_busy_users(df):
    x = df['user'].value_counts().head()

    df=round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'})

    return x,df



def create_wordcloud(selected_user,df):

    # removing stupid words like hai haan aacha
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    #removing useless words
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    # filtered group notification and media messages

    def remove_stopwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)



    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep=' '))
    return df_wc

def most_commonwords(selected_user,df):

    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    # filtered group notification and media messages

    # removing stupid words like hai haan aacha
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    #print(stop_words)

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df


def commonly_used_emojis(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    datafr=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return datafr


def montly_data(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append((str(timeline['month'][i]) + "-" + str(timeline['year'][i])))
    timeline['time'] = time
    return timeline


def daily_data(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]

    daily_timeline = df.groupby('day-date').count()['message'].reset_index()
    return daily_timeline


def week_activity(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]

    weekly_data = df['day_name'].value_counts()
    return weekly_data

def month_activity(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]

    month_activity_data = df['month'].value_counts()
    return month_activity_data


def hourly_activity(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]

    activity_map=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return activity_map


def sentiment_analysis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for message in temp['message']:
        score = sia.polarity_scores(message)['compound']
        if score > 0.05:
            sentiments["Positive"] += 1
        elif score < -0.05:
            sentiments["Negative"] += 1
        else:
            sentiments["Neutral"] += 1

    return sentiments
