!pip install seaborn --quiet

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


movies_df = pd.read_csv('/content/movie_data.csv', delimiter=';', quotechar='"')
financials_df = pd.read_csv('/content/financial_data.csv', delimiter=';', quotechar='"')


df = pd.merge(movies_df, financials_df, on='movie_id')


df['profit'] = df['revenue'] - df['budget']
df['profit_margin'] = (df['profit'] / df['revenue']) * 100


df['category'] = pd.cut(df['revenue'],
                        bins=[0, 50000000, 100000000, float('inf')],
                        labels=['Flop', 'Average', 'Hit'])


fig1, axs1 = plt.subplots(3, 2, figsize=(14, 12))


top5_revenue = df.nlargest(5, 'revenue')
sns.barplot(x='revenue', y='title', data=top5_revenue, ax=axs1[0,0], color='skyblue')
axs1[0,0].set_title('Top 5 Movies by Revenue')

df['category'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=axs1[0,1])
axs1[0,1].set_ylabel('')
axs1[0,1].set_title('Movie Performance Distribution')

top5_profit = df.nlargest(5, 'profit')
sns.barplot(x='profit', y='title', data=top5_profit, ax=axs1[1,0], color='orange')
axs1[1,0].set_title('Top 5 Most Profitable Movies')


industry_margin = df.groupby('industry')['profit_margin'].mean().sort_values()
industry_margin.plot(kind='bar', ax=axs1[1,1], color='green')
axs1[1,1].set_title('Average Profit Margin by Industry')
axs1[1,1].set_ylabel('Profit Margin (%)')


year_revenue = df.groupby('year')['revenue'].sum()
year_revenue.plot(kind='line', marker='o', ax=axs1[2,0], color='purple')
axs1[2,0].set_title('Year-wise Total Revenue')
axs1[2,0].set_ylabel('Revenue')

sns.scatterplot(x='budget', y='profit', hue='industry', data=df, ax=axs1[2,1])
axs1[2,1].set_title('Profit vs Budget by Industry')

plt.tight_layout()
plt.show()


fig2, axs2 = plt.subplots(3, 2, figsize=(14, 12))


df['industry'].value_counts().plot(kind='bar', ax=axs2[0,0], color='teal')
axs2[0,0].set_title('Number of Movies by Industry')

avg_data = df.groupby('industry')[['budget','revenue']].mean()
avg_data.plot(kind='bar', ax=axs2[0,1])
axs2[0,1].set_title('Avg Budget vs Revenue by Industry')
axs2[0,1].set_ylabel('Amount')

movies_per_year = df['year'].value_counts().sort_index()
movies_per_year.plot(kind='bar', ax=axs2[1,0], color='salmon')
axs2[1,0].set_title('Movies Released Per Year')
axs2[1,0].set_ylabel('Number of Movies')


top5_directors = df.groupby('director')['revenue'].sum().nlargest(5)
top5_directors.plot(kind='barh', ax=axs2[1,1], color='purple')
axs2[1,1].set_title('Top 5 Directors by Revenue')
axs2[1,1].set_xlabel('Total Revenue')


df['currency'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=axs2[2,0])
axs2[2,0].set_ylabel('')
axs2[2,0].set_title('Currency Distribution')


fig2.delaxes(axs2[2,1])

plt.tight_layout()
plt.show()
