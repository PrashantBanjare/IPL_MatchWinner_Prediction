import pickle
from pathlib import Path
from PIL import Image
import pandas as pd
import streamlit as st


logo = Image.open("IPL LOGO/image.png")

st.set_page_config(
    page_title="IPL Match Winner Prediction",
    page_icon=logo,
    layout="wide"
)


col1, col2 = st.columns([1, 4])

with col1:
    st.image(logo, width=100)

with col2:
    st.markdown("<h1 style='margin-top:0;margin-bottom:0;'>🏏IPL Match Winner Prediction</h1>", unsafe_allow_html=True)

st.markdown("Enter the live match situation and predict the chasing team's winning probability.")
# File paths

MODEL_PATH = Path("model.pkl")
DATA_PATH = Path("final_df.csv")


# Load model
@st.cache_resource
def load_model(path: Path):
    with open(path, "rb") as f:
        return pickle.load(f)


# Load data

@st.cache_data
def load_data(path: Path):
    return pd.read_csv(path)


# Build model input
def build_input_dataframe(
    batting_team: str,
    bowling_team: str,
    city: str,
    target: int,
    current_score: int,
    balls_bowled: int,
    runs_left: int,
    balls_left: int,
    wickets_left: int,
    crr: float,
    rrr: float
) -> pd.DataFrame:
    """
    Build input exactly according to model training columns:
    match_id, ball, city, batting_team, target, bowling_team,
    current_score, runs_left, balls_left, wickets_left, crr, rrr
    """

    input_data = {
        "match_id": [0],                 
        "ball": [balls_bowled],          
        "city": [city],
        "batting_team": [batting_team],
        "target": [target],
        "bowling_team": [bowling_team],
        "current_score": [current_score],
        "runs_left": [runs_left],
        "balls_left": [balls_left],
        "wickets_left": [wickets_left],
        "crr": [round(crr, 2)],
        "rrr": [round(rrr, 2)],
    }

    return pd.DataFrame(input_data)


# Check required files
if not MODEL_PATH.exists():
    st.error("model.pkl not found in the current folder.")
    st.stop()

if not DATA_PATH.exists():
    st.error("final_df.csv not found in the current folder.")
    st.stop()


pipe = load_model(MODEL_PATH)
df = load_data(DATA_PATH)



# Dropdown values
required_cols = ["batting_team", "bowling_team", "city"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"Column '{col}' not found in final_df.csv")
        st.stop()

batting_teams = sorted(df["batting_team"].dropna().unique().tolist())
bowling_teams = sorted(df["bowling_team"].dropna().unique().tolist())
cities = sorted(df["city"].dropna().unique().tolist())



# Inputs
col1, col2, col3 = st.columns(3)

with col1:
    batting_team = st.selectbox("Batting Team (Chasing Team)", batting_teams)
    bowling_team = st.selectbox("Bowling Team", bowling_teams)
    city = st.selectbox("City", cities)

with col2:
    target = st.number_input("Target", min_value=1, max_value=300, value=180, step=1)
    current_score = st.number_input("Current Score", min_value=0, max_value=300, value=100, step=1)
    wickets_out = st.number_input("Wickets Out", min_value=0, max_value=10, value=3, step=1)

with col3:
    overs_completed = st.number_input("Overs Completed", min_value=0.0, max_value=20.0, value=12.0, step=0.1)
    balls_in_current_over = st.number_input(
        "Balls Bowled in Current Over (0 to 5)",
        min_value=0,
        max_value=5,
        value=0,
        step=1
    )



# Derived values
whole_overs = int(overs_completed)
balls_bowled = whole_overs * 6 + balls_in_current_over

if balls_bowled > 120:
    balls_bowled = 120

balls_left = 120 - balls_bowled
runs_left = target - current_score
wickets_left = 10 - wickets_out

crr = (current_score / balls_bowled) * 6 if balls_bowled > 0 else 0.0
rrr = (runs_left / balls_left) * 6 if balls_left > 0 else 0.0


# Show match situation

st.subheader("Live Match Situation")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Runs Left", max(runs_left, 0))
m2.metric("Balls Left", max(balls_left, 0))
m3.metric("Wickets Left", max(wickets_left, 0))
m4.metric("CRR", round(crr, 2))
m5.metric("RRR", round(rrr, 2))


# Prediction

if st.button("Predict Winning Probability", use_container_width=True):
    if batting_team == bowling_team:
        st.warning("Batting team and bowling team cannot be the same.")
        st.stop()

    if current_score > target:
        st.warning("Current score cannot be greater than target.")
        st.stop()

    if wickets_out >= 10 and runs_left > 0:
        st.warning("All wickets are down. The chasing team has already lost.")
        st.stop()

    if balls_left <= 0 and runs_left > 0:
        st.warning("No balls left. The chasing team has already lost.")
        st.stop()

    try:
        input_df = build_input_dataframe(
            batting_team=batting_team,
            bowling_team=bowling_team,
            city=city,
            target=target,
            current_score=current_score,
            balls_bowled=balls_bowled,
            runs_left=max(runs_left, 0),
            balls_left=max(balls_left, 0),
            wickets_left=max(wickets_left, 0),
            crr=crr,
            rrr=rrr
        )

        probs = pipe.predict_proba(input_df)[0]
        lose_prob = round(probs[0] * 100, 2)
        win_prob = round(probs[1] * 100, 2)

        st.subheader("Prediction Result")

        c1, c2 = st.columns(2)
        with c1:
            st.success(f"**{batting_team} Win Probability:** {win_prob}%")
        with c2:
            st.error(f"**{bowling_team} Win Probability:** {lose_prob}%")

        if win_prob > lose_prob:
            st.info(f"Predicted Winner: **{batting_team}**")
        elif lose_prob > win_prob:
            st.info(f"Predicted Winner: **{bowling_team}**")
        else:
            st.info("This match is extremely close.")

        st.write("### Model Input Used")
        st.dataframe(input_df, use_container_width=True)

    except Exception as e:
        st.error(f"Prediction failed: {e}")