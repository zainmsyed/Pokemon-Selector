import streamlit as st  
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff



df = pd.read_csv('modified.csv')
full_df = pd.read_csv('pokemon.csv')
modified_full_df = full_df.rename(columns={'name': 'Name', 'against_bug': 'Bug','against_dark': 'Dark','against_dragon': 'Dragon','against_electric': 'Electric','against_fairy': 'Fairy', 'against_fight': 'Fight', 'against_fire': 'Fire', 'against_flying': 'Flying', 'against_ghost': 'Ghost','against_grass': 'Grass', 'against_ground': 'Ground','against_ice': 'Ice','against_normal': 'Normal','against_poison': 'Poison','against_psychic': 'Psychic','against_rock': 'Rock', 'against_steel': 'Steel','against_water': 'Water'})
only_against = modified_full_df[['Name','Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fight', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']]

st.set_page_config(layout='wide')


#### MAIN PAGE TITLE####

st.title('Pokemon Analyzer')

st.markdown('''
###### Pokemon dataset was obtained from [kaggle](https://www.kaggle.com/rounakbanik/pokemon)
###### This dashboard was created using [pandas](https://pandas.pydata.org/), [plotly](https://plotly.com/), and [streamlit](https://streamlit.io/)
---
''')

st.header('Select Your Pokemon:')


name_pokemon = st.multiselect(
    label='',
    options=df['Name'],
    default=('Bulbasaur', 'Charmander', 'Squirtle')
)

#### 1st Bar Graph ####

name_df = df[df['Name'].isin(name_pokemon)]


fig_go = go.Figure()
fig_go.add_trace(go.Bar(
    x=name_df['Name'],
    y=name_df['HP'],
    name='HP'
))   
fig_go.add_trace(go.Bar(
    x=name_df['Name'],
    y=name_df['Attack'],
    name='Attack'
))   

fig_go.add_trace(go.Bar(
    x=name_df['Name'],
    y=name_df['Defense'],
    name='Defense'
))   

fig_go.add_trace(go.Bar(
    x=name_df['Name'],
    y=name_df['Speed'],
    name='Speed'
))   

fig_go.add_trace(go.Bar(
    x=name_df['Name'],
    y=name_df['Sp. Atk'],
    name='Sp. Atk'
))   

fig_go.add_trace(go.Bar(
    x=name_df['Name'],
    y=name_df['Sp. Def'],
    name='Sp. Def'
))   


fig_go.update_layout(
    title='Base Stats of Pokemon by Name',
    xaxis_title='Name',
    yaxis_title='Value',
    legend_title='Stats'
)

fig_name_df = ff.create_table(name_df)

with st.expander('Click to See Table of Selected Pokemon'):
    st.plotly_chart(fig_name_df, use_container_width=True)



#### Transposed Bar graph ####

namegroup_name_df = name_df.groupby('Name').mean()
m_namegroup_name_df = namegroup_name_df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']]
transposed_namegroup = m_namegroup_name_df.T

fig_xy_flip = px.bar(transposed_namegroup, title='Base Stats of Pokemon by Stats', barmode='group')
fig_xy_flip.update_xaxes(title_text='Stats')
fig_xy_flip.update_yaxes(title_text='Value')


##### Weak Against #####

against_name_df = only_against[only_against['Name'].isin(name_pokemon)].groupby('Name').mean()

def df_heat(against_name_df):
    return {'z': against_name_df.values.tolist(),
            'x': against_name_df.columns.tolist(),
            'y': against_name_df.index.tolist()}

fig_heat = go.Figure(data=go.Heatmap(df_heat(against_name_df), colorscale='picnic'))
fig_heat.update_layout(
    title='Pokemon Weakness by Type: (Number = Damage Multiplier Taken by Pokemon)',
    xaxis_title='Pokemon Type',
    yaxis_title='Name'
)


#### LAYOUT ####

r1col1, r1col2 = st.columns(2)
r2col1, r2col2, r2col3 = st.columns([1,2,1])
r3col1, r3col2 = st.columns([3,1])
r4col1, r4col2 = st.columns(2)
with r1col1:
    st.plotly_chart(fig_go, use_container_width=True) 

with r1col2:
    st.plotly_chart(fig_xy_flip, use_container_width=True) 

with r2col2:
    st.plotly_chart(fig_heat, use_container_width=True)

with r3col1:
    st.header('Find Pokemon by Type')

with r4col1:
    type1_filter = st.multiselect(
        'Fiter by Pokemon Type 1',
        options=df['Type 1'].unique(),
        default=('Dragon')
    )

type1_filter_name = df[df['Type 1'].isin(type1_filter)]

with r4col2:
    type2_filter = st.multiselect(
        'Fiter by Pokemon Type 2',
        options=type1_filter_name['Type 2'].unique(),
        default=('Flying')
    )

type1_filter_name = df[df['Type 1'].isin(type1_filter)]
type2_filter_name = df[df['Type 2'].isin(type2_filter)]
combined_type_filter_name = df[(df['Type 1'].isin(type1_filter)) & (df['Type 2'].isin(type2_filter))] 


fig_type_filter_name = ff.create_table(combined_type_filter_name)

st.plotly_chart(fig_type_filter_name, use_container_width=True) 
