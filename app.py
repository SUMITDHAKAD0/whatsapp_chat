import streamlit as st
import pandas as pd

import matplotlib.pylab as plt
import seaborn as sns
import emoji

import src.preprocessing as pp
import src.chat_analysis as ca

f = open('TAI_chat_data.txt', mode = 'r', encoding = 'utf-8')
data = f.read()

st.markdown("<h1 style='text-align: center; color: Red;'>Whatsapp Chat Analizer</h1>", unsafe_allow_html=True)
st.sidebar.title('Whatsapp Chat Analizer')

text_file = st.sidebar.file_uploader('Choose a file')
if text_file is not None:
    byte_data = text_file.getvalue()
    data = byte_data.decode("utf-8")

    # st.title('Whatsapp Chat Analizer')
    df = pp.preprocess(data)
    # st.dataframe(df)

    # selecting unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Select User ',user_list)
    if st.sidebar.button('Show Analysis'):
        
        # Stats Area
        num_messages, words, num_media_messages, num_links = ca.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Total Msg's")
            st.subheader(num_messages)
        with col2:
            st.subheader("Total Words")
            st.subheader(words)
        with col3:
            st.subheader("Media Shared")
            st.subheader(num_media_messages)
        with col4:
            st.subheader("Links Shared")
            st.subheader(num_links)

        # user monthly timeline 
        st.title('Monthly User Timeline')
        col1, col2 = st.columns([2,1])
        monthly_time_line = ca.monthly_timeline(selected_user, df)
        with col1:
            fig, ax = plt.subplots()
            ax.plot(monthly_time_line['time'], monthly_time_line['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(monthly_time_line[['time', 'message']])

        # user Daily timeline 
        st.title('Daily User Timeline')
        col1, col2 = st.columns([2,1])
        daily_time_line = ca.daily_timeline(selected_user, df)
        with col1:
            fig, ax = plt.subplots()
            ax.plot(daily_time_line['only_date'], daily_time_line['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(daily_time_line[['only_date', 'message']])

        # weekly and monthly activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Most Busy Day in Week')
            busy_day = ca.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.subheader('Most Busy Month in Year')
            busy_month = ca.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)



        # finding most busy user in the group
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            col1, col2 = st.columns(2)
            x, new_df = ca.most_busy_user(df)
            

            with col1: 
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                # claculating message percentage
                st.dataframe(new_df)               

        # create word cloud
        st.title('Word Cloud')
        df_wc = ca.word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words used
        st.title('Most Common Words Used')
        col1, col2 = st.columns(2)
        most_common_words_df = ca.most_common_words(selected_user, df)
        with col1:
            fig, ax = plt.subplots()
            ax.bar(most_common_words_df['word'], most_common_words_df['frequency'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(most_common_words_df)

        # Emoji analysis
        st.title("Common used Emoji's")
        col1, col2 = st.columns(2)
        emoji_df = ca.emoji_analysis(selected_user, df)
        if emoji_df.shape[0] != 0:
            with col1:
                fig, ax = plt.subplots()
                ax.pie(emoji_df['frequency'].head(), labels=emoji_df['emoji'].head(), autopct="%0.2f")
                st.pyplot(fig)
            with col2:
                st.dataframe(emoji_df)

        # activity heat mam
        st.title('Activaty Heat Map')
        fig, ax = plt.subplots()
        activity_heatmap_df = ca.activity_heat_map(selected_user, df)
        ax = sns.heatmap(activity_heatmap_df, annot=True)       
        plt.xticks(rotation = 'vertical')
        plt.yticks(rotation = 'horizontal')
        st.pyplot(fig)





