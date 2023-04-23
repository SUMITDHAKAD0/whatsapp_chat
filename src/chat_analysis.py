import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()



def fetch_stats(selected_user, df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #  dataset shape
    num_messages = df.shape[0]

    # claculating total number of words  
    words = []
    for msg in df['message']:
        words.extend(msg.split())

    # calculating number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # claculating total number of links 
    num_links = []
    for msg in df['message']:
        words.extend(extract.find_urls(msg))

    return num_messages, len(words), num_media_messages, len(num_links)

def most_busy_user(df):
    
    x = df['user'].value_counts().head()
    # claculating message percentage
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns = {'index':'user', 'user': 'percentage'})
    return x, df

def word_cloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # removing group notifications and media omitted
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # reading stop word file
    f = open('stop_hinglish.txt', mode = 'r', encoding = 'utf-8')
    stop_words = f.read()

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=400, height=300, min_font_size=16, background_color='white')
    # temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep = " "))
    return df_wc

def most_common_words(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    # removing group notifications and media omitted
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # reading stop word file
    f = open('stop_hinglish.txt', mode = 'r', encoding = 'utf-8')
    stop_words = f.read()

    # removing stop words from data 
    words = []
    for msg in temp['message']:
        for word in msg.lower().split():
            words.append(word)
    
    # If you want to remove stop words the uncomment this code from line no. (88-92) and connemt (81-84)
    # words = []
    # for msg in temp['message']:
    #     for word in msg.lower().split():
    #         if word not in stop_words:
    #             words.append(word)


    # most common used words 
    most_common_words_df = pd.DataFrame(Counter(words).most_common(20))
    # most_common_words_df.rename(columns = {'0':'word', '1': 'frequency'})
    return most_common_words_df.rename(columns = {0:'word', 1: 'frequency'}) 

def emoji_analysis(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # extrating mostly used emojis from text
    emojis = []
    for msg in df['message']:
        emojis.extend([i for i in msg if emoji.distinct_emoji_list(i)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df.rename(columns = {0:'emoji', 1: 'frequency'})

def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # apply groupby on year and month
    monthly_time_line = df.groupby(['year', 'month']).count()['message'].reset_index()
    
    # merging month and year columns
    time = []
    for i in range(monthly_time_line.shape[0]):
        time.append(monthly_time_line['month'][i] + '-' + str(monthly_time_line['year'][i]))
    monthly_time_line['time'] = time

    return monthly_time_line

def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_time_line = df.groupby(['only_date']).count()['message'].reset_index()

    return daily_time_line

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heat_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    activity_heatmap_df = df.pivot_table(index = 'day_name', columns = 'period', values = 'message', aggfunc='count').fillna(0)
    return activity_heatmap_df
