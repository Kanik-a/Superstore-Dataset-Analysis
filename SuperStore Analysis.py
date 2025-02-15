# IMPORTING REQUIRED LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# LOADING DATA 
df = pd.read_csv(r"C:\Users\kanik\OneDrive\Desktop\Superstore.csv", sep=";", encoding='mac_roman', on_bad_lines='skip')

# EXPLORATORY DATA ANALYSIS
# Getting information about the datafram columns, rows etc.
datafram_info = df.info()
print(datafram_info)

# Running description of dataframe
df_describe = df.describe()
print(df_describe)

# Checking if there is any missing data.
missing_values = df.isnull 
print(missing_values)

# Boxplot of numerical data
Sales = go.Box(x=df['Sales'],name='Sales')
Quantity = go.Box(x=df['Quantity'],name='Quantity')
Discount = go.Box(x=df['Discount'],name='Discount')
Profit = go.Box(x=df['Profit'],name='Profit')
fig = make_subplots(rows=4, cols=2)
fig.append_trace(Sales, row = 1, col = 1)
fig.append_trace(Quantity, row = 1, col = 2)
fig.append_trace(Discount, row = 2, col = 1)
fig.append_trace(Profit, row = 2, col = 2)
fig.update_layout(
    title_text = 'Distribution of numerical data',
    title_font_size = 24,
    title_x=0.45)
fig.show()

# Sorting Profit and Quantity values from lowest to highest
sort_values = ['Profit', 'Quantity']
for k in sort_values:
    df_sort = df.sort_values(by = k).head() 
    print(df_sort)
sort_values = ['Profit', 'Quantity', 'Region']
for j in sort_values:
    df_correlation = df.sort_values(by=j, ascending = False)
    print(df_correlation)

dominant_prodcut = df.groupby("Sub-Category")["Product ID"].count().drop_duplicates(keep='last')
print(sorted(dominant_prodcut))

# DATA CLEANING
def remove_columns(df):
    remove_columns = ['Order ID', 'Customer Name', 'Postal Code', 'Customer ID', 'Country', 'Ship Date']
    for item in remove_columns:
        df = df.drop(columns = item)
    print(df)

remove_columns(df)


# AREA 1: GEOSPATIAL ANALYSIS

# FIGURING OUT TOTAL PROFITS IN EACH REGION
regions = ['South', 'Central', 'East', 'West']
total_profit = []
for k in regions:
    df_new = df[df['Region'].isin([k])]
    total = df_new['Profit'].sum()
    total_profit.append(total)
data1 = [('South', 46749.4303),('Central', 39706.3625),('East', 91522.7800),('West', 108418.4489)]
profit_comparison = pd.DataFrame(data1, columns=['Region','Total_Profit'])
profit_comparison = profit_comparison.set_index('Region')
print(profit_comparison)
profit_comparison.plot(kind = 'bar', color='b')
plt.title("Profit Comparision in different Regions (in USD)")
plt.show()

# FIGURING OUT MOST PROFITABLE STATES
min_states = []
max_states = []
for k in regions:
    state_df = df[df['Region'].isin([k])]
    state_total = state_df.groupby('State')['Profit'].sum()
    minimum = min(state_total)
    min_states.append(minimum)
    maximum = max(state_total)
    max_states.append(maximum)
min_loc = ['North Carolina', 'Texas', 'Ohio', 'Colorado']
max_loc = ['Virginia', 'Michigan', 'New York', 'California']

print(min_states)
print(max_states)
min_profit = dict(zip(min_loc,min_states))
min_profit_df = pd.DataFrame.from_dict(min_profit, orient='index')
min_profit_df.plot(kind = 'bar', figsize=(10,5))
plt.title("Minimum Profit in each State (in USD)")
plt.show()
max_profit = dict(zip(max_loc,max_states))
max_profit_df = pd.DataFrame.from_dict(max_profit, orient='index')
max_profit_df.plot(kind = 'bar')
plt.title("Maximum Profit in each State (in USD)")
plt.legend()
plt.show()


def state_sales(df):
#Combining the data through States and sorting it based on the Sales the states are making
    combined_state_sales = df.groupby("State", as_index=False).sum().sort_values(by="Sales", ascending=False)
    combined_state_sales["profit_margin"] = combined_state_sales["Profit"] / combined_state_sales["Sales"]


    fig, ax = plt.subplots(figsize=(10,10))

    sns.barplot(x=combined_state_sales["Sales"][:10], y=combined_state_sales["State"][:10],
           ax=ax, palette="light:b")

    for p in ax.patches:
        _, y = p.get_xy()
    
        ax.annotate(f"${p.get_width() / 1000 :.1f}K", xy=(p.get_width(), y+0.45))
    
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.set(ylabel=None, xlabel=None)
    ax.tick_params(labelbottom=None, bottom=None)

    ax.set_title("Highest Revenue - Top 10 States", fontdict={"fontsize":14})
    plt.show()

state_sales(df)

# AREA 2: CUSTOMER SEGMENT ANALYSIS
segments = ['Consumer', 'Corporate', 'Home Office']
df_features4 = ['Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Customer Name','Ship Mode', 'Postal Code', 'Product ID', 'Country', 'State', 'Customer ID', 'Customer', 'City', 'Category', 'Sub-Category', 'Product Name', 'Sales', 'Quantity', 'Discount']

for j in segments:
    df4 = df[df['Segment'].isin([j])]
    for i in df_features4:
        if i in df4:
            df4 = df4.drop(i, axis = 1)
    segment_total = df4.groupby('Segment')['Profit'].sum()
    for item in segment_total:
        print(item)
data2 = [['Consumer', 134119], ['Corporate', 91979], ['Home Office', 60298]]
df5 = pd.DataFrame(data2, columns=['Segment', 'Profit'])
df5 = df5.set_index('Segment')
print(df5)
df5.plot(kind = 'bar')
plt.show()

def segment_category(df):
    segment_and_category = df.groupby(["Segment", "Category"], as_index=False).sum()

    fig3, ax3 = plt.subplots(figsize=(6,6))
    sns.barplot(x=segment_and_category["Segment"], y=segment_and_category["Sales"], hue=segment_and_category["Category"], ax=ax3)

    ax3.spines[["top", "right"]].set_visible(False)
    ax3.set_title("Revenue by Category per Segment", fontdict={"fontsize":15}, loc="left")
    ax3.set(xlabel=None, ylabel=None)

    ax3.yaxis.set_major_formatter("${x:,.0f}")

    ax3.legend(title="Categories", loc="center right", bbox_to_anchor=(1, 0.85))

    plt.show()

segment_category(df)

# AREA 3: CATEGORY ANALYSIS

# Grouping the data based on category
sales_per_category = df.groupby("Category").sum()

# Getting a list of colors. This will help other charts use the same colors given the label texts.
category_colors = ["tab:red" if label == "Furniture" else "tab:blue" if label == "Office Supplies" else "tab:green" for label in sales_per_category.index]
    
# Creating the first pie chart of sales per category
fig, ax1 = plt.subplots(figsize=(8, 8))

ax1.pie(sales_per_category["Sales"], labels=sales_per_category.index,
      autopct=lambda p:f"{p:.1f}% \n ${p*np.sum(sales_per_category['Sales'])/100 :,.0f}",
      wedgeprops={"linewidth": 1, "edgecolor":"blue", "alpha":0.55},
      colors=category_colors, explode=[0.05, 0, 0])

# Setting the title
ax1.set_title("Share of Total Revenue by Category", loc="left", fontdict={"fontsize":14})
plt.show()
# Grouping the data based on category
sales_per_category = df.groupby("Category").sum()

# Getting a list of colors. This will help other charts use the same colors given the label texts.
category_colors = ["tab:red" if label == "Furniture" else "tab:blue" if label == "Office Supplies" else "tab:green" for label in sales_per_category.index]
    
# Creating the second pie chart of profit per category
fig, ax2 = plt.subplots(figsize=(8, 8))

ax2.pie(sales_per_category["Profit"], labels=sales_per_category.index,
       autopct=lambda p: f"{p:.1f}% \n ${p*np.sum(sales_per_category['Profit'])/100 :,.0f}",
        startangle=45, wedgeprops={"linewidth": 1, "edgecolor":"blue", "alpha":0.55},
        colors=category_colors, explode=[0.15, 0, 0])

# Setting the title
ax2.set_title("Share of Total Profit by Category",loc="left", fontdict={"fontsize":14})
plt.show()
