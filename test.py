import pandas as pd
import logging

SOURCE_TEXTS = "assets/text.xlsx"
SOURCE_METRICS = "assets/metrics.csv"

def count_digits(value):
    value = int(value)
    value = abs(value)
    value = str(value)
    value = len(str)
    return value

def read_texts(source = SOURCE_TEXTS, sheet_name = 0):
    df = pd.read_excel(source, sheet_name=sheet_name)
    return df

def read_metrics(source = SOURCE_METRICS):
    df = pd.read_csv(source, encoding='utf-16')
    logging.info('WTF?')
    return df

def get_metric(df, title, value_col, title_col = 'Title', unit='bn', currency='USD'):
    df = df
    value = df[value_col][df[title_col]==title].iloc[0]
    if unit == '%':
        value = "{:.1%}".format(value)
    elif unit == 'k':
        value = "{:.2f}".format(value)
        value = f'{value} {currency}k'
    elif unit == 'mn':
        value = "{:.2f}".format(value)
        value = f'{value} {currency}mn'
    elif unit == 'bn':
        value = "{:.2f}".format(value)
        value = f'{value} {currency}bn'
    elif abs(value) > 99:
        value = "{:.0f}".format(value)
    elif abs(value) > (10**3):
        value = value / (10**3)
        value = "{:.2f}".format(value)
        value = f'{value} {currency}k'
    elif abs(value) > (10**6):
        value = value / (10**6)
        value = "{:.2f}".format(value)
        value = f'{value} {currency}mn'
    elif abs(value) > (10**9):
        value = value / (10**9)
        value = "{:.2f}".format(value)
        value = f'{value} {currency}bn'
    return value

df_m = read_metrics()
value = get_metric(df_m, 'International Reserves', 'Last value')
print(value)
