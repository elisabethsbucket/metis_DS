import pandas as pd
import streamlit as st
import xgboost as xgb
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
from google.oauth2 import service_account



header = st.beta_container()
dataset = st.beta_container()
features = st.beta_container()




import pandas as pd
import sqlite3

import pandas as pd
import sqlite3


# ------------------- below is the code that works for streamlit use ------------------

# con = sqlite3.connect("test1.db") #, timeout=30)

# query = con.execute("SELECT * from md_5") #10000 rows of data because sqlite cannot handle the 300,000 rows of data and I do not have access to mongo db
# cols = [column[0] for column in query.description]
# a= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)

# a.columns = ['Age', 'Condition', 'Date','Drug', 'DrugId', 'EaseofUse', 'Effectiveness','Reviews', 'Satisfaction', 'Sex', 'Sides', 'UsefulCount']

# ------------------- above is the code that works for streamlit use ------------------


#using the CSV file

a = pd.read_csv('webmd.csv')
a = a.dropna(how='any',axis=0)

# For clients Illness
condition= 'Select a condition.'
origin_list = [condition] + sorted(a.Condition.unique())
default_value_route = ""
default_value_dest_city = ""


origin_choice = st.sidebar.selectbox('Illness/Ailment', origin_list, index=0)



# For Clients ease of use tolerance
tolerance= 'Select a tolerance level.'
tolerance_list = [tolerance] + sorted(a[a['Condition']== origin_choice].EaseofUse.unique())


#create tolerance selection
tol_choice = st.sidebar.selectbox('Tolerance Level', tolerance_list, index=0)


with header:
    st.title('Medication Database for varying Illnesses')
    st.image('pills.jpg', width = 350)

    st.markdown('This tool may be used to idenitfy prescriptions available for varying illnesses. On the left please select the condition you are interested in followed by your ease of use and comfort level with treating this illness.')

with dataset:

    st.markdown('Prescriptions available and their average effectiveness and Satisfaction for ' + str(origin_choice) + ' can be found below:')


    b=a[a['Condition']== origin_choice]
    k=b[b['EaseofUse']== tol_choice]
    c=k[['Drug', 'Effectiveness', 'Satisfaction']].groupby(['Drug']).mean().reset_index()
    c['Effectiveness']= c['Effectiveness'].astype(float)
    c['Satisfaction']= c['Satisfaction'].astype(float)
    c.sort_values(by=['Effectiveness'], ascending=False)
    st.write(c)
    try:
        st.markdown('One of the highest rated effective drugs for this illness is ' + str(c.iloc[c['Effectiveness'].argmax()][0]) + ' with a rating of ' + str(c.iloc[c['Effectiveness'].argmax()][1]) + '.')
    except ValueError:
        ''
    try:
        st.markdown('Further, one of the highest rated satisfactory drugs for this illness is ' + str(c.iloc[c['Satisfaction'].argmax()][0]) + ' with a rating of ' + str(c.iloc[c['Satisfaction'].argmax()][1]) + '.')
    except ValueError:
        ''
    try:
        st.write(('The number of reviews we have for the most effective drug is ' + str(len(a[a['Drug']== c.iloc[c['Effectiveness'].argmax()][0]])) + '. '))
    except ValueError:
        ''
    

    st.markdown('Up to ten Prescription reviews for ' + str(origin_choice) + ' can be found below:')


    b=a[(a['Condition'] == origin_choice) & (a['EaseofUse'] == tol_choice)]
    c=b[['Drug','Reviews']].drop_duplicates()
    st.write(c.head(10))


