import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

# Load data
day_df = pd.read_csv('./Data/day.csv')
hour_df = pd.read_csv('./Data/hour.csv')

# Preprocessing
day_df.dropna(inplace=True)
hour_df.dropna(inplace=True)
day_df['date'] = pd.to_datetime(day_df['dteday'])
hour_df['date'] = pd.to_datetime(hour_df['dteday'])

day_df['year'] = day_df['date'].dt.year
day_df['month'] = day_df['date'].dt.month

# Sidebar for start and end date selection
st.sidebar.title("Date Range Selection")
min_date = day_df['date'].min()
max_date = day_df['date'].max()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

filtered_day_df = day_df[(day_df['date'] >= pd.to_datetime(start_date)) & (day_df['date'] <= pd.to_datetime(end_date))]

# Dashboard Title
st.title(f"Bike Sharing Dashboard ({start_date} - {end_date})")

# Correlation matrix
numerical_columns = ['temp', 'atemp', 'hum', 'windspeed', 'cnt']
correlation_matrix = filtered_day_df[numerical_columns].corr()
st.subheader('Correlation Matrix')
st.write(correlation_matrix)

# 1. Trend of Bike Rentals Over Time
st.subheader('Trend of Bike Rentals Over Time')
fig = px.line(filtered_day_df, x='date', y='cnt',
              labels={'date': 'Date', 'cnt': 'Number of Rentals'},
              title='Daily Bike Rentals')
st.plotly_chart(fig)

# 2. Temperature vs Bike Rentals
st.subheader('Temperature vs Bike Rentals')
fig = px.scatter(filtered_day_df, x='temp', y='cnt',
                 labels={'temp': 'Temperature (Normalized)', 'cnt': 'Bike Rentals'},
                 title='Temperature vs Bike Rentals')
st.plotly_chart(fig)

# 3. Humidity vs Bike Rentals
st.subheader('Humidity vs Bike Rentals')
fig = px.scatter(filtered_day_df, x='hum', y='cnt',
                 labels={'hum': 'Humidity (Normalized)', 'cnt': 'Bike Rentals'},
                 title='Humidity vs Bike Rentals')
st.plotly_chart(fig)

# 4. Windspeed vs Bike Rentals
st.subheader('Windspeed vs Bike Rentals')
fig = px.scatter(filtered_day_df, x='windspeed', y='cnt',
                 labels={'windspeed': 'Windspeed (Normalized)', 'cnt': 'Bike Rentals'},
                 title='Windspeed vs Bike Rentals')
st.plotly_chart(fig)

# 5. Boxplot: Effect of weather conditions on bike rentals
st.subheader('Effect of Weather Conditions on Bike Rentals')
fig = px.box(filtered_day_df, x='weathersit', y='cnt',
             labels={'weathersit': 'Weather Condition', 'cnt': 'Bike Rentals'},
             title='Bike Rentals under Different Weather Conditions',
             color='weathersit')
fig.update_xaxes(tickvals=[1, 2, 3], ticktext=['Clear', 'Cloudy', 'Rain/Snow'])
st.plotly_chart(fig)

# 6. Average Bike Rentals on Weekdays vs Holidays
st.subheader('Average Bike Rentals on Weekdays vs Holidays')
workingday_mean = filtered_day_df.groupby('workingday')['cnt'].mean().reset_index()
fig = px.bar(workingday_mean, x='workingday', y='cnt',
             labels={'workingday': 'Hari (0 = Hari Libur, 1 = Hari Kerja)', 'cnt': 'Rata-rata Penyewaan Sepeda'},
             title='Average Bike Rentals on Weekdays vs Holidays')
st.plotly_chart(fig)

# 7. Average Bike Rentals by Season
st.subheader('Average Bike Rentals by Season')
season_mean = filtered_day_df.groupby('season')['cnt'].mean().reset_index()
fig = px.bar(season_mean, x='season', y='cnt',
             labels={'season': 'Musim (1 = Winter, 2 = Spring, 3 = Summer, 4 = Fall)', 'cnt': 'Rata-rata Penyewaan Sepeda'},
             title='Average Bike Rentals by Season')
fig.update_xaxes(tickvals=[1, 2, 3, 4], ticktext=['Winter', 'Spring', 'Summer', 'Fall'])
st.plotly_chart(fig)
