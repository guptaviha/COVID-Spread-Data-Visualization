
import pandas
import plotly.express as px
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from IPython.display import HTML
import numpy as np

"""### Index"""

index = pandas.read_csv("https://storage.googleapis.com/covid19-open-data/v3/index.csv")

index = index[['location_key', 'country_code', 'country_name', 'subregion1_code', 'subregion1_name', 'subregion2_code'
, 'subregion2_name', 'locality_code', 'locality_name', 'aggregation_level', 'iso_3166_1_alpha_2', 'iso_3166_1_alpha_3']]

index = index.convert_dtypes()

US_index = index[index['country_code'] == 'US']

US_index_list = US_index['location_key'].to_list()

"""### Demographics"""

demo = pandas.read_csv("https://storage.googleapis.com/covid19-open-data/v3/demographics.csv")

demo = demo.convert_dtypes()

US_demo = demo[demo['location_key'].isin(US_index_list)]

"""### Data"""

US_data = pandas.read_csv("https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv")

US_data = US_data.convert_dtypes()

US_data = US_data[US_data['location_key'].isin(US_index_list)]

US_data_merge = pandas.merge(US_data, US_demo, how='inner', on = 'location_key')

US_data_merge = pandas.merge(US_data_merge, US_index, how='inner', on = 'location_key')

"""### Plot"""

US_data_merge_sub = US_data_merge[['date', 'subregion1_code', 'cumulative_confirmed']]

US_data_merge_sub = US_data_merge_sub.dropna()

US_data_merge_sub['cumulative_confirmed'] = US_data_merge_sub['cumulative_confirmed'].astype('int')

US_data_merge_sub = US_data_merge_sub.astype({'cumulative_confirmed':'int'})

US_data_merge_wide = US_data_merge_sub.pivot_table(index='date', columns='subregion1_code', values='cumulative_confirmed')

US_data_merge_wide

US_data_merge_wide = US_data_merge_wide.fillna(0)

US_data_merge_wide = US_data_merge_wide.drop(['2022-12-30'])

n = 120

df_daily = US_data_merge_wide.iloc[0:n:1]

df_weekly = US_data_merge_wide.iloc[n::7]

df = pandas.concat([df_daily, df_weekly])

def nice_axes(ax):
    ax.set_facecolor('.8')
    ax.tick_params(labelsize=8, length=0)
    ax.grid(True, axis='x', color='white')
    ax.set_axisbelow(True)
    ax.set_xlabel('Confirmed Cases')
    ax.set_ylabel('States by Rank')
    [spine.set_visible(False) for spine in ax.spines.values()]

def prepare_data(df):
    df = df.reset_index()
    df.index = df.index * steps
    last_idx = df.index[-1] + 1
    df_expanded = df.reindex(range(last_idx))
    df_expanded['date'] = df_expanded['date'].fillna(method='ffill')
    df_expanded = df_expanded.set_index('date')
    df_rank_expanded = df_expanded.rank(axis=1, method='first')
    df_expanded = df_expanded.interpolate()
    df_rank_expanded = df_rank_expanded.interpolate()
    return df_expanded, df_rank_expanded

def init():
    ax.clear()
    nice_axes(ax)
    ax.set_ylim(.2, 6.8)

def update(i):
    for bar in ax.containers:
        bar.remove()
    y = df_rank_expanded.iloc[i]
    width = df_expanded.iloc[i]
    ax.barh(y=y, width=width, color=colors, tick_label=labels)
    date_str = df_expanded.index[i]
    if i < n * steps:
      freq = "Daily"
    else:
      freq = "Speed Up: Weekly"
    ax.set_title(f'Confirmed COVID-19 Cases by US States \n{date_str}\n{freq}', fontsize='smaller')

colors = plt.cm.Paired(range(12))
steps = 3
df_expanded, df_rank_expanded = prepare_data(df)
labels = df_expanded.columns
fig = plt.Figure(figsize=(4, 8), dpi=144)
ax = fig.add_subplot()
anim = FuncAnimation(fig=fig, func=update, init_func=init, frames=len(df_expanded), 
                     interval=100, repeat=False)
# fig, (ax1, ax2) = plt.subplots(2)
# fig.suptitle('Vertically stacked subplots')
# ax1.plot(x, y)
# ax2.plot(x, -y)

html = anim.to_html5_video()
HTML(html)