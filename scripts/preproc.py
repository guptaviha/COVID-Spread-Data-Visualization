
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

# n = 120

# df_daily = US_data_merge_wide.iloc[0:n:1]

# df_weekly = US_data_merge_wide.iloc[n::7]

# df = pandas.concat([df_daily, df_weekly])

US_data_merge_wide.to_csv('/static/cases_by_state.csv')  

# n = 20
# df = US_data_merge_wide.iloc[0:30:1]
# df.to_csv('cases_by_state_test.csv')  