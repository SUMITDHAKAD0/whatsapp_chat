import re
import pandas as pd

def preprocess(data):
    """
        returns text data into dataframe
    """
    #extrating data and message from text and  spliting them
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    msg = re.split(pattern, data)[1:]

    pattern1 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}'
    dates = re.findall(pattern1, data)

    # creating dataframe
    df = pd.DataFrame({'date' : dates ,'user_message':msg})

    # converting datetime formate
    df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)

    # spliting user name and message
    user = []
    message = []

    for msg in df['user_message']:
        result = re.split('([\w\W]+?):\s', msg)
        if result[1:]:
            user.append(result[1])
            message.append(result[2])
        else:
            user.append('group_notification')
            message.append(result[0])

    df['user'] = user
    df['message'] = message
    df.drop(['user_message'],axis = 1, inplace=True)

    # extrating date and time
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    
    df['period'] = period

    return df
        
