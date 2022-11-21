import streamlit as st
import os
import requests
import streamlit as st
from streamlit_option_menu import option_menu


#1. as sidebar menu
with st.sidebar:

    selected =option_menu(
        menu_title=0,
        options=["Home","My Team","Battle"],
        icons=["house","dribbble","trophy"],
        menu_icon="cast",
        default_index=0,

    )

if selected == "Home":

    def add_bg_from_url():
        '''Add background image with a link'''
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("https://media.tenor.com/8Q3Y3scvPDsAAAAC/qatar-world-cup.gif");
                background-position: center;
                background-size:contain ;
                background-repeat: no-repeat;
            }}
             </style>
             """,
            unsafe_allow_html=True
         )
    add_bg_from_url()


if selected == "My Team":
    def add_bg_from_url():
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("https://image.nhandan.vn/w800/Files/Images/2022/04/02/fpnfy6ixmae0udd_1648772051411212-1648834231578.jpg");
                background-attachment: fixed;
                background-size: cover

            }}
             </style>
             """,
            unsafe_allow_html=True
         )
    add_bg_from_url()

    st.title(f"Welcome To Prediction World Cup 2022 Results of a choosen team")

    pick_team = st.selectbox(
    "Choose Any team you want",
    ('Qatar', 'Germany', 'Denmark', 'Brazil', 'France', 'Belgium', 'Croatia', 'Spain', 'Serbia', 'England', 'Switzerland', 'Netherlands', 'Argentina', 'Iran', 'Korea Republic', 'Japan', 'Saudi Arabia', 'Ecuador', 'Uruguay', 'Canada', 'Ghana', 'Senegal', 'Portugal', 'Poland', 'Tunisia', 'Morocco', 'Cameroon', 'USA', 'Mexico', 'Wales', 'Australia', 'Costa Rica')
    )

    params = dict(
    pick_team=pick_team)

    #TODO
    #put api link
    #football_api_url = ''
    #response = requests.get(football_api_url, params=params)

    #prediction = response.json()

    #TODO
    #To put appropriate prediction like results and where eliminated
    #pred = prediction['results']

    ok = st.button("Results")
    #if ok:
        #results = pred
    #st.subheader(f'results{pred}')

# Nice to have as we talked, battle between two teams only, predict the winner
if selected == "Battle":
    def add_bg_from_url():
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("https://www.aljazeera.com/wp-content/uploads/2022/09/SOR06738.jpg?resize=770%2C513");
                background-attachment: fixed;
                background-size: cover

            }}
             </style>
             """,
            unsafe_allow_html=True
         )
    add_bg_from_url()
    st.title(f"Welcome To the One vs One Showdown")

    Team_1 = st.selectbox(
    "TEAM 1",
    ('Qatar', 'Germany', 'Denmark', 'Brazil', 'France', 'Belgium', 'Croatia', 'Spain', 'Serbia', 'England', 'Switzerland', 'Netherlands', 'Argentina', 'Iran', 'Korea Republic', 'Japan', 'Saudi Arabia', 'Ecuador', 'Uruguay', 'Canada', 'Ghana', 'Senegal', 'Portugal', 'Poland', 'Tunisia', 'Morocco', 'Cameroon', 'USA', 'Mexico', 'Wales', 'Australia', 'Costa Rica')
    )
    Team_2 = st.selectbox(
    "TEAM 2",
    ('Qatar', 'Germany', 'Denmark', 'Brazil', 'France', 'Belgium', 'Croatia', 'Spain', 'Serbia', 'England', 'Switzerland', 'Netherlands', 'Argentina', 'Iran', 'Korea Republic', 'Japan', 'Saudi Arabia', 'Ecuador', 'Uruguay', 'Canada', 'Ghana', 'Senegal', 'Portugal', 'Poland', 'Tunisia', 'Morocco', 'Cameroon', 'USA', 'Mexico', 'Wales', 'Australia', 'Costa Rica')
    )
    win = st.button("Winner")

    #TODO
    #To put appropriate prediction like probality of win, change to conviance value
    #prob = prediction['probability']


    #if win:

        #winning_team = prob
        #if prob Team_1 > Team_2 :
            #print(f"(Team_1} is the Winner"")
        #elif prob Team_1 < Team_2 :
            #print(f"{Team_2} is the winner")
    #st.subheader(f'Winner is {pred}')
