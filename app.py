import streamlit as st
import preprocess,helper
import matplotlib.pyplot as plt
import seaborn as sns
l= []
st.sidebar.title("WhatsApp chat analyser")
uploaded_file = st.sidebar.file_uploader("Choose a WhatApp export chat file without attechment of media")
if uploaded_file is not None:
    def help():
        option = st.sidebar.selectbox("What device you used",('iPhone','Android'))   
        return option
    bytes_data = uploaded_file.getvalue()
    file = uploaded_file.getvalue().decode("utf-8")
    df = preprocess.pre(file)
    user_list = df['user'].unique().tolist()
    # if option == 'iPhone':
    # user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    # st.write(user_list)
    select = st.sidebar.selectbox("show analysis wrt ",user_list)    
    bu = st.sidebar.button('Show analysis')
    if bu:
        num_m,num_w,num_media,lenght_link = helper.stat(select,df)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header('Total messages')
            st.subheader(num_m) 
        with col2:
            st.header('Total word')
            st.subheader(num_w)
        with col3:
            st.header('Total Media')
            st.subheader(num_media)
        with col4:
            st.header('Total Links')  
            st.subheader(lenght_link) 

        t_m = helper.timeline(select,df)
        fig,ax = plt.subplots()
        st.title("Time line wrt messages")
        ax.plot(t_m['time'],t_m['message'],color='green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        daily_tm = helper.daily(select,df)
        fig,ax = plt.subplots()
        st.title("Daily time line")
        ax.plot(daily_tm['date_new'],daily_tm['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        busy_d = helper.week_activity(select,df)
        busy_m = helper.month_activity(select,df)
        col1,col2 = st.columns(2)
        with col1:
            st.title("Most busy day")
            fig,ax = plt.subplots()
            ax.bar(busy_d.index,busy_d.values)
            plt.xticks(rotation ='vertical')
            st.pyplot(fig)
        with col2:
            st.title("Most busy month")
            fig,ax = plt.subplots()
            ax.bar(busy_m.index,busy_m.values,color='yellow')
            plt.xticks(rotation ='vertical')
            st.pyplot(fig)


        if select == 'Overall':
            name,value,y = helper.busy(df)
            st.title("Most busy member")
            fig,ax = plt.subplots()
            # ax.bar(name,value)
            # st.pyplot(fig)
            # plt.xticks(rotation = 'vertical')
            # plt.show()
            col1,col2 = st.columns(2)
            with col1:
                ax.bar(name,value,color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(y)
        st.title("Word cloud")
        op= helper.word_cloud(select,df)
        fig,ax = plt.subplots()
        plt.imshow(op)
        st.pyplot(fig)
        per = helper.perticular(select,df)
        fig,ax = plt.subplots()
        ax.barh(per[0],per[1])
        plt.xticks(rotation = 'vertical')
        st.title("Most Commen word")
        st.pyplot(fig)
        r = helper.emoji(select,df)
        st.title("Most Commen emoji")
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(r)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(r[1].head(5),labels=r[0].head(5),autopct="0.2f")
            st.pyplot(fig)

        table = helper.heat(select,df)
        st.title("Weekly activity map")
        fig,ax= plt.subplots()
        ax=sns.heatmap(table)
        plt.yticks(rotation = 'horizontal')
        st.pyplot(fig)
