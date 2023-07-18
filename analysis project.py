#!/usr/bin/env python
# coding: utf-8

# # Project: Retail Analysis with Walmart Data
# ## Introduction
# ### This data set contains information about Historical sales data for 45 Walmart stores located in different regions are available.
# ### This is the historical data that covers sales from 2010-02-05 to 2012-11-01, in which you will find the following fields:
# #### • Store - the store number
# #### • Date - the week of sales
# #### • Weekly_Sales - sales for the given store
# #### • Holiday_Flag - whether the week is a special holiday week 1 – Holiday week 0 – Non-holiday week
# #### • Temperature - Temperature on the day of sale
# #### • Fuel_Price - Cost of fuel in the region
# #### • CPI – Prevailing consumer price index
# #### • Unemployment - Prevailing unemployment rate
# ### and they have a strong relationship that we will show in this project
# ### Example about questions that we Interested for Analysis:
# #### Which store has maximum sales?
# #### Which store has maximum standard deviation i.e., the sales vary a lot
# #### Some holidays have a negative impact on sales. Find out holidaysthat have higher sales than the mean sales in the non-holiday season for all stores together.
# #### Provide a monthly and semester view of sales in units and give insights.
# #### Plot the relations between weekly sales vs. other numeric features and give insights

# ## Importing Libraries

# In[88]:


# import packages that we will use 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


#    ##  import and display the data
# 

# In[89]:


data = pd.read_csv("walmart-sales-dataset-of-45stores.csv")
data.head()


# ##  clean the data
# 

# In[90]:


# explore the Properties of the data
data.info()


# In[91]:


data.describe()


# In[92]:


data.isnull().sum()


# In[93]:


data.duplicated().any()


# ## Value Distribution
# 

# In[94]:


# hist graph about our data 
data.hist(figsize=(15,10));


# In[95]:


data.plot(subplots=True, grid=True, figsize=(15,15));


# # Exploratory Data Analysis

# ### Research Question 1: Which store has maximum sales?
# 

# In[8]:


df1 = data.groupby("Store")["Weekly_Sales"].agg(['sum'])


# In[9]:


#I take top 10 store to analysis it 
df1_top = df1.sort_values(by='sum',ascending = False).reset_index()
df_store=df1_top[0:10]
df_store


# In[10]:


dd = df_store.sort_values(by='sum')
dd


# In[28]:


fig, ax = plt.subplots(figsize=(13,7))
sns.barplot(data= dd, x="Store", y="sum", ax=ax)
plt.title('Top 10 stores with sales',size=30)
plt.xlabel("store", size=25 )
plt.ylabel(" sales ", size=25)
plt.show()


# ### Conclusion : Store 20 has the Maximum Weekly Sales and store 4 is close to him
# 
# 
# 
# 

# ### Research Question 2: Which store has maximum standard deviation?

# In[20]:


std_stores = data.groupby('Store', as_index=False).agg(Std_of_Weekly_Sales=('Weekly_Sales','std'))


# In[29]:


std_stores[(std_stores['Std_of_Weekly_Sales'] == max(std_stores['Std_of_Weekly_Sales']))]


# In[33]:


#I take top 10 store to analysis it 
std_stores = std_stores.sort_values(by='Std_of_Weekly_Sales',ascending = False)
std_stores=std_stores[0:10]
std_stores


# In[34]:


ddf = std_stores.sort_values(by='Std_of_Weekly_Sales')
ddf


# In[42]:


fig, ax = plt.subplots(figsize=(13,7))
sns.barplot(data=ddf, x="Store", y="Std_of_Weekly_Sales", ax=ax)
plt.title('vary in sales',size=35)
plt.xlabel("store", size=25 )
plt.ylabel(" Std ", size=25)
plt.show()


# ### Conclusion : The Weekly Sales vary a lot in Store 14

# 
# 
# ## Research Question 3: Some holidays have a negative impact on sales. Find out holidays that have higher sales than the mean sales in the non-holiday season for all stores together.

# In[20]:


data.head()


# In[21]:


df_non_holiday = data[(data.Weekly_Sales > 0) & (data.Holiday_Flag == 0)]


# In[22]:


df_non_holiday.Weekly_Sales.mean()


# In[23]:


df_holiday = data[(data.Weekly_Sales > 1041256.3802088564) & (data.Holiday_Flag == 1)]


# In[24]:


df_holiday


# ###  Name of the Holidays is given in the Dataset Description.

# In[25]:


def assign_holiday(date):
    if date in ['12-02-2010', '11-02-2011', '10-02-2012']:
        return 'Super Bowl'
    elif date in ['10-09-2010', '09-09-2011', '07-09-2012']:
        return 'Labour Day'
    elif date in ['26-11-2010', '25-11-2011', '23-11-2012']:
        return 'Thanksgiving'
    elif date in ['31-12-2010', '30-12-2011', '28-12-2012']:
        return 'Christmas'
    else:
        return 'Non-Holiday' 


# In[26]:


data['Holiday'] = data['Date'].apply(assign_holiday)
data


# In[27]:


mean_df = data.groupby('Holiday').agg(Mean_Weekly_Sales=('Weekly_Sales','mean')).reset_index()
mean_df


# In[33]:


dd = mean_df.sort_values(by='Mean_Weekly_Sales')
dd


# In[32]:


fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(data=dd, x="Holiday", y="Mean_Weekly_Sales", ax=ax)
plt.title('Top holidays with sales',size=30)
plt.xlabel("Holiday_Name", size=22 )
plt.ylabel(" Mean_Sales ", size=25)
plot.show()


# ### Conclusion: Labour Day Week, Super Bowl Week and Thanksgiving Week have negative impact on Sales, which means they have higher sales than the Mean of Non-Holiday Week sales

# ### Question 4: Provide a monthly and semester view of sales in units and give insights.

# In[83]:


data["Date"] = pd.to_datetime(data["Date"])
data["Month"] = data["Date"].dt.month


# In[45]:


counts = data["Month"].value_counts()


# In[46]:


data["Semester"] = "1"
data.loc[data["Month"].isin([4,5,6]), "Semester"] = "2"
data.loc[data["Month"].isin([7, 8 ,9]), "Semester"] = "3"
data.loc[data["Month"].isin([10, 11, 12]), "Semester"] = "4"


# In[48]:


monthly_sales = data.groupby("Month")['Weekly_Sales'].sum()
semester_sales = data.groupby("Semester")["Weekly_Sales"].sum()


# In[49]:


monthly_sales


# In[50]:


semester_sales


# ### The correlation between months and sales

# In[51]:


# plot the monthly sales
plt.plot(monthly_sales)
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.title('Monthly Sales')
plt.show()


# #### As we can see sales tend to get higher in April and May and tend to get very low around November.

# ### The correlation between months and sales

# In[52]:


#plot the semester sales
plt.plot(semester_sales)
plt.xlabel('Semester')
plt.ylabel('Total Sales')
plt.title('Semester Sales')
plt.show()


# #### As we can see semester 2 is the best sales option.

# ### The relations between weekly sales vs. other numeric features

# In[55]:


# make a subplot that constu=itutes of 4 different plots
fig, ax = plt.subplots(2, 2, figsize=(12, 10))

# the first plot is to show the correlation between temperature and weekly sales
ax[0, 0].set_title("temperature vs weekly sales")
ax[0, 0].set_xlabel("temperature")
ax[0, 0].set_ylabel("Weekly sales")
ax[0, 0].plot(data.groupby('Temperature')['Weekly_Sales'].sum())

# the second plot is to show the correlation between fuel price and weekly sales
ax[0, 1].set_title("fuel vs weekly sales")
ax[0, 1].set_xlabel("fuel")
ax[0, 1].set_ylabel("Weekly sales")
ax[0, 1].plot( data.groupby('Fuel_Price')['Weekly_Sales'].sum(), color = "black")

# the third plot is to show the correlation between CPI and weekly sales
ax[1, 0].set_title("CPI vs weekly sales")
ax[1, 0].set_xlabel("CPI")
ax[1, 0].set_ylabel("Weekly sales")
ax[1, 0].plot(data.groupby('CPI')['Weekly_Sales'].sum(), color = "green")

# the fourth plot is to show the correlation between the date and weekly sales
ax[1, 1].set_title("Date vs weekly sales")
ax[1, 1].set_xlabel("Date")
ax[1, 1].set_ylabel("Weekly sales")
plt.xticks(rotation=90 )
ax[1, 1].plot(data.groupby('Date')['Weekly_Sales'].sum(), color = "orange")

# Display the figure
plt.show()


# ### Basesd on our findings, it is clear that,
# 1) best sales are between 50 and 80 fahrenheit degrees.
# 
# 2) sales get lower when fuel prices get over 4 usd and are the best when the prices are areound 3.60 usd.
# 
# 3) There is a plain negative correlation between the CPI and the weekly sales.
# 
# 4) weekly sales are the best in the holidays season in december.

# ### weekly sales vs. Unemployment rate.

# In[59]:


plt.title('Weekly Sales vs Unemployment Rate')

plt.xlabel('Unemployment Rate')
plt.ylabel('Weekly Sales')
plt.bar(data['Unemployment'].unique(), data.groupby('Unemployment')['Weekly_Sales'].sum(), color = "purple");


# #### we conclude that, when the unemployment rate is around 9, we find the best weekly sales.

# ### weekly sales vs. Temperature.

# In[62]:


plt.title('fuel price vs weekly sales', fontsize=20)

# Set the x-axis label and y-axis label for the scatter plot with a red color
plt.xlabel('fuel price')
plt.ylabel('weekly sales')
plt.scatter(data['Fuel_Price'], data['Weekly_Sales'], color='red', edgecolor='black');


# #### we find that sales get lower when fuel prices are over 4 usd.

# ### weekly sales vs. Unemployment.

# In[66]:


plt.title('Unemployment vs weekly sales', fontsize=20)

# Set the x-axis label and y-axis label for the scatter plot with a red color
plt.xlabel('unemployment')
plt.ylabel('weekly sales ')
plt.scatter(data['Unemployment'], data['Weekly_Sales'], edgecolor='black');


# #### we can see that when the unemployment rate exceeds 10, sales tend to get lower.

# ### Holiday sales vs. non- holiday sales.

# In[85]:


holiday_sales = data.groupby("Holiday_Flag")["Weekly_Sales"].sum()
plt.pie(holiday_sales)
plt.legend( ["non-holiday", "holiday"]);


# #### It is worth noting that, Holiday sales make a good chunk of our sales even though, they are not that many But of course, non-holiday sales are much higher.

# # Conclusions

# ## After analyzing the data, we conclude that:

# ### `1.` Store 20 has the Maximum Weekly Sales and store 4 is close to him.
# ### `2.` The Weekly Sales vary a lot in Store 14.
# ### `3.` Labour Day Week, Super Bowl Week and Thanksgiving Week have negative impact on Sales, which means they have higher sales than the Mean of Non-Holiday Week sales.
# ### `4.` sales tend to get higher in April and May and tend to get very low around November.
# ### `5.` semester 2 is the best sales option.
# ### `6.` best sales are between 50 and 80 fahrenheit degrees.
# ### `7.` sales get lower when fuel prices get over 4 usd and are the best when the prices are areound 3.60 usd.
# ### `8.` There is a plain negative correlation between the CPI and the weekly sales.
# ### `9.` weekly sales are the best in the holidays season in december.
# ### `10.` when the unemployment rate is around 9, we find the best weekly sales.
# ### `11.` sales get lower when fuel prices are over 4 usd.
# ### `12.` when the unemployment rate exceeds 10, sales tend to get lower.
# ### `13.` It is worth noting that, Holiday sales make a good chunk of our sales even though, they are not that many But of course, non-holiday sales are much higher.
