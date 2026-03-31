import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Social Media Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# CLEAN DARK UI
# =========================
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background-color: #0b0f19;
    color: white;
}

h1 {
    text-align: center;
    color: white;
    font-size: 46px;
    font-weight: 900;
    margin-bottom: 10px;
}

div[data-testid="metric-container"] {
    background-color: #151a26;
    border-radius: 14px;
    padding: 18px;
    border: 1px solid #2b3245;
    box-shadow: 0 4px 12px rgba(0,0,0,0.6);
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.stDataFrame {
    background-color: #151a26;
}

.stDownloadButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
def load_csv(path):
    return pd.read_csv(path)

df_fb = load_csv("data/facebook_data.csv")
df_ig = load_csv("data/instagram_data.csv")
df_li = load_csv("data/linkedin_data.csv")

df_fb["platform"] = "Facebook"
df_ig["platform"] = "Instagram"
df_li["platform"] = "LinkedIn"

df = pd.concat([df_fb, df_ig, df_li], ignore_index=True)

# =========================
# PROCESS DATA
# =========================
df["created_time"] = pd.to_datetime(df["created_time"])
df["engagement"] = df["likes"] + df["comments"] + df["shares"]

# =========================
# TITLE
# =========================
st.markdown("<h1>📊 Social Media Analytics Dashboard</h1>", unsafe_allow_html=True)

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔎 Filters")

platform_filter = st.sidebar.multiselect(
    "Platform",
    df["platform"].unique(),
    default=df["platform"].unique()
)

date_filter = st.sidebar.date_input(
    "Date Range",
    [df["created_time"].min(), df["created_time"].max()]
)

df = df[df["platform"].isin(platform_filter)]

df = df[
    (df["created_time"].dt.date >= date_filter[0]) &
    (df["created_time"].dt.date <= date_filter[1])
]

# =========================
# INSIGHTS (AUTO ANALYSIS)
# =========================
top_platform = df.groupby("platform")["engagement"].sum().idxmax()
avg_eng = df["engagement"].mean()
best_post = df.loc[df["engagement"].idxmax()]

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "📌 Overview",
    "📈 Analytics",
    "🔥 Top Posts",
    "📥 Export"
])

# =========================
# TAB 1 - OVERVIEW
# =========================
with tab1:

    st.markdown("## 📊 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👍 Likes", f"{df['likes'].sum():,}")
    col2.metric("💬 Comments", f"{df['comments'].sum():,}")
    col3.metric("🔁 Shares", f"{df['shares'].sum():,}")
    col4.metric("🚀 Engagement", f"{df['engagement'].sum():,}")

    st.markdown("---")

    st.success(f"🔥 Top Performing Platform: {top_platform}")

    st.info(f"📊 Average Engagement per Post: {avg_eng:.2f}")

    st.warning(f"⭐ Best Post ID: {best_post['message']}")

# =========================
# TAB 2 - ANALYTICS
# =========================
with tab2:

    st.markdown("## 📈 Engagement Trend Over Time")
    st.line_chart(df.set_index("created_time")["engagement"])

    st.markdown("## 📊 Platform Comparison")
    st.bar_chart(df.groupby("platform")["engagement"].sum())

# =========================
# TAB 3 - TOP POSTS
# =========================
with tab3:

    st.markdown("## 🔥 Top Performing Posts")

    top_df = df.sort_values("engagement", ascending=False).head(10)

    st.dataframe(top_df, use_container_width=True)

# =========================
# TAB 4 - EXPORT
# =========================
with tab4:

    st.markdown("## 📥 Download Data")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Full Dataset",
        data=csv,
        file_name="social_media_analytics.csv",
        mime="text/csv"
    )

    st.download_button(
        "⬇ Download Top Posts",
        data=top_df.to_csv(index=False).encode("utf-8"),
        file_name="top_posts.csv",
        mime="text/csv"
    )