import re
import pandas as pd
from app import help

def pre(data):
    option = help()
    if option == 'iPhone':
        p = "\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s\w[A-Z]\]"
        message = re.split(p, data)[1:]
        time = re.findall(p,data)
        df= pd.DataFrame({'user_message':message, 'time':time})
        df['time'] = pd.to_datetime(df['time'],format="[%d/%m/%y, %H:%M:%S %p]") 
        df.rename(columns= {'time':'date'},inplace = True)
    else: 
        p = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w[a-zA-Z]\s-\s"
        message = re.split(p, data)[1:]
        time = re.findall(p,data)
        df = pd.DataFrame({'user_message':message, 'date_o':time})
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
        hour.append(str(h%13)+'-'+str((h+1)%13))
    df['new_h'] = hour
    return df