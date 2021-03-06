# -*- coding: utf-8 -*-
"""Automatically generated by Colaboratory."""

import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns
from sklearn.linear_model import LinearRegression

"""# Notebook Presentation"""

pd.options.display.float_format = '{:,.2f}'.format

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

"""# Read the Data"""

data = pd.read_csv('cost_revenue_dirty.csv')

"""# Explore and Clean the Data

**Challenge**: Answer these questions about the dataset:
1. How many rows and columns does the dataset contain?
2. Are there any NaN values present?
3. Are there any duplicate rows?
4. What are the data types of the columns?
"""

data.shape
data.isna().values.any()
data.duplicated().values.any()
data.dtypes

"""### Data Type Conversions

**Challenge**: Convert the `USD_Production_Budget`, `USD_Worldwide_Gross`, and `USD_Domestic_Gross` columns to a numeric format by removing `$` signs and `,`. 
<br>
<br>
Note that *domestic* in this context refers to the United States.
"""

# data['USD_Domestic_Gross'] = data['USD_Domestic_Gross'].str.replace("$", "")
# data['USD_Domestic_Gross'] = data['USD_Domestic_Gross'].str.replace(",", "")
# data['USD_Domestic_Gross'] = pd.to_numeric(data['USD_Domestic_Gross'], errors='coerce')
for column in ['USD_Production_Budget', 'USD_Worldwide_Gross']:
  data[column] = data[column].str.replace("$", "")
  data[column] = data[column].str.replace(",", "")
  data[column] = pd.to_numeric(data[column], errors='coerce')
data.head()

"""**Challenge**: Convert the `Release_Date` column to a Pandas Datetime type. """

data['Release_Date'] = pd.to_datetime(data['Release_Date'])
data.head()

"""### Descriptive Statistics

**Challenge**: 

1. What is the average production budget of the films in the data set?
2. What is the average worldwide gross revenue of films?
3. What were the minimums for worldwide and domestic revenue?
4. Are the bottom 25% of films actually profitable or do they lose money?
5. What are the highest production budget and highest worldwide gross revenue of any film?
6. How much revenue did the lowest and highest budget films make?
"""

print(f"Average Production Budget: ${data['USD_Production_Budget'].mean():,.2f}")
print(f"Average Worldwide Gross Revenue: ${data['USD_Worldwide_Gross'].mean():,.2f}")
print(f"Minimum Worldwide Revenue: ${data['USD_Worldwide_Gross'].min():,.2f}")
print(f"Minimum Domestic Revenue: $ {data['USD_Domestic_Gross'].min():,.2f}")
data["Net_Revenue"] = pd.to_numeric(data['USD_Worldwide_Gross'] - data['USD_Production_Budget'])
bot_20 = data.sort_values('Net_Revenue')[:int(5391 * .25)]
print(f"From the bottom 25%... {len(bot_20[bot_20['Net_Revenue']>=0])} films were profitable.")
print(f"highest production budget: ${data['USD_Production_Budget'].max():,.2f}".title())
print(f"highest worldwide gross revenue: ${data['USD_Worldwide_Gross'].max():,.2f}".title())
print(f"Lowest Budget Film's Revenue: Gross ${data['USD_Worldwide_Gross'].loc[data['USD_Production_Budget'].idxmin()]:,.2f} and Net ${data['Net_Revenue'].loc[data['USD_Production_Budget'].idxmin()]:,.2f}")
print(f"Highest Budget Film's Revenue: Gross ${data['USD_Worldwide_Gross'].loc[data['USD_Production_Budget'].idxmax()]:,.2f} and Net ${data['Net_Revenue'].loc[data['USD_Production_Budget'].idxmax()]:,.2f}")

"""# Investigating the Zero Revenue Films

**Challenge** How many films grossed $0 domestically (i.e., in the United States)? What were the highest budget films that grossed nothing?
"""

print(f"{len(data[data['USD_Domestic_Gross']==0])} films grossed $0 domestically.")
data[data['USD_Domestic_Gross']==0].sort_values('USD_Production_Budget')[:-6:-1]

"""**Challenge**: How many films grossed $0 worldwide? What are the highest budget films that had no revenue internationally?"""

print(f"{len(data[data['USD_Worldwide_Gross']==0])} films grossed $0 worldwide.")
data[data['USD_Worldwide_Gross']==0].sort_values('USD_Production_Budget')[:-6:-1]

"""### Filtering on Multiple Conditions"""

international_releases = data[(data['USD_Domestic_Gross']==0) & (data['USD_Worldwide_Gross']!=0)]
international_releases.head()

"""**Challenge**: Use the [`.query()` function](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) to accomplish the same thing. Create a subset for international releases that had some worldwide gross revenue, but made zero revenue in the United States. 

Hint: This time you'll have to use the `and` keyword.
"""

data.query('USD_Domestic_Gross == 0 and USD_Worldwide_Gross != 0')

"""### Unreleased Films

**Challenge**:
* Identify which films were not released yet as of the time of data collection (May 1st, 2018).
* How many films are included in the dataset that have not yet had a chance to be screened in the box office???
* Create another DataFrame called data_clean that does not include these films. 
"""

# Date of Data Collection
scrape_date = pd.Timestamp('2018-5-1')

films_not_released = data.query('Release_Date >= @scrape_date')
data_clean = data.drop(films_not_released.index)
data_clean

"""### Films that Lost Money

**Challenge**: 
What is the percentage of films where the production costs exceeded the worldwide gross revenue???
"""

print(f"Percent of films that lost money: {len(data_clean[data['Net_Revenue']<0]) / len(data_clean) * 100:.2f}")

"""# Seaborn for Data Viz: Bubble Charts"""

plt.figure(figsize=(8,4), dpi=200)
  
# set styling on a single chart
with sns.axes_style('darkgrid'):
  ax = sns.scatterplot(data=data_clean,
                        x='USD_Production_Budget', 
                        y='USD_Worldwide_Gross',
                        hue='USD_Worldwide_Gross',
                        size='USD_Worldwide_Gross')
  
  ax.set(ylim=(0, 3000000000),
        xlim=(0, 450000000),
        ylabel='Revenue in $ billions',
        xlabel='Budget in $100 millions')

  plt.show()

"""### Plotting Movie Releases over Time

**Challenge**: Try to create the following Bubble Chart:

<img src=https://i.imgur.com/8fUn9T6.png>


"""

plt.figure(figsize=(8,4), dpi=200)

with sns.axes_style('darkgrid'):
  ax2 = sns.scatterplot(data=data_clean,
                        x='Release_Date',
                        y='USD_Production_Budget',
                        hue='USD_Worldwide_Gross',
                        size='USD_Worldwide_Gross')
  
  ax2.set(ylim=(0, 450000000),
          xlim=('01-01-1910', '01-01.2020'),
          ylabel='Budget in $100 millions',
          xlabel='Year')
  
  plt.show()

"""# Converting Years to Decades Trick

**Challenge**: Create a column in `data_clean` that has the decade of the release. 

<img src=https://i.imgur.com/0VEfagw.png width=650> 

Here's how: 
1. Create a [`DatetimeIndex` object](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html) from the Release_Date column. 
2. Grab all the years from the `DatetimeIndex` object using the `.year` property.
<img src=https://i.imgur.com/5m06Ach.png width=650>
3. Use floor division `//` to convert the year data to the decades of the films.
4. Add the decades as a `Decade` column to the `data_clean` DataFrame.
"""

data_clean['Decade'] = pd.DatetimeIndex(data_clean.Release_Date).year // 10 * 10
data_clean

"""### Separate the "old" (before 1969) and "New" (1970s onwards) Films

**Challenge**: Create two new DataFrames: `old_films` and `new_films`
* `old_films` should include all the films before 1969 (up to and including 1969)
* `new_films` should include all the films from 1970 onwards
* How many films were released prior to 1970?
* What was the most expensive film made prior to 1970?
"""

old_films = data_clean[data_clean.Decade < 1970]
new_films = data_clean[data_clean.Decade >= 1970]
print(f"# of films released prior to 1970: {len(old_films)}")
print(f"The most expensive film before 1970 was: {old_films.Movie_Title.loc[old_films.USD_Production_Budget.idxmax()]}")

"""# Seaborn Regression Plots"""

plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
  sns.regplot(data=old_films, 
            x='USD_Production_Budget', 
            y='USD_Worldwide_Gross',
            scatter_kws = {'alpha': 0.4},
            line_kws = {'color': 'black'})

"""**Challenge**: Use Seaborn's `.regplot()` to show the scatter plot and linear regression line against the `new_films`. 
<br>
<br>
Style the chart

* Put the chart on a `'darkgrid'`.
* Set limits on the axes so that they don't show negative values.
* Label the axes on the plot "Revenue in \$ billions" and "Budget in \$ millions".
* Provide HEX colour codes for the plot and the regression line. Make the dots dark blue (#2f4b7c) and the line orange (#ff7c43).

Interpret the chart

* Do our data points for the new films align better or worse with the linear regression than for our older films?
* Roughly how much would a film with a budget of $150 million make according to the regression line?
"""

plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("darkgrid"):
  ax3 = sns.regplot(data=new_films, 
            x='USD_Production_Budget', 
            y='USD_Worldwide_Gross',
            scatter_kws = {'color': '#2f4b7c'},
            line_kws = {'color': '#ff7c43'})
  
  ax3.set(ylim=(0, 3000000000),
          xlim=(0, 450000000),
          ylabel='Revenue in $ billions',
          xlabel='Budget in $ millions')

"""# Run Your Own Regression with scikit-learn

$$ REV \hat ENUE = \theta _0 + \theta _1 BUDGET$$
"""

regression = LinearRegression()
X = pd.DataFrame(new_films, columns=['USD_Production_Budget'])
y = pd. DataFrame(new_films, columns=['USD_Worldwide_Gross'])
regression.fit(X, y)
print(f"Intercept: {regression.intercept_}\nSlope: {regression.coef_}")
print(f"R-squared: {regression.score(X, y)}")

"""**Challenge**: Run a linear regression for the `old_films`. Calculate the intercept, slope and r-squared. How much of the variance in movie revenue does the linear model explain in this case?"""

regression2 = LinearRegression()
X = pd.DataFrame(old_films, columns=['USD_Production_Budget'])
y = pd. DataFrame(old_films, columns=['USD_Worldwide_Gross'])
regression.fit(X, y)
print(f"Intercept: {regression.intercept_}\nSlope: {regression.coef_}")

print(f"R-squared: {regression.score(X, y)}")

"""# Use Your Model to Make a Prediction

We just estimated the slope and intercept! Remember that our Linear Model has the following form:

$$ REV \hat ENUE = \theta _0 + \theta _1 BUDGET$$

**Challenge**:  How much global revenue does our model estimate for a film with a budget of $350 million? 
"""

budget = 350000000
    revenue_estimate = regression.intercept_[0] + regression.coef_[0,0]*budget
    revenue_estimate = round(revenue_estimate, -6)
    print(f'The estimated revenue for a $350 film is around ${revenue_estimate:.10}.')
