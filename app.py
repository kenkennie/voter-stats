import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Kenya Voter Records Dashboard",
    page_icon="🗳️",
    layout="wide",
)

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        border: 1px solid #e9ecef;
    }
    div[data-testid="metric-container"] {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 0.75rem 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("voters.csv")
    return df


df = load_data()

# ── Header ──────────────────────────────────────────────────────────────────
st.title("🗳️ Kenya Voter Records Dashboard")
st.caption(f"Showing data from voters.csv · {len(df):,} total records")
st.divider()

# ── Sidebar Filters ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")

    # County filter
    counties = ["All Counties"] + sorted(df["county"].unique().tolist())
    selected_county = st.selectbox("County", counties)

    # Constituency (cascading)
    if selected_county != "All Counties":
        constituencies = ["All Constituencies"] + sorted(
            df[df["county"] == selected_county]["constituency"].unique().tolist()
        )
    else:
        constituencies = ["All Constituencies"] + sorted(df["constituency"].unique().tolist())
    selected_constituency = st.selectbox("Constituency", constituencies)

    # Ward (cascading)
    temp = df.copy()
    if selected_county != "All Counties":
        temp = temp[temp["county"] == selected_county]
    if selected_constituency != "All Constituencies":
        temp = temp[temp["constituency"] == selected_constituency]
    wards = ["All Wards"] + sorted(temp["ward"].unique().tolist())
    selected_ward = st.selectbox("Ward", wards)

    st.divider()

    # Year filter
    years = ["All Years"] + sorted(df["registration_year"].unique().tolist())
    selected_year = st.selectbox("Registration Year", years)

    # Gender filter
    genders = ["All Genders"] + sorted(df["gender"].unique().tolist())
    selected_gender = st.selectbox("Gender", genders)

    # Status filter
    statuses = ["All Statuses"] + sorted(df["voter_status"].unique().tolist())
    selected_status = st.selectbox("Voter Status", statuses)

    st.divider()

    # Age range
    min_age, max_age = int(df["age"].min()), int(df["age"].max())
    age_range = st.slider("Age Range", min_age, max_age, (min_age, max_age))

    st.divider()

    # Name search
    name_search = st.text_input("Search by name", placeholder="e.g. Wanjiku")

# ── Apply Filters ────────────────────────────────────────────────────────────
filtered = df.copy()
if selected_county != "All Counties":
    filtered = filtered[filtered["county"] == selected_county]
if selected_constituency != "All Constituencies":
    filtered = filtered[filtered["constituency"] == selected_constituency]
if selected_ward != "All Wards":
    filtered = filtered[filtered["ward"] == selected_ward]
if selected_year != "All Years":
    filtered = filtered[filtered["registration_year"] == selected_year]
if selected_gender != "All Genders":
    filtered = filtered[filtered["gender"] == selected_gender]
if selected_status != "All Statuses":
    filtered = filtered[filtered["voter_status"] == selected_status]
filtered = filtered[
    (filtered["age"] >= age_range[0]) & (filtered["age"] <= age_range[1])
]
if name_search:
    filtered = filtered[
        filtered["full_name"].str.contains(name_search, case=False, na=False)
    ]

# ── Metric Cards ─────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Voters", f"{len(filtered):,}")
col2.metric("Counties", filtered["county"].nunique())
col3.metric("Wards", filtered["ward"].nunique())
col4.metric("Avg Age", f"{filtered['age'].mean():.1f}" if len(filtered) else "—")
col5.metric(
    "Active Voters",
    f"{len(filtered[filtered['voter_status'] == 'Active']):,}" if len(filtered) else "—",
)

st.divider()

# ── Charts Row 1 ─────────────────────────────────────────────────────────────
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Voters by County")
    if len(filtered):
        county_counts = (
            filtered["county"].value_counts().reset_index()
        )
        county_counts.columns = ["county", "count"]
        fig = px.bar(
            county_counts,
            x="count",
            y="county",
            orientation="h",
            color="count",
            color_continuous_scale="Teal",
            labels={"count": "Voters", "county": "County"},
        )
        fig.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0),
            height=320,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis={"categoryorder": "total ascending"},
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data matches your filters.")

with chart_col2:
    st.subheader("Age Distribution")
    if len(filtered):
        bins = [18, 25, 35, 50, 65, 120]
        labels = ["18–25", "26–35", "36–50", "51–65", "65+"]
        filtered["age_group"] = pd.cut(filtered["age"], bins=bins, labels=labels, right=False)
        age_dist = filtered["age_group"].value_counts().sort_index().reset_index()
        age_dist.columns = ["age_group", "count"]
        fig2 = px.bar(
            age_dist,
            x="age_group",
            y="count",
            color="count",
            color_continuous_scale="Purples",
            labels={"age_group": "Age Group", "count": "Voters"},
        )
        fig2.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0),
            height=320,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        fig2.update_traces(marker_line_width=0)
        st.plotly_chart(fig2, use_container_width=True)

# ── Charts Row 2 ─────────────────────────────────────────────────────────────
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.subheader("Registrations by Year")
    if len(filtered):
        year_counts = (
            filtered["registration_year"].value_counts().sort_index().reset_index()
        )
        year_counts.columns = ["year", "count"]
        year_counts["year"] = year_counts["year"].astype(str)
        fig3 = px.bar(
            year_counts,
            x="year",
            y="count",
            color="count",
            color_continuous_scale="Blues",
            labels={"year": "Election Year", "count": "Registrations"},
        )
        fig3.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0),
            height=300,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        fig3.update_traces(marker_line_width=0)
        st.plotly_chart(fig3, use_container_width=True)

with chart_col4:
    st.subheader("Gender Split")
    if len(filtered):
        gender_counts = filtered["gender"].value_counts().reset_index()
        gender_counts.columns = ["gender", "count"]
        fig4 = px.pie(
            gender_counts,
            names="gender",
            values="count",
            color="gender",
            color_discrete_map={"Female": "#1D9E75", "Male": "#7F77DD"},
            hole=0.55,
        )
        fig4.update_layout(
            margin=dict(l=0, r=0, t=10, b=0),
            height=300,
            legend=dict(orientation="h", y=-0.1),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        fig4.update_traces(textinfo="percent+label", showlegend=True)
        st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Voter Status Breakdown ────────────────────────────────────────────────────
st.subheader("Voter Status Breakdown")
if len(filtered):
    status_counts = filtered["voter_status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]
    color_map = {"Active": "#1D9E75", "Inactive": "#E24B4A", "Under Review": "#EF9F27"}
    fig5 = px.bar(
        status_counts,
        x="status",
        y="count",
        color="status",
        color_discrete_map=color_map,
        labels={"status": "Status", "count": "Voters"},
    )
    fig5.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        height=260,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig5.update_traces(marker_line_width=0)
    st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ── Data Table ────────────────────────────────────────────────────────────────
st.subheader(f"Voter Records · {len(filtered):,} results")

display_cols = [
    "full_name", "gender", "age", "national_id",
    "county", "constituency", "ward",
    "registration_year", "occupation", "voter_status",
]

col_labels = {
    "full_name": "Full Name",
    "gender": "Gender",
    "age": "Age",
    "national_id": "National ID",
    "county": "County",
    "constituency": "Constituency",
    "ward": "Ward",
    "registration_year": "Year Reg.",
    "occupation": "Occupation",
    "voter_status": "Status",
}

st.dataframe(
    filtered[display_cols].rename(columns=col_labels),
    use_container_width=True,
    height=400,
    hide_index=True,
)

# ── Download Button ───────────────────────────────────────────────────────────
csv_export = filtered[display_cols].rename(columns=col_labels).to_csv(index=False)
st.download_button(
    label="⬇️ Download filtered data as CSV",
    data=csv_export,
    file_name="filtered_voters.csv",
    mime="text/csv",
)