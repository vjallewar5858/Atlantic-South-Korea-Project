import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="K-Pop Chart Intelligence | Atlantic RC",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main { background-color: #0d1117; }
    .stApp { background-color: #0d1117; }

    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }

    .metric-card {
        background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border-top: 3px solid #e94560;
    }

    .metric-value {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #e94560;
        line-height: 1;
    }

    .metric-label {
        font-size: 0.75rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 6px;
    }

    .section-header {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #f0f6fc;
        border-left: 4px solid #e94560;
        padding-left: 12px;
        margin: 24px 0 16px 0;
    }

    .insight-box {
        background: linear-gradient(135deg, #1c2128, #161b22);
        border: 1px solid #30363d;
        border-left: 4px solid #3fb950;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 12px 0;
        color: #c9d1d9;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    .highlight { color: #e94560; font-weight: 600; }

    .stSelectbox label, .stMultiSelect label,
    .stSlider label, .stDateInput label {
        color: #8b949e !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div[data-testid="stMetric"] {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px;
    }

    h1 { font-family: 'Rajdhani', sans-serif !important; color: #f0f6fc !important; }
    h2 { font-family: 'Rajdhani', sans-serif !important; color: #f0f6fc !important; }
    h3 { color: #c9d1d9 !important; }

    .stTabs [data-baseweb="tab-list"] {
        background-color: #161b22;
        border-bottom: 1px solid #30363d;
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #8b949e;
        font-weight: 500;
        padding: 10px 20px;
        border-radius: 6px 6px 0 0;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1c2128 !important;
        color: #e94560 !important;
        border-bottom: 2px solid #e94560 !important;
    }

    .stDataFrame { background-color: #161b22 !important; }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Plot Style ─────────────────────────────────────────────────
plt.style.use('dark_background')
DARK_BG  = '#0d1117'
CARD_BG  = '#161b22'
RED      = '#e94560'
BLUE     = '#58a6ff'
GREEN    = '#3fb950'
ORANGE   = '#d29922'
PURPLE   = '#bc8cff'
TEXT     = '#c9d1d9'

def style_fig(fig):
    fig.patch.set_facecolor(DARK_BG)
    for ax in fig.axes:
        ax.set_facecolor(CARD_BG)
        ax.tick_params(colors=TEXT, labelsize=9)
        ax.xaxis.label.set_color(TEXT)
        ax.yaxis.label.set_color(TEXT)
        ax.title.set_color('#f0f6fc')
        for spine in ax.spines.values():
            spine.set_edgecolor('#30363d')
    return fig

# ── Load Data ──────────────────────────────────────────────────
@st.cache(allow_output_mutation=True)
def load_data():
    df           = pd.read_csv('data/df_with_momentum.csv',   parse_dates=['date'])
    reentry_df   = pd.read_csv('data/reentry_analysis.csv')
    fandom_df    = pd.read_csv('data/fandom_scores.csv')
    retention_df = pd.read_csv('data/retention_analysis.csv', parse_dates=['reentry_date'])
    return df, reentry_df, fandom_df, retention_df

df, reentry_df, fandom_df, retention_df = load_data()

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px 0;'>
        <div style='font-family: Rajdhani; font-size: 1.5rem; font-weight: 700; color: #f0f6fc;'>
            🎵 K-Pop Intelligence
        </div>
        <div style='font-size: 0.75rem; color: #8b949e; letter-spacing: 1px; margin-top: 4px;'>
            ATLANTIC RECORDING CORP
        </div>
    </div>
    <hr style='border-color: #30363d; margin: 10px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("**FILTERS**")

    date_min = df['date'].min().date()
    date_max = df['date'].max().date()
    date_range = st.date_input("Date Range",
                               value=(date_min, date_max),
                               min_value=date_min,
                               max_value=date_max)

    album_types = st.multiselect("Album Type",
                                  options=df['album_type'].unique().tolist(),
                                  default=df['album_type'].unique().tolist())

    explicit_filter = st.selectbox("Explicit Content",
                                    options=["All", "Explicit Only", "Non-Explicit Only"])

    min_reentry = st.slider("Min Re-Entries", 0, int(reentry_df['reentry_count'].max()), 0)

    st.markdown("<hr style='border-color: #30363d;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 0.7rem; color: #8b949e; text-align: center; padding: 10px 0;'>
        Dataset: South Korea Top 40<br>
        Period: 2023 – 2024<br>
        Records: 27,784
    </div>
    """, unsafe_allow_html=True)

# ── Apply Filters ──────────────────────────────────────────────
filtered = df.copy()
if len(date_range) == 2:
    filtered = filtered[
        (filtered['date'].dt.date >= date_range[0]) &
        (filtered['date'].dt.date <= date_range[1])
    ]
if album_types:
    filtered = filtered[filtered['album_type'].isin(album_types)]
if explicit_filter == "Explicit Only":
    filtered = filtered[filtered['is_explicit'] == True]
elif explicit_filter == "Non-Explicit Only":
    filtered = filtered[filtered['is_explicit'] == False]

filtered_reentry = reentry_df[reentry_df['reentry_count'] >= min_reentry]
filtered_fandom  = fandom_df[fandom_df['reentry_count'] >= min_reentry]

# ── Header ─────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 30px 0 10px 0;'>
    <div style='font-family: Rajdhani; font-size: 2.8rem; font-weight: 700; color: #f0f6fc; line-height: 1;'>
        Comeback Momentum & Fandom Intensity
    </div>
    <div style='font-size: 1rem; color: #8b949e; margin-top: 8px;'>
        Chart Re-Entry Intelligence Dashboard  •  South Korea Top 40 Spotify Playlist  •  2023–2024
    </div>
</div>
<hr style='border-color: #30363d; margin-bottom: 24px;'>
""", unsafe_allow_html=True)

# ── KPI Row ────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)

kpis = [
    (k1, str(len(filtered)),             "Total Records"),
    (k2, str(filtered['artist'].nunique()), "Unique Artists"),
    (k3, str(filtered['song'].nunique()),   "Unique Songs"),
    (k4, f"{filtered['popularity'].mean():.1f}", "Avg Popularity"),
    (k5, str(len(filtered_reentry[filtered_reentry['reentry_count'] > 0])), "Songs Re-Entered"),
    (k6, f"{retention_df['retention_days'].mean():.1f}d", "Avg Comeback Retention"),
]

for col, val, label in kpis:
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{val}</div>
            <div class='metric-label'>{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview",
    "🔄 Re-Entry Analysis",
    "⚡ Momentum Spikes",
    "🎯 Fandom Intensity",
    "🔍 Song Explorer"
])

# ══════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<div class='section-header'>Popularity & Chart Overview</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(filtered['popularity'], bins=25, color=RED, edgecolor=DARK_BG, linewidth=0.5, alpha=0.9)
        ax.axvline(filtered['popularity'].mean(), color=BLUE, linestyle='--', linewidth=2,
                   label=f"Mean: {filtered['popularity'].mean():.1f}")
        ax.set_title('Popularity Distribution', fontweight='bold', pad=12)
        ax.set_xlabel('Popularity Score')
        ax.set_ylabel('Frequency')
        ax.legend(facecolor=CARD_BG, edgecolor='#30363d', labelcolor=TEXT)
        style_fig(fig)
        st.pyplot(fig)
        plt.close()

    with col2:
        monthly = filtered.copy()
        monthly['ym'] = monthly['date'].dt.to_period('M').astype(str)
        m_avg = monthly.groupby('ym')['popularity'].mean()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(m_avg.index, m_avg.values, color=RED, linewidth=2.5,
                marker='o', markersize=4, markerfacecolor=DARK_BG, markeredgewidth=2)
        ax.fill_between(m_avg.index, m_avg.values, m_avg.min(), alpha=0.15, color=RED)
        ax.set_title('Monthly Avg Popularity Trend', fontweight='bold', pad=12)
        ax.set_xlabel('Month')
        ax.set_ylabel('Avg Popularity')
        ax.tick_params(axis='x', rotation=45)
        style_fig(fig)
        st.pyplot(fig)
        plt.close()

    col3, col4 = st.columns(2)

    with col3:
        top_artists = filtered['artist'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_bar = [RED if i == 0 else BLUE for i in range(len(top_artists))]
        ax.barh(top_artists.index[::-1], top_artists.values[::-1],
                color=colors_bar[::-1], edgecolor=DARK_BG)
        ax.set_title('Top 10 Most Charted Artists', fontweight='bold', pad=12)
        ax.set_xlabel('Chart Appearances')
        for i, v in enumerate(top_artists.values[::-1]):
            ax.text(v + 10, i, str(v), va='center', fontsize=8, color=TEXT)
        style_fig(fig)
        st.pyplot(fig)
        plt.close()

    with col4:
        album_pop = filtered.groupby('album_type')['popularity'].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(album_pop.index, album_pop.values,
                      color=[RED, BLUE, GREEN][:len(album_pop)],
                      edgecolor=DARK_BG, width=0.5)
        ax.set_title('Avg Popularity by Album Type', fontweight='bold', pad=12)
        ax.set_ylabel('Avg Popularity Score')
        ax.set_ylim(65, album_pop.max() + 5)
        for bar, val in zip(bars, album_pop.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    f"{val:.1f}", ha='center', fontsize=11, fontweight='bold', color=TEXT)
        style_fig(fig)
        st.pyplot(fig)
        plt.close()

    st.markdown("""
    <div class='insight-box'>
        <b style='color:#3fb950;'>KEY INSIGHTS —</b>
        South Korea's chart is dominated by <span class='highlight'>Korean artists</span> in frequency,
        but <span class='highlight'>Western artists</span> lead in global popularity scores.
        Singles outperform albums both in chart frequency and average popularity.
        Mean popularity of <span class='highlight'>76.9/100</span> confirms this is a high-quality, globally-relevant playlist.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 2 — RE-ENTRY ANALYSIS
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-header'>Chart Re-Entry Patterns</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        top_reentry = filtered_reentry.sort_values('reentry_count', ascending=False).head(15)
        fig, ax = plt.subplots(figsize=(8, 6))
        colors_r = [RED if i < 3 else BLUE for i in range(len(top_reentry))]
        ax.barh(top_reentry['artist'][::-1], top_reentry['reentry_count'][::-1],
                color=colors_r[::-1], edgecolor=DARK_BG)
        ax.set_title('Top 15 Artists by Re-Entry Count', fontweight='bold', pad=12)
        ax.set_xlabel('Number of Re-Entries')
        for i, v in enumerate(top_reentry['reentry_count'][::-1]):
            ax.text(v + 0.05, i, str(v), va='center', fontsize=8, color=TEXT)
        style_fig(fig)
        st.pyplot(fig)
        plt.close()

    with col2:
        comeback = filtered_reentry[filtered_reentry['reentry_count'] > 0].groupby(
            'album_type')['reentry_count'].mean().round(2)
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(comeback.index, comeback.values,
                      color=[RED, BLUE, GREEN][:len(comeback)],
                      edgecolor=DARK_BG, width=0.4)
        ax.set_title('Album Comeback Advantage Index\n(Avg Re-Entries by Type)', fontweight='bold', pad=12)
        ax.set_ylabel('Avg Re-Entry Count')
        for bar, val in zip(bars, comeback.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f"{val:.2f}", ha='center', fontsize=12, fontweight='bold', color=TEXT)
        style_fig(fig)
        st.pyplot(fig)
        plt.close()

    col3, col4 = st.columns(2)

    with col3:
        fig, ax = plt.subplots(figsize=(8, 4))
        reentry_only = filtered_reentry[filtered_reentry['reentry_count'] > 0]['reentry_count']
        ax.hist(reentry_only, bins=15, color=PURPLE, edgecolor=DARK_BG, alpha=0.9)
        ax.set_title('Re-Entry Count Distribution', fontweight='bold', pad=12)
        ax.set_xlabel('Number of Re-Entries')
        ax.set_ylabel('Number of Songs')
        style_fig(fig)
        st.pyplot(fig)
        plt.close()

    with col4:
        if len(retention_df) > 0:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.hist(retention_df['retention_days'], bins=20,
                    color=GREEN, edgecolor=DARK_BG, alpha=0.9)
            ax.axvline(retention_df['retention_days'].mean(), color=RED,
                       linestyle='--', linewidth=2,
                       label=f"Mean: {retention_df['retention_days'].mean():.1f} days")
            ax.set_title('Post-Comeback Retention Days', fontweight='bold', pad=12)
            ax.set_xlabel('Days Retained After Re-Entry')
            ax.set_ylabel('Number of Comebacks')
            ax.legend(facecolor=CARD_BG, edgecolor='#30363d', labelcolor=TEXT)
            style_fig(fig)
            st.pyplot(fig)
            plt.close()

    st.markdown("<div class='section-header' style='font-size:1.1rem;'>Re-Entry Data Table</div>",
                unsafe_allow_html=True)
    show_cols = ['song','artist','album_type','reentry_count','avg_gap_days',
                 'total_appearances','peak_popularity','best_position']
    st.dataframe(
        filtered_reentry[filtered_reentry['reentry_count'] > 0][show_cols]
        .sort_values('reentry_count', ascending=False)
        .reset_index(drop=True),
        height=300
    )

    st.markdown("""
    <div class='insight-box'>
        <b style='color:#3fb950;'>KEY INSIGHTS —</b>
        K-Pop artists show <span class='highlight'>significantly higher re-entry rates</span> than other genres,
        confirming fandom-driven streaming cycles.
        Singles have a higher comeback advantage index than albums —
        shorter, targeted releases are more effective for <span class='highlight'>chart re-entry strategy</span>.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 3 — MOMENTUM SPIKES
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-header'>Momentum Spike Detection</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        top_momentum = filtered.nlargest(15, 'momentum_score')[
            ['date','song','artist','position','popularity','momentum_score']
        ].reset_index(drop=True)
        st.markdown("**Top 15 Highest Momentum Moments**")
        st.dataframe(top_momentum, height=400)

    with col2:
        fig, ax = plt.subplots(figsize=(8, 6))
        artist_ms = filtered.groupby('artist')['momentum_score'].sum().sort_values(
            ascending=False).head(12)
        ax.barh(artist_ms.index[::-1], artist_ms.values[::-1],
                color=ORANGE, edgecolor=DARK_BG, alpha=0.9)
        ax.set_title('Total Momentum Score by Artist\n(Cumulative Comeback Intensity)', fontweight='bold', pad=12)
        ax.set_xlabel('Total Momentum Score')
        style_fig(fig)
        st.pyplot(fig)
        plt.close()

    col3, col4 = st.columns(2)

    with col3:
        fig, ax = plt.subplots(figsize=(8, 4))
        monthly_ms = filtered.copy()
        monthly_ms['ym'] = monthly_ms['date'].dt.to_period('M').astype(str)
        ms_trend = monthly_ms.groupby('ym')['momentum_score'].mean()
        ax.plot(ms_trend.index, ms_trend.values, color=ORANGE,
                linewidth=2.5, marker='o', markersize=4,
                markerfacecolor=DARK_BG, markeredgewidth=2)
        ax.fill_between(ms_trend.index, ms_trend.values, 0, alpha=0.15, color=ORANGE)
        ax.set_title('Monthly Avg Momentum Score Trend', fontweight='bold', pad=12)
        ax.set_xlabel('Month')
        ax.set_ylabel('Avg Momentum Score')
        ax.tick_params(axis='x', rotation=45)
        style_fig(fig)
        st.pyplot(fig)
        plt.close()

    with col4:
        fig, ax = plt.subplots(figsize=(8, 4))
        exp_ms = filtered.groupby('is_explicit')['momentum_score'].mean()
        labels = ['Non-Explicit', 'Explicit']
        ax.bar(labels, exp_ms.values, color=[BLUE, RED], edgecolor=DARK_BG, width=0.4)
        ax.set_title('Momentum Score:\nExplicit vs Non-Explicit', fontweight='bold', pad=12)
        ax.set_ylabel('Avg Momentum Score')
        for i, v in enumerate(exp_ms.values):
            ax.text(i, v + 0.001, f"{v:.4f}", ha='center', fontsize=11,
                    fontweight='bold', color=TEXT)
        style_fig(fig)
        st.pyplot(fig)
        plt.close()

    st.markdown("""
    <div class='insight-box'>
        <b style='color:#3fb950;'>KEY INSIGHTS —</b>
        Momentum spikes are <span class='highlight'>concentrated around specific artists</span>,
        not evenly distributed — confirming fandom-driven rather than organic chart movement.
        Seasonal peaks in momentum scores align with K-Pop <span class='highlight'>comeback seasons</span>
        (typically Q1 and Q4).
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 4 — FANDOM INTENSITY
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-header'>Fandom Intensity Leaderboard</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 0.8])

    with col1:
        top_fandom = filtered_fandom.sort_values(
            'fandom_intensity_score', ascending=False).head(20)
        fig, ax = plt.subplots(figsize=(9, 8))
        colors_f = [RED if i < 3 else BLUE if i < 8 else PURPLE for i in range(len(top_fandom))]
        ax.barh(top_fandom['artist'][::-1], top_fandom['fandom_intensity_score'][::-1],
                color=colors_f[::-1], edgecolor=DARK_BG, alpha=0.9)
        ax.set_title('Fandom Intensity Score — Top 20 Artists\n(Re-Entry + Spike + Recovery composite)',
                     fontweight='bold', pad=12)
        ax.set_xlabel('Fandom Intensity Score (0–100)')
        for i, v in enumerate(top_fandom['fandom_intensity_score'][::-1]):
            ax.text(v + 0.3, i, f"{v:.1f}", va='center', fontsize=8, color=TEXT)
        style_fig(fig)
        st.pyplot(fig)
        plt.close()

    with col2:
        fig, axes = plt.subplots(3, 1, figsize=(6, 8))
        metrics = [
            ('reentry_score',  'Re-Entry Score',   RED),
            ('spike_score',    'Spike Score',       ORANGE),
            ('recovery_score', 'Recovery Score',    GREEN),
        ]
        for ax, (col_name, title, color) in zip(axes, metrics):
            top5 = filtered_fandom.sort_values(col_name, ascending=False).head(8)
            ax.barh(top5['artist'][::-1], top5[col_name][::-1],
                    color=color, edgecolor=DARK_BG, alpha=0.9)
            ax.set_title(f'Top 8 — {title}', fontweight='bold', fontsize=10, pad=8)
            ax.set_xlabel('Score')
            style_fig(fig)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("<div class='section-header' style='font-size:1.1rem;'>Full Fandom Score Table</div>",
                unsafe_allow_html=True)
    fandom_show = ['artist','song','reentry_count','total_appearances',
                   'reentry_score','spike_score','recovery_score','fandom_intensity_score']
    st.dataframe(
        filtered_fandom[fandom_show].sort_values(
            'fandom_intensity_score', ascending=False).reset_index(drop=True),
        height=300
    )

    st.markdown("""
    <div class='insight-box'>
        <b style='color:#3fb950;'>KEY INSIGHTS —</b>
        The Fandom Intensity Score reveals artists whose chart presence is
        <span class='highlight'>community-driven</span> rather than passive listening.
        High-scoring artists represent Atlantic's most <span class='highlight'>strategically valuable</span>
        partnerships for release timing and promotional campaigns in the Korean market.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 5 — SONG EXPLORER
# ══════════════════════════════════════════════════════════════
with tab5:
    st.markdown("<div class='section-header'>Song & Artist Deep Dive</div>", unsafe_allow_html=True)

    search_artist = st.selectbox("Select Artist",
                                  options=["All"] + sorted(df['artist'].unique().tolist()))

    if search_artist != "All":
        artist_df = df[df['artist'] == search_artist].sort_values('date')

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Appearances", len(artist_df))
        with m2:
            st.metric("Avg Popularity", f"{artist_df['popularity'].mean():.1f}")
        with m3:
            st.metric("Best Position", artist_df['position'].min())
        with m4:
            reentry_row = reentry_df[reentry_df['artist'] == search_artist]
            reentries = reentry_row['reentry_count'].sum() if len(reentry_row) > 0 else 0
            st.metric("Total Re-Entries", reentries)

        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(artist_df['date'], artist_df['popularity'],
                    color=RED, linewidth=2, marker='o', markersize=3,
                    markerfacecolor=DARK_BG, markeredgewidth=1.5)
            ax.fill_between(artist_df['date'], artist_df['popularity'],
                            artist_df['popularity'].min(), alpha=0.1, color=RED)
            ax.set_title(f'{search_artist} — Popularity Timeline', fontweight='bold', pad=12)
            ax.set_xlabel('Date')
            ax.set_ylabel('Popularity Score')
            ax.tick_params(axis='x', rotation=45)
            style_fig(fig)
            st.pyplot(fig)
            plt.close()

        with col2:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.scatter(artist_df['date'], artist_df['position'],
                       color=BLUE, s=20, alpha=0.7)
            ax.invert_yaxis()
            ax.set_title(f'{search_artist} — Chart Position Timeline', fontweight='bold', pad=12)
            ax.set_xlabel('Date')
            ax.set_ylabel('Position (1 = Top)')
            ax.tick_params(axis='x', rotation=45)
            style_fig(fig)
            st.pyplot(fig)
            plt.close()

        st.markdown("**Song-Level Breakdown**")
        song_summary = artist_df.groupby('song').agg(
            appearances=('date','count'),
            avg_popularity=('popularity','mean'),
            best_position=('position','min'),
            album_type=('album_type','first')
        ).round(2).sort_values('appearances', ascending=False).reset_index()
        st.dataframe(song_summary, height=300)

    else:
        st.info("Select an artist from the dropdown above to see their detailed analysis.")