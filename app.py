# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 17:52:12 2021

@author: Anand
"""


#%%writefile app1.py
 
import pickle
import streamlit as st
import pandas as pd
import numpy as np
 
# loading the trained model
pickle_in = open('model.pkl', 'rb') 
classifier = pickle.load(pickle_in)
 
@st.cache()
  
# defining the function which will make the prediction using the data which the user inputs
# Variables input to this function are from user, we will convert them in order to feed the model 
def prediction(dom,season,yr,mnth,holiday,weekday,workingday,weather,temp,hum,windspeed,casual_reg):
    weekday_dict = {'Monday':1,'Tuesday':2,'Wednesday':3,'Thursday':4, 'Friday':5,'Saturday':6, 'Sunday':0}
    weather_dict = {'Clear, Few clouds, Partly cloudy, Partly cloudy':1,
                    'Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist':2,
                    'Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds':3,
                    'Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog':4}
    season_dict = {'Spring':1,'Summer':2,'Fall':3, 'Winter':4}
     
    if season in season_dict:
        season = season_dict[season]
#Converting input of weekday to numerical value    
    if weekday in weekday_dict:
        weekday = weekday_dict[weekday]

#Converting input of weekday to numerical value    
    if weather in weather_dict:
        weathersit = weather_dict[weather]
    
    # Making predictions 
    prediction = classifier.predict( 
        np.array([[dom,season,yr,mnth,holiday,weekday,workingday,weathersit,temp,hum,windspeed,casual_reg]]))
     
#    if prediction == 0:
#        pred = 'Not Default'
#    else:
#        pred = 'Default'
    return int(prediction)
      
  
# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:yellow;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Bank Loan Prediction</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # following lines create boxes in which user can enter data required to make prediction 
    dom = st.selectbox("Day of the Month", range(1,32))
    season = st.selectbox("Season of the Year",['Spring','Summer','Fall','Winter'],index = 0)
    yr = st.selectbox("Year", [0,1], help = '0: 2011, 1:2012') 
    mnth = st.selectbox("Month" , range(1,13))
    holiday = st.selectbox("Whether or not it is Holiday",[0,1], help = 'If day is neither weekend nor holiday is 1, otherwise is 0')
    weekday = st.selectbox("Day of the week" , ['Monday','Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday'])
    workingday = st.selectbox("Whether or not it is Workingday" , [0,1], help = 'If day is neither weekend nor holiday is 1, otherwise is 0')
    weather = st.selectbox("How is the Weather", ['Clear, Few clouds, Partly cloudy, Partly cloudy',
                                                    'Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist',
                                                    'Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds',
                                                    'Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'])
    temp = st.number_input("Temperature")
    hum = st.number_input("Humidity")
    windspeed = st.number_input("Windspeed")
    casual_reg = st.number_input("Ratio of casual to registered customers")
    result =""
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(dom,season,yr,mnth,holiday,weekday,workingday,weather,temp,hum,windspeed,casual_reg) 
        st.success('The count of bikes rented is {}'.format(result))
        #print(result)
     
if __name__=='__main__': 
    main()