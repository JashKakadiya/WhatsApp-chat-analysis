import re
import pandas as pd
import streamlit as st

def pre(data):
    option= st.sidebar.selectbox("What device you used",('iPhone','Android'))
    option2=st.sidebar.radio("Select your device time formate",('12 hour formate','24 hour formate'))
    if option == 'iPhone':
        if option2 == '12 hour formate':
            p = "\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s\w[A-Z]\]"
        else:
            p = "\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s\]"
        message = re.split(p, data)[1:]
        time = re.findall(p,data)
        df= pd.DataFrame({'user_message':message, 'time':time})
        if option2 == '24 hour formate':
            df['time'] = pd.to_datetime(df['time'],format="[%d/%m/%y, %H:%M:%S %p]")
        else:
            df['time'] = pd.to_datetime(df['time'],format="[%d/%m/%y, %I:%M:%S %p]") 
        df.rename(columns= {'time':'date'},inplace = True)
    else:
        if option2 == '12 hour formate':
            p = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w[a-zA-Z]\s-\s"
        else:
            p = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
        message = re.split(p, data)[1:]
        time = re.findall(p,data)
        df = pd.DataFrame({'user_message':message, 'date_o':time})
        if option2 == '24 hour formate':
            formate = []
            for i in df['date_o']:
                formate.append(i[:-3])
            df['date'] = formate
            df['date']=pd.to_datetime(df['date'],format="%d/%m/%y, %H:%M")
        else:
            formate = []
            for i in df['date_o']:
                formate.append(i[:-6])
            df['date'] = formate
            df['date'] =pd.to_datetime(df['date'],format="%d/%m/%y, %I:%M")
     

    user=[]
    m = []
    for me in df['user_message']:
        entry = re.split('([\w\W]+?):\s',me)
        if entry[1:]:
            user.append(entry[1])
            m.append(entry[2])
        else:
            m.append(entry[0])
            user.append("group notification")
    df['user']=user
    df['message']= m
    df.drop(columns= ['user_message'],inplace = True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['date_new'] = df['date'].dt.date
    df['day_name']= df['date'].dt.day_name()
    hour = []
    for h in df[['hour','day_name']]['hour']:
        if option2 == '24 hour formate':
            hour.append(str(h%24)+'-'+str((h+1)%24))
        else:
            hour.append(str(h%12)+'-'+str((h+1)%12))
    df['new_h'] = hour
    return df,option
