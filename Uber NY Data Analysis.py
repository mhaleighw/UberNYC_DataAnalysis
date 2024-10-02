#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


import os


# In[3]:


os.listdir(r"/Users/haleigh/Desktop/Udemy Courses/Data Analysis Projects/Uber Project/Datasets")


# In[4]:


# obtaining the dataset
uber_15 = pd.read_csv(r"/Users/haleigh/Desktop/Udemy Courses/Data Analysis Projects/Uber Project/Datasets/uber-raw-data-janjune-15_sample.csv")


# In[5]:


# showing rows and columns shape
uber_15.shape


# In[6]:


# checking type
type(uber_15)


# In[7]:


# checking for duplications
uber_15.duplicated().sum()


# In[8]:


uber_15.drop_duplicates(inplace=True)


# In[9]:


uber_15.duplicated().sum()


# In[10]:


uber_15.shape


# In[11]:


uber_15.dtypes


# In[12]:


uber_15.isnull().sum()


# In[13]:


# find the first pick up date
uber_15['Pickup_date'][0]


# In[14]:


uber_15['Pickup_date'] = pd.to_datetime(uber_15['Pickup_date'])


# In[15]:


uber_15['Pickup_date'].dtype


# In[16]:


uber_15['Pickup_date'][0]


# In[17]:


type(uber_15['Pickup_date'][0])


# In[18]:


uber_15.dtypes


# In[19]:


# analysing which month has the maximum uber pickups in NYC?
# extract the month feature
uber_15


# uber_15['month'] = uber_15['Pickup_date'].dt.month_name()

# In[20]:


uber_15['month'] = uber_15['Pickup_date'].dt.month_name()


# In[21]:


uber_15['month']


# In[22]:


#freq. table
uber_15['month'].value_counts()


# In[23]:


uber_15['month'].value_counts().plot(kind='bar')


# In[24]:


uber_15['Weekday'] = uber_15['Pickup_date'].dt.day_name()
uber_15['Day'] = uber_15['Pickup_date'].dt.day
uber_15['Hour'] = uber_15['Pickup_date'].dt.hour
uber_15['Minute'] = uber_15['Pickup_date'].dt.minute


# In[25]:


uber_15.head(4)


# In[26]:


pivot = pd.crosstab(index=uber_15['month'], columns=uber_15['Weekday'])


# In[27]:


# create grouped bar chart
pivot.plot(kind='bar', figsize = (8,6))


# In[31]:


# finding hourly rush in NYC for all days
summary = uber_15.groupby(['Weekday', 'Hour'], as_index = False).size()


# In[32]:


summary


# In[33]:


# making point plot
plt.figure(figsize=(8,6))
sns.pointplot(x="Hour", y="size", hue="Weekday", data=summary)


# In[36]:


# show which base number has the MOST number of active vehicles
# pull from data set to get the base_number and active vehicles
uber_foil = pd.read_csv(r"/Users/haleigh/Desktop/Udemy Courses/Data Analysis Projects/Uber Project/Datasets/Uber-Jan-Feb-FOIL.csv")


# In[37]:


uber_foil.shape


# In[38]:


uber_foil.head(3)


# In[39]:


# making box plot
get_ipython().system('pip install chart_studio')
get_ipython().system('pip install plotly')


# In[40]:


import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.express as px

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


# In[41]:


init_notebook_mode(connected=True)


# In[42]:


uber_foil.columns


# In[43]:


px.box(x='dispatching_base_number', y='active_vehicles', data_frame = uber_foil)


# In[45]:


px.violin(x='dispatching_base_number', y='active_vehicles', data_frame = uber_foil)


# In[46]:


# collect entire data for data analysis
# Big Data --> new .csv file
files = [
    'uber-raw-data-apr14.csv', 'uber-raw-data-aug14.csv',
    'uber-raw-data-jul14.csv', 'uber-raw-data-jun14.csv',
    'uber-raw-data-may14.csv', 'uber-raw-data-sep14.csv'
]
# concatenate these files


# In[51]:


final = pd.DataFrame()
path = r"/Users/haleigh/Desktop/Udemy Courses/Data Analysis Projects/Uber Project/Datasets"

for file in files:
    current_df = pd.read_csv(path+'/'+file)
    final = pd.concat([current_df, final])


# In[49]:


final.shape


# In[52]:


final.duplicated().sum()


# In[53]:


final.drop_duplicates(inplace=True)


# In[54]:


final.shape


# In[55]:


final.head(3)


# In[61]:


# spatial analysis / locations for uber pick up rushes
# map based visualization
rush_uber = final.groupby(['Lat', 'Lon'], as_index=False).size()


# In[62]:


rush_uber.head(6)


# In[63]:


# create base map
get_ipython().system('pip install folium')


# In[64]:


import folium


# In[65]:


basemap = folium.Map()


# In[66]:


from folium.plugins import HeatMap


# In[67]:


HeatMap(rush_uber).add_to(basemap)


# In[68]:


# zoom in to see NYC and Manhattan
basemap


# In[71]:


final['Date/Time'][0]


# In[73]:


# pair wise analysis to figure out the rush (on hr and weekday)
final['Date/Time'] = pd.to_datetime(final['Date/Time'], format="%m/%d/%Y %H:%M:%S")


# In[74]:


final['Date/Time'].dtype


# In[79]:


final['Day'] = final['Date/Time'].dt.day
final['Hour'] = final['Date/Time'].dt.hour


# In[80]:


final.head(4)


# In[82]:


pivot = final.groupby(['Day', 'Hour']).size().unstack()


# In[83]:


pivot


# In[84]:


pivot.style.background_gradient()


# In[89]:


# automating analysis
def gen_pivot_table(df, col1, col2):
    pivot = final.groupby([col1, col2]).size().unstack()
    return pivot.style.background_gradient()


# In[90]:


final.columns


# In[91]:


gen_pivot_table(final, "Day", "Hour")

