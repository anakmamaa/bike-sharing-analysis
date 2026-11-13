
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Bike Sharing Analysis",
    page_icon="🎀",
    layout="wide"
)

# ==============================
# CUSTOM CSS
# ==============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

.stApp {
    background: #FFF7FA;
    color: #684B56;
    font-family: 'DM Sans', sans-serif;
}

header {visibility: hidden;}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #A94F70 !important;
}

p, label, span {
    color: #795D68;
}

.hero {
    background: linear-gradient(120deg, #F9DCE7, #FFF0F5, #FCE5ED);
    padding: 35px;
    border-radius: 25px;
    border: 1px solid #F3D0DD;
    margin-bottom: 28px;
}

.hero h1 {
    font-size: 38px;
    margin-bottom: 5px;
    color: #A94F70 !important;
}

.hero p {
    font-size: 14px;
    margin-bottom: 0;
    color: #936C7B;
}

.section-title {
    font-family: 'Playfair Display', serif;
    color: #A94F70;
    font-size: 23px;
    margin-top: 20px;
    margin-bottom: 15px;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid #F2D6E0;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 5px 18px rgba(183, 113, 143, 0.07);
    min-height: 120px;
}

.metric-label {
    font-size: 13px;
    color: #A47C8B;
    margin-bottom: 10px;
}

.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 27px;
    font-weight: 700;
    color: #B65E80;
}

.metric-note {
    font-size: 11px;
    color: #B995A3;
    margin-top: 5px;
}

.chart-card {
    background: #FFFFFF;
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #F2D6E0;
    box-shadow: 0 5px 18px rgba(183, 113, 143, 0.05);
}

div[data-testid="stSidebar"] {
    background: #FCEBF1;
    border-right: 1px solid #F2D6E0;
}

div[data-testid="stSidebar"] h2 {
    color: #A94F70 !important;
}

.stMultiSelect div[data-baseweb="select"] > div {
    background: white;
    border-color: #E9BCCD;
    border-radius: 12px;
}

.stButton button {
    background: #D98BA8;
    color: white;
    border: none;
    border-radius: 12px;
}

hr {
    border-color: #F0D6E0;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #F2D6E0;
    border-radius: 15px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("day.csv")
df["dteday"] = pd.to_datetime(df["dteday"])

season_mapping = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

weather_mapping = {
    1: "Clear",
    2: "Mist / Cloudy",
    3: "Light Rain / Snow",
    4: "Heavy Rain / Snow"
}

df["season"] = df["season"].map(season_mapping)
df["weathersit"] = df["weathersit"].map(weather_mapping)

# ==============================
# SIDEBAR
# ==============================
st.sidebar.markdown("# 🎀 Pinkie Journal")
st.sidebar.caption("A little bicycle data diary ♡")
st.sidebar.divider()

st.sidebar.markdown("### Filter your data")

selected_season = st.sidebar.multiselect(
    "Choose season",
    options=["Spring", "Summer", "Fall", "Winter"],
    default=["Spring", "Summer", "Fall", "Winter"]
)

selected_weather = st.sidebar.multiselect(
    "Choose weather",
    options=df["weathersit"].dropna().unique(),
    default=list(df["weathersit"].dropna().unique())
)

filtered_df = df[
    (df["season"].isin(selected_season)) &
    (df["weathersit"].isin(selected_weather))
]

st.sidebar.divider()
st.sidebar.caption("Made with love & little pink bows ♡")

# ==============================
# HEADER
# ==============================
st.markdown("""
<div class="hero">
    <h1>🎀 Pinkie Bike Journal</h1>
    <p>A sweet little journey through bike sharing data · 2011 — 2012</p>
    <p>Discover how seasons and weather affect bicycle rentals ♡</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# METRICS
# ==============================
st.markdown('<div class="section-title">A little overview ♡</div>',
            unsafe_allow_html=True)

total_rentals = filtered_df["cnt"].sum()
average_rentals = filtered_df["cnt"].mean()
total_days = len(filtered_df)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">♡ Total rentals</div>
        <div class="metric-value">{total_rentals:,.0f}</div>
        <div class="metric-note">Total bicycle rentals</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">♡ Daily average</div>
        <div class="metric-value">{average_rentals:,.0f}</div>
        <div class="metric-note">Average rentals per day</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">♡ Total days</div>
        <div class="metric-value">{total_days:,}</div>
        <div class="metric-note">Days included in analysis</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==============================
# CHART SETTINGS
# ==============================
pink_palette = ["#E9A6BD", "#D889A8", "#C66F94", "#F2C6D5"]

def style_chart(ax):
    ax.set_facecolor("#FFFFFF")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#F0D6E0")
    ax.spines["bottom"].set_color("#F0D6E0")
    ax.tick_params(colors="#896B77")
    ax.xaxis.label.set_color("#896B77")
    ax.yaxis.label.set_color("#896B77")
    ax.title.set_color("#A94F70")

# ==============================
# SEASON CHART
# ==============================
st.markdown('<div class="section-title">01. Rentals by season 🌷</div>',
            unsafe_allow_html=True)

season_order = ["Spring", "Summer", "Fall", "Winter"]
season_avg = (
    filtered_df.groupby("season")["cnt"]
    .mean()
    .reindex(season_order)
    .dropna()
)

fig1, ax1 = plt.subplots(figsize=(10, 4))
bars = ax1.bar(
    season_avg.index,
    season_avg.values,
    color=pink_palette,
    width=0.55
)

ax1.set_title("Average bicycle rentals in each season", pad=18)
ax1.set_xlabel("Season")
ax1.set_ylabel("Average rentals")
style_chart(ax1)

for bar in bars:
    ax1.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        f"{bar.get_height():,.0f}",
        ha="center",
        va="bottom",
        fontsize=9,
        color="#A94F70"
    )

fig1.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

# ==============================
# WEATHER CHART
# ==============================
st.markdown('<div class="section-title">02. Rentals by weather ☁️</div>',
            unsafe_allow_html=True)

weather_order = ["Clear", "Mist / Cloudy", "Light Rain / Snow", "Heavy Rain / Snow"]
weather_avg = (
    filtered_df.groupby("weathersit")["cnt"]
    .mean()
    .reindex(weather_order)
    .dropna()
)

fig2, ax2 = plt.subplots(figsize=(10, 4))
bars = ax2.bar(
    weather_avg.index,
    weather_avg.values,
    color=["#E9A6BD", "#D889A8", "#C66F94", "#F2C6D5"][:len(weather_avg)],
    width=0.55
)

ax2.set_title("Average bicycle rentals in different weather", pad=18)
ax2.set_xlabel("Weather condition")
ax2.set_ylabel("Average rentals")
style_chart(ax2)
ax2.tick_params(axis="x", rotation=10)

for bar in bars:
    ax2.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        f"{bar.get_height():,.0f}",
        ha="center",
        va="bottom",
        fontsize=9,
        color="#A94F70"
    )

fig2.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

# ==============================
# MONTHLY TREND
# ==============================
st.markdown('<div class="section-title">03. Monthly rental diary 🌸</div>',
            unsafe_allow_html=True)

monthly_avg = (
    filtered_df.groupby("mnth")["cnt"]
    .mean()
    .reindex(range(1, 13))
)

fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.plot(
    monthly_avg.index,
    monthly_avg.values,
    marker="o",
    linewidth=2.5,
    markersize=7,
    color="#D889A8"
)
ax3.fill_between(
    monthly_avg.index,
    monthly_avg.values,
    alpha=0.12,
    color="#E9A6BD"
)

ax3.set_title("Monthly average bicycle rentals", pad=18)
ax3.set_xlabel("Month")
ax3.set_ylabel("Average rentals")
ax3.set_xticks(range(1, 13))
ax3.set_xticklabels([
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
])
style_chart(ax3)

fig3.tight_layout()
st.pyplot(fig3)
plt.close(fig3)

# ==============================
# DATA TABLE
# ==============================
st.markdown("---")
st.markdown('<div class="section-title">A peek at the data ♡</div>',
            unsafe_allow_html=True)

st.caption("Here is the bicycle rental data based on your selected filters.")

st.dataframe(
    filtered_df,
    width="stretch",
    hide_index=True
)

# ==============================
# FOOTER
# ==============================
st.markdown("""
<br>
<div style="
    text-align:center;
    background:#FCEBF1;
    border-radius:18px;
    padding:20px;
    color:#A47C8B;
">
    <div style="font-size:22px;">🎀 ♡ 🎀</div>
    <b style="color:#A94F70;">Thank you for visiting Pinkie Bike Journal!</b>
    <p style="font-size:12px;margin-top:5px;">
        A little data, a little pink, and lots of curiosity.
    </p>
</div>
""", unsafe_allow_html=True)

