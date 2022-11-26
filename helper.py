import streamlit as st
from urlextract import URLExtract
from collections import Counter
from wordcloud import WordCloud
import pandas as pd
import emoji as em
import seaborn as sns
import WPChat_analysis
extractor = URLExtract()
op = WPChat_analysis.help()
def stat(select,df):
    if select != 'Overall':
        df = df[df['user'] == select]
    l= []
    for m in df['message']:
            l.extend(m.split()) 
    num_m = df.shape[0]
    num_w = len(l)
    c=0
    link=[]
    for i in l:
        # print(i[-8:])
        link.extend(extractor.find_urls(i))
        if i[-8:] == 'omitted':
            c+=1
    num_media = c
    lenght_link = len(link)
    return num_m,num_w,num_media,lenght_link

def busy(df):
    x=df['user'].value_counts().head()
    name = x.index
    value = x.values
    y=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {'index':'name','user':'percentage'})
    return name,value,y

def word_cloud(select,df):
    if select != 'Overall':
        df = df[df['user'] == select]
    
    wc = WordCloud(width=800,height=800,min_font_size=12,background_color='white')
    op = wc.generate(df['message'].str.cat(sep = " "))
    return op

def perticular(select,df):
    if select != 'Overall':
        df= df[df['user']==select]
    
    temp = df[df['user'] != 'group notification']
    if op == 'iPhone':
        temp = temp[temp['message'] != '\u200eimage omitted\n']
    else:
        temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != '\u200esticker omitted\n']
    temp = temp[temp['message'] != '\u200eaudio omitted\n']
    l= []
    f = open('word.txt','r')
    stop_word = f.read()
    for m in temp['message']:
        for w in m.lower().split():
            if w not in stop_word:
                l.append(w)
    j = [character for character in l if character != '\u200e']
    o = [character for character in j if character != 'omitted' and character != '\u200esticker']
    new = pd.DataFrame(Counter(o).most_common(20))
    return new

def emoji(select,df):

    emojis = []
    if select != 'Overall':
        df= df[df['user']==select]
    for m in df['message']:
         emojis.extend([c for c in m if c in em.EMOJI_DATA])
    r = pd.DataFrame(Counter(emojis).most_common(20))
    return r
def timeline(select,df):
    if select != 'Overall':
        df= df[df['user']==select]
    time_line = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time =[]
    for i in range(time_line.shape[0]):
        time.append(time_line['month'][i] + "-" + str(time_line['year'][i]))
    time_line['time'] = time
    return time_line

def daily(select,df):
    if select != 'Overall':
        df = df[df['user'] == select]
    date_ti = df.groupby(['date_new']).count()['message'].reset_index()
    return date_ti
def week_activity(select,df):
    if select != 'Overall':
        df = df[df['user'] == select]
    busy = df['day_name'].value_counts()
    return busy
def month_activity(select,df):
    if select != 'Overall':
        df = df[df['user'] == select]
    busy_m = df['month'].value_counts()
    return busy_m

def heat(select,df):
    if select != 'Overall':
        df = df[df['user'] == select]
    table = df.pivot_table(index ='day_name',columns='new_h',values= 'message',aggfunc ='count').fillna(0)
    return table
