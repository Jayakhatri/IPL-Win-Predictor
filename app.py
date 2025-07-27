import streamlit as st
import pickle
import pandas as pd

teams = [
    'Chennai Super Kings',
    'Delhi Capitals',
    'Gujarat Titans',
    'Kolkata Knight Riders',
    'Lucknow Super Giants',
    'Mumbai Indians',
    'Punjab Kings',
    'Rajasthan Royals',
    'Royal Challengers Bangaluru',
    'Sunrisers Hyderabad'
]
cities = ['Chandigarh', 'Delhi', 'Jaipur', 'Chennai', 'Kolkata', 'Mumbai',
       'Cape Town', 'Durban', 'Port Elizabeth', 'Centurion',
       'East London', 'Johannesburg', 'Kimberley', 'Bloemfontein',
       'Ahmedabad', 'Dharamsala', 'Pune', 'Bangalore', 'Hyderabad',
       'Raipur', 'Abu Dhabi', 'Ranchi', 'Cuttack',
       'Visakhapatnam', 'Indore', 'Dubai', 'Sharjah', 'Navi Mumbai',
       'Lucknow', 'Guwahati', 'Mohali', 'New Chandigarh']
pipe = pickle.load(open('pipe.pkl','rb'))
st.title('IPL Win Predictor')
col1,col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Batting team',['Select Team'] + sorted(teams))
with col2:
    bowling_team = st.selectbox('Bowling team',['Select Team'] + sorted(teams))

selected_city = st.selectbox('Host city',['Select City'] + sorted(cities))

target = st.number_input('Target')

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Score')
with col4:
    overs = st.number_input('Overs completed')
with col5:
    wickets = st.number_input('Wickets out')

if st.button('Predict Probability'):
    runs_left = target-score
    balls_left = 120-(overs*6)
    wickets = 10-wickets
    crr = score/overs
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],
                             'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets_left':[wickets],
                             'total_score_inn1':[target],'crr':[crr],'rrr':[rrr]})
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "- " + str(round(win*100)) + "%")
    st.header(bowling_team + "- " + str(round(loss*100)) + "%")
