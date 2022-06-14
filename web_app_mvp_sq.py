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

con = sqlite3.connect("test1.db") #, timeout=30)


query = con.execute("SELECT * from md_5") #10000 rows of data because sqlite cannot handle the 300,000 rows of data and I do not have access to mongo db
cols = [column[0] for column in query.description]
a= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)

a.columns = ['Age', 'Condition', 'Date','Drug', 'DrugId', 'EaseofUse', 'Effectiveness','Reviews', 'Satisfaction', 'Sex', 'Sides', 'UsefulCount']


# For clients Illness
condition= 'Select a condition.'
origin_list = [condition] + sorted(a.Condition.unique())
default_value_route = ""
default_value_dest_city = ""


origin_choice = st.sidebar.selectbox('Illness/Ailment', origin_list, index=0)



# For Clients ease of use tolerance
tolerance= 'Select a tolerance level.'
tolerance_list = [tolerance] + sorted(a.EaseofUse.unique())


#create tolerance selection
tol_choice = st.sidebar.selectbox('Tolerance Level', tolerance_list, index=0)


with header:
    st.title('Medication Database for varying Illnesses')
    st.image('pills.jpg', width = 400)

    st.subheader('This tool may be used to idenitfy prescriptions available for varying illnesses. On the left please select the condition you are interested in and your tolerance/ease of use comfortability level.')

with dataset:

    st.subheader('Prescriptions available and their average effectiveness and Satisfaction for ' + str(origin_choice) + ' can be found below:')


    b=a[((a['Condition'] == origin_choice) & (a['EaseofUse']) == tol_choice)]
    c=b[['Drug', 'Effectiveness', 'Satisfaction']].groupby(['Drug']).mean().reset_index()
    c['Effectiveness']= c['Effectiveness'].astype(float)
    c['Satisfaction']= c['Satisfaction'].astype(float)
    c.sort_values(by=['Effectiveness'], ascending=False)
    st.write(c)


    st.subheader('Prescription reviews for ' + str(origin_choice) + ' can be found below:')


    b=a[(a['Condition'] == origin_choice) & (a['EaseofUse'] == tol_choice)]
    c=b[['Drug','Reviews']].drop_duplicates()
    #c['Effectiveness']= c['Effectiveness'].astype(float)
    #c.sort_values(by=['Effectiveness'], ascending=False)
    st.write(c)

    #st.subheader('Prescription reviews for ' + str(origin_choice) + ' can be found below:') #heatmap here



