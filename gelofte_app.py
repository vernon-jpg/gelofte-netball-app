
import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import Optional, List

st.set_page_config(
    page_title="Gelofte 1st Netball Season Tracker",
    page_icon="🏐",
    layout="wide"
)

@dataclass
class QuarterScore:
    q1_for: Optional[int] = None
    q1_against: Optional[int] = None
    q2_for: Optional[int] = None
    q2_against: Optional[int] = None
    q3_for: Optional[int] = None
    q3_against: Optional[int] = None
    q4_for: Optional[int] = None
    q4_against: Optional[int] = None

@dataclass
class Match:
    date: str
    opponent: str
    competition: str
    goals_for: int
    goals_against: int
    quarters: Optional[QuarterScore] = None
    notes: str = ""

    def gd(self) -> int:
        return self.goals_for - self.goals_against

    def result(self) -> str:
        if self.goals_for > self.goals_against:
            return "W"
        if self.goals_for < self.goals_against:
            return "L"
        return "D"

matches: List[Match] = [
    Match("2026-02-21", "Unknown", "Night Series", 43, 0, notes="Score remembered from parent group"),
    Match("2026-02-27", "Curro Salt Rock", "Night Series", 20, 25),
    Match("2026-03-??", "Kloof High", "Night Series", 1, 0, notes="Placeholder: won by 1"),
    Match("2026-03-??", "DHS Girls", "Night Series", 1, 0, notes="Placeholder: won by 1"),
    Match("2026-03-10", "Danville", "Friendly", 0, 30, notes="Placeholder: lost by 30"),
    Match("2026-03-24", "Suid-Natal", "League", 31, 34, QuarterScore(6, 9, 10, 8, 8, 7, 7, 10)),
    Match("2026-03-31", "Aliwal Noord", "Tour Tournament", 24, 18, QuarterScore(9, 4, 5, 5, 4, 4, 6, 5)),
    Match("2026-04-01", "Bastion", "Tour Tournament", 21, 12, QuarterScore(6, 3, 3, 2, 5, 3, 7, 4)),
    Match("2026-04-01", "Carletonville", "Tour Tournament", 32, 13, QuarterScore(6, 5, 6, 2, 11, 2, 9, 4)),
    Match("2026-04-01", "Tuine", "Tour Tournament", 30, 14, QuarterScore(5, 4, 5, 4, 9, 3, 11, 3)),
    Match("2026-04-02", "Curro Waterfall", "Tour Tournament", 33, 4, QuarterScore(7, 1, 5, 2, 10, 1, 11, 0)),
    Match("2026-04-02", "Wolmaransstad", "Tour Tournament", 22, 26, QuarterScore(6, 4, 9, 4, 6, 8, 1, 10)),
    Match("2026-04-02", "Pionier", "Tour Tournament", 26, 21, QuarterScore(7, 5, 8, 4, 7, 8, 4, 4)),
    Match("2026-04-11", "Toti High", "League", 48, 12),
    Match("2026-04-14", "Curro Hillcrest", "League", 22, 25, QuarterScore(5, 10, 7, 5, 5, 6, 5, 4)),
    Match("2026-04-18", "Kingsway", "League", 42, 7, QuarterScore(10, 2, 7, 1, 9, 3, 16, 1)),
    Match("2026-04-21", "Curro Salt Rock", "League", 29, 16, QuarterScore(11, 2, 4, 7, 4, 3, 10, 4)),
    Match("2026-04-28", "Luthayi", "League", 23, 35, QuarterScore(4, 10, 4, 11, 6, 6, 9, 8)),
    Match("2026-05-05", "Kloof High", "League", 24, 25, QuarterScore(6, 6, 7, 4, 7, 6, 4, 9)),
]

player_counts = {
    "Nika": 54,
    "Yahne": 54,
    "Zanike": 54,
    "Sune": 54,
    "Anel": 114,
    "Mikhaela": 84,
    "Verenique": 51,
    "Nadia": None,
    "Kari": None,
}

pom_counts = {
    "Zanike": 1,
    "Anel": 1,
    "Sune": 1,
    "Nika": 1,
    "Nadia": 1,
}

upcoming_fixtures = pd.DataFrame([
    {"Date": "2026-05-12", "Opponent/Event": "Westville Girls High School", "Venue": "Away", "Prediction": "Westville 28-24 Gelofte"},
    {"Date": "2026-05-16", "Opponent/Event": "Sportdag Port Natal", "Venue": "Away", "Prediction": "Positive record expected"},
    {"Date": "2026-05-19", "Opponent/Event": "Kuswag", "Venue": "Away", "Prediction": "Gelofte by 8-12"},
    {"Date": "2026-05-23", "Opponent/Event": "Sportdag Port Natal - 1stes only", "Venue": "Away", "Prediction": "Depends on opponents"},
    {"Date": "2026-05-26", "Opponent/Event": "St Mary’s", "Venue": "Home", "Prediction": "Very tight"},
    {"Date": "2026-05-27", "Opponent/Event": "Thomas More College", "Venue": "Away", "Prediction": "Gelofte by 6-10"},
])

def matches_to_df(match_list: List[Match]) -> pd.DataFrame:
    rows = []
    for match in match_list:
        rows.append({
            "Date": match.date,
            "Opponent": match.opponent,
            "Competition": match.competition,
            "GF": match.goals_for,
            "GA": match.goals_against,
            "GD": match.gd(),
            "Result": match.result(),
            "Notes": match.notes,
        })
    return pd.DataFrame(rows)

def quarter_df(match_list: List[Match]) -> pd.DataFrame:
    rows = []
    for match in match_list:
        q = match.quarters
        if not q:
            continue
        rows.append({
            "Date": match.date,
            "Opponent": match.opponent,
            "Q1 GF": q.q1_for,
            "Q1 GA": q.q1_against,
            "Q2 GF": q.q2_for,
            "Q2 GA": q.q2_against,
            "Q3 GF": q.q3_for,
            "Q3 GA": q.q3_against,
            "Q4 GF": q.q4_for,
            "Q4 GA": q.q4_against,
        })
    return pd.DataFrame(rows)

def quarter_averages(match_list: List[Match]) -> pd.DataFrame:
    data = {"Quarter": [], "Average Scored": [], "Average Conceded": [], "Average Margin": []}
    quarter_fields = {
        "Q1": ("q1_for", "q1_against"),
        "Q2": ("q2_for", "q2_against"),
        "Q3": ("q3_for", "q3_against"),
        "Q4": ("q4_for", "q4_against"),
    }
    for quarter, (gf_field, ga_field) in quarter_fields.items():
        goals_for = []
        goals_against = []
        for match in match_list:
            if not match.quarters:
                continue
            gf = getattr(match.quarters, gf_field)
            ga = getattr(match.quarters, ga_field)
            if gf is not None and ga is not None:
                goals_for.append(gf)
                goals_against.append(ga)
        if goals_for:
            avg_for = sum(goals_for) / len(goals_for)
            avg_against = sum(goals_against) / len(goals_against)
            data["Quarter"].append(quarter)
            data["Average Scored"].append(round(avg_for, 2))
            data["Average Conceded"].append(round(avg_against, 2))
            data["Average Margin"].append(round(avg_for - avg_against, 2))
    return pd.DataFrame(data)

df = matches_to_df(matches)
qdf = quarter_df(matches)
qavg = quarter_averages(matches)

st.title("🏐 Gelofte Skool 1st Netball Team 2026")
st.caption("Season tracker dashboard — results, quarter trends, competition split and player milestones.")

total_games = len(df)
wins = int((df["Result"] == "W").sum())
losses = int((df["Result"] == "L").sum())
draws = int((df["Result"] == "D").sum())
gf = int(df["GF"].sum())
ga = int(df["GA"].sum())
gd = int(df["GD"].sum())
win_pct = (wins / total_games * 100) if total_games else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Games Played", total_games)
col2.metric("Wins", wins)
col3.metric("Losses", losses)
col4.metric("Win %", f"{win_pct:.1f}%")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Goals For", gf)
col6.metric("Goals Against", ga)
col7.metric("Goal Difference", f"{gd:+}")
col8.metric("Average Margin", f"{gd / total_games:+.1f}")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Season Dashboard",
    "🏆 Competition Split",
    "⏱ Quarter Trends",
    "👥 Players",
    "📅 Fixtures",
])

with tab1:
    st.subheader("Season Match Log")
    st.dataframe(df, use_container_width=True)

    st.subheader("Last 5 Form")
    st.dataframe(df.tail(5)[["Date", "Opponent", "GF", "GA", "GD", "Result"]], use_container_width=True)

    st.subheader("Goal Difference by Match")
    st.bar_chart(df[["Opponent", "GD"]].set_index("Opponent"))

with tab2:
    st.subheader("Competition Split")
    split = df.groupby("Competition").agg(
        Played=("Opponent", "count"),
        Wins=("Result", lambda x: (x == "W").sum()),
        Losses=("Result", lambda x: (x == "L").sum()),
        Draws=("Result", lambda x: (x == "D").sum()),
        GF=("GF", "sum"),
        GA=("GA", "sum"),
        GD=("GD", "sum"),
    ).reset_index()
    split["Win %"] = (split["Wins"] / split["Played"] * 100).round(1)
    st.dataframe(split, use_container_width=True)
    st.bar_chart(split.set_index("Competition")[["GF", "GA"]])

with tab3:
    st.subheader("Quarter-by-Quarter Match Data")
    st.dataframe(qdf, use_container_width=True)

    st.subheader("Quarter Averages")
    st.dataframe(qavg, use_container_width=True)

    st.subheader("Average Margin by Quarter")
    st.bar_chart(qavg.set_index("Quarter")["Average Margin"])

    strongest = qavg.sort_values("Average Margin", ascending=False).iloc[0]
    weakest = qavg.sort_values("Average Margin", ascending=True).iloc[0]
    st.info(f"Strongest quarter so far: {strongest['Quarter']} with average margin {strongest['Average Margin']:+.2f}.")
    st.warning(f"Most important improvement quarter: {weakest['Quarter']} with average margin {weakest['Average Margin']:+.2f}.")

with tab4:
    st.subheader("Player Match Counts")
    player_rows = []
    for player, count in player_counts.items():
        player_rows.append({
            "Player": player,
            "Match Count": "" if count is None else count,
            "Player of Match": pom_counts.get(player, 0),
        })
    players_df = pd.DataFrame(player_rows)
    st.dataframe(players_df, use_container_width=True)

    st.subheader("Player of the Match Leaderboard")
    pom_df = pd.DataFrame(
        [{"Player": player, "Awards": count} for player, count in pom_counts.items()]
    ).sort_values("Awards", ascending=False)
    st.dataframe(pom_df, use_container_width=True)

with tab5:
    st.subheader("Remaining Fixtures")
    st.dataframe(upcoming_fixtures, use_container_width=True)

    st.subheader("Add New Result")
    st.write("This calculates a new result quickly. To permanently save it, add it into the matches list in the code.")

    with st.form("new_result_form"):
        opponent = st.text_input("Opponent")
        goals_for = st.number_input("Gelofte score", min_value=0, step=1)
        goals_against = st.number_input("Opponent score", min_value=0, step=1)
        submitted = st.form_submit_button("Calculate Result")

        if submitted:
            if opponent.strip():
                new_gd = goals_for - goals_against
                outcome = "W" if new_gd > 0 else "L" if new_gd < 0 else "D"
                st.success(
                    f"Gelofte {goals_for}-{goals_against} {opponent} | "
                    f"Result: {outcome} | GD: {new_gd:+}"
                )
            else:
                st.error("Please enter an opponent name.")

st.divider()
st.caption("Built for Gelofte 1st Netball — Start strong. Control the game. Finish strong. 💚")
