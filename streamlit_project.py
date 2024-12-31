import json

import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch, Pitch


st.title("Euros 2024 Shot Map")
st.subheader("Filter to any team/player to see all of their shots taken!")

df = pd.read_csv('euros_2024_shot_map.csv')
df = df[df['type']=='Shot'].reset_index(drop=True)

df['location'] = df['location'].apply(json.loads)                   #using 'json' to load the location as a list object rather than a string object


team = st.selectbox('Select a team',df['team'].sort_values().unique(), index=None)

# Now you want to filter for players within the selected team. 
# index=None so that it doesn't default to any player. 'index=0' will default to the first player on the list
player = st.selectbox('Select a player', df[df['team'] == team]['player'].sort_values().unique(), index=None) 

def filter_data(df, team, player):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]

    return df

filtered_df  = filter_data(df, team, player)


pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10,10))

def plot_shot(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x = float(x['location'][0]),
            y = float(x['location'][1]),
            ax = ax,
            s = 1000*  x['shot_statsbomb_xg'],
            color = 'green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors = 'red' if x['shot_type'] == 'Penalty' else 'black',
            alpha = 1 if x['type'] == 'goal' else .5,
            zorder = 2 if (x['type'] == 'goal' and x['shot_type'] == 'Penalty') else 1                     #layering. we need goals to be on top of non-goals 
        )

plot_shot(filtered_df, ax, pitch)


st.pyplot(fig)