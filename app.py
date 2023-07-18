import streamlit as st
import pandas as pd
import plotly.express as px

# read in vehicles_us.csv file in the root directory
vehicles_data = pd.read_csv('vehicles_us.csv')

## added a column in the df for manufacturer from the model name
vehicles_data['manufacturer'] = vehicles_data['model'].apply(lambda x: x.split()[0]) 

## filling in missing values for 'model_year', 'cylinders' and 'odometer'
vehicles_data['model_year'] = vehicles_data.groupby(["model"])['model_year'].transform(lambda x: x.fillna(x.median()))
vehicles_data['cylinders'] = vehicles_data.groupby(["model"])['cylinders'].transform(lambda x: x.fillna(x.median()))
vehicles_data['odometer'] = vehicles_data.groupby(["model"])['odometer'].transform(lambda x: x.fillna(x.median()))

## converting 'model_year' and 'date_posted' columns to datetime type.
# vehicles_data['model_year'] = pd.to_datetime(vehicles_data['model_year']).dt.year
vehicles_data['date_posted'] = pd.to_datetime(vehicles_data['date_posted']).dt.date
## converting 'model_year' resulted in an issue with the date and month to be set to 01-01-____
## is there a way to change the type of 'model_year' to datetime with just the year?


###########################################################################
# Start of app on render 
st.header('Data analysis of car sales advertisements.')
st.write('This project contains the raw dataframe of vehicles sold in the US by various manufacturers. The plots in this study are made to be interactive, giving more flexibility to the user, to look closely at the relationships between various varables. Such as, the correlation between the prices of vehicles by the model year or the relationship between the days the ad is listed and the condition of the vehicle.')

st.header('Vehicles data')
st.dataframe(vehicles_data)

st.write('Note: null values from the dataset for columns, "model_year", "cylinders" and "odometer" were filled with their respective model median. The "odometer" column was still null for 41 rows, but this is unlikely to effect the overall analysis due to the small quantity compared to the total 51,525 rows of data.')
# null_values = vehicles_data.isna().sum().reset_index()
# null_values.columns = ['columns', 'null values']
# st.dataframe(null_values)
## do not need to show the number of null values ^^^ in the render app 


st.markdown("---")
########################################################
# interactive graphs
## created a table grouping model and year and geting the average price
st.header('Interactive graphs')
st.subheader('Fig 1. Average price of vehicles by year and model')
avg_price = vehicles_data.groupby(['model', 'model_year'])['price'].mean().reset_index()
fig = px.scatter(avg_price, x="model_year", y="price", color="model")
st.plotly_chart(fig, use_container_width=True)
st.write('Fig 1. gives a glimpse of the changes in the average price of a vehicle model over the years. The graph can be utilized to look at the changes for an individual model or multiple for comparison. The outliers on this plot are clearly visible and further research could be done to look into the reasoning for such distinct prices')
st.write('')

### The total count of each type of car for each manufracturer
st.subheader('Fig 2. Count of each type of car for each manufracturer')
manufracturertypes = px.histogram(vehicles_data, x='manufacturer', color='type')
st.write(manufracturertypes)
st.write('Fig 2. gives a broad view of the total number of each type of vehicle for each manufacturer.')
st.write('')

### Is there any specific reason for the number of days vehicles are listed? 
### perhaps certian types of vehicles sell fasted? how much does the condition play a role?
st.subheader('Fig 3. Compare price distribution between manufacturers')
test=''
df_columns = list(vehicles_data)
# manufac_list = ['model', 'model_year', 'condition', 'manufacturer', 'fuel', 'transmission', 'type']
df_columns.remove('days_listed')
select = st.selectbox('Select ', df_columns, index=df_columns.index('condition'))
test = vehicles_data[select]
normalize = st.checkbox('Normalize histogram', value=False)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

st.write(px.histogram(vehicles_data,
                      x= 'days_listed',
                      nbins=30,
                      color=test,
                      histnorm=histnorm,
                      barmode='overlay'))
## bins could be changed
st.write('Fig 3. has "days_listed" on the x-axis. This graph allows us to see the relationship between the  number of days vehicles are listed and the rest of the columns in the data. By selecting "manufacturer", we can see that each manufacturer follows a similar trend of most vehicles listed for 10-40 days')
st.write('')


##### compare price of two manufacturers
st.subheader('Fig 4. Compare price distribution between manufacturers')
manufac_list = sorted(vehicles_data['manufacturer'].unique())
manufacturer_1 = st.selectbox('Select manufacturer 1',
                              manufac_list, index=manufac_list.index('chevrolet'))

manufacturer_2 = st.selectbox('Select manufacturer 2',
                              manufac_list, index=manufac_list.index('hyundai'))
mask_filter = (vehicles_data['manufacturer'] == manufacturer_1) | (vehicles_data['manufacturer'] == manufacturer_2)
df_filtered = vehicles_data[mask_filter]
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
st.write(px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay'))
st.write('Fig 4. allows us to compare the price of vehicles for two manufacturer of our choice.')