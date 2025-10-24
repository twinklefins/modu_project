# =============================
# 🎵 Stay or Skip — Main Streamlit App
# =============================
import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------
# 1️⃣ 데이터 불러오기 함수
# -----------------------------
@st.cache_data(show_spinner=False)
def load_data():
    path = Path(__file__).with_name("spotify_merged.xlsx")  # 같은 폴더의 엑셀 파일 경로
    return pd.read_excel(path)

# -----------------------------
# 2️⃣ 예외 처리 (파일 없거나 에러 방지)
# -----------------------------
try:
    tidy = load_data()
except FileNotFoundError:
    st.error("⚠️ `spotify_merged.xlsx` 파일을 찾을 수 없습니다. 레포 루트에 올려주세요.")
    st.stop()
except Exception as e:
    st.error(f"데이터 로드 중 오류 발생: {e}")
    st.stop()

# -----------------------------
# 3️⃣ 페이지 설정 및 내용
# -----------------------------
st.set_page_config(page_title="Stay or Skip 🎵", page_icon="🎧", layout="wide")

st.title("🎵 Stay or Skip — Spotify User Behavior Dashboard")

# 예시: 데이터 확인용
st.dataframe(tidy.head())

# 이후에 네 탭 구성(tabs[3])이나 그래프 코드들이 여기 아래에 들어가면 됨

# app_stay_or_skip.py — Spotify Green themed
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64

def vgap(px: int):
    """위아래 여백을 강제로 추가하는 세로 스페이서"""
    import streamlit as st
    st.markdown(f'<div style="height:{px}px;"></div>', unsafe_allow_html=True)

def tight_top(px: int):
    """바로 다음 요소의 위 여백을 줄이는 용도 (음수 px 권장)"""
    import streamlit as st
    st.markdown(f'<div style="margin-top:{px}px;"></div>', unsafe_allow_html=True)

st.set_page_config(page_title="Stay or Skip", page_icon="🎧", layout="wide")

# ================= CSS =================
st.markdown("""
<style>
:root{
  /* Spotify-like palette */
  --bg:#121212;                /* main background */
  --panel:#191414;             /* sidebar/card panel */
  --text:#F9FCF9;              /* main text (soft white) */
  --muted:#D7E4DC;            /* muted text (초록기 살짝) */
  --line:rgba(255,255,255,.08);

  --brand:#1DB954;             /* Primary Green */
  --brand-2:#1ED760;           /* Lighter Green (hover/active) */
  --soft-ivory:#E8F5E9;        /* 아주 연한 그린 아이보리 */
  --tab-underline:rgba(29,185,84,.5);
  --navShift:18px;
}

/* ===== Dark theme base ===== */
html, body, .stApp,
[data-testid="stAppViewContainer"], [data-testid="stMain"]{
  background:var(--bg) !important; color:var(--text) !important;
}
[data-testid="stHeader"]{ background:var(--bg) !important; box-shadow:none !important; }
[data-testid="stAppViewContainer"] .main .block-container{
  padding-top:.15rem !important; padding-bottom:2rem !important;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"]{ background:var(--panel) !important; color:var(--text) !important; }
section[data-testid="stSidebar"] .block-container{ padding-top:.25rem !important; padding-bottom:.8rem !important; }
section[data-testid="stSidebar"] img{ opacity:.98; margin:.1rem 0 .5rem 0; }
hr.cup-divider{ border:none; height:1px; background:var(--line); margin:.6rem 0 .5rem 0; }

/* 메뉴(라디오) 그룹 */
section[data-testid="stSidebar"] [role="radiogroup"]{
  display:flex; flex-direction:column; gap:.30rem; margin-left:var(--navShift) !important;
}
section[data-testid="stSidebar"] label[data-baseweb="radio"]{
  position:relative !important; display:block !important;
  background:transparent !important; border:none !important; border-radius:6px !important;
  padding:.35rem .45rem .35rem .90rem !important; line-height:1.08 !important; cursor:pointer !important;
  transition:color .12s ease, background .12s ease !important;
}
section[data-testid="stSidebar"] label[data-baseweb="radio"] p{
  margin:0 !important; color:#CFE3D8 !important; font-weight:600 !important; letter-spacing:.15px !important;
  font-size:.94rem !important; transition:color .12s ease !important;
}
/* Hover */
section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover p{ color:var(--brand-2) !important; }
/* Selected: left green dot + white text */
section[data-testid="stSidebar"] label[data-baseweb="radio"][aria-checked="true"],
section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked){
  background:transparent !important; border:none !important;
}
section[data-testid="stSidebar"] label[data-baseweb="radio"][aria-checked="true"]::before,
section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked)::before{
  content:""; position:absolute; left:.42rem; top:50%;
  width:9px; height:9px; border-radius:50%; background:var(--brand); transform:translateY(-50%);
}
section[data-testid="stSidebar"] label[data-baseweb="radio"][aria-checked="true"] p,
section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) p{
  color:#FFF !important; font-weight:700 !important;
}
/* 기본 라디오 불릿 숨김 */
section[data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child,
section[data-testid="stSidebar"] label[data-baseweb="radio"] svg{ display:none !important; }
section[data-testid="stSidebar"] label[data-baseweb="radio"] input[type="radio"]{
  position:absolute !important; left:-9999px !important; opacity:0 !important;
}

/* Sidebar footer & link button */
hr.cup-footer-line{ border:none; height:1px; background:var(--line); margin:.8rem 0 .75rem 0; }
.cup-sidebar-footer{ margin-left:var(--navShift) !important; color:var(--muted); font-size:.84rem; letter-spacing:.1px; text-align:left; }
.cup-link-btn{
  display:inline-block; margin-bottom:.45rem; padding:6px 10px; font-size:.85rem; font-weight:600;
  color:var(--brand); text-decoration:none; border:1px solid rgba(29,185,84,.45); border-radius:6px; transition:all .2s ease;
}
.cup-link-btn:hover{ background:var(--brand); color:#0E0E0E; border-color:var(--brand); }

/* ===== Main: typography & sections ===== */
h1{ font-weight:800; letter-spacing:-0.2px; margin:0 0 -0.2rem 0 !important; }
.cup-subtitle{ color:var(--muted); font-size:1.08rem; font-weight:500; margin:0 0 1rem 0; letter-spacing:.1px; }
.cup-h2{ display:flex; align-items:center; gap:.8rem; margin:1.6rem 0 .9rem 0; font-weight:700; font-size:1.25rem; letter-spacing:0.1px; }
.cup-h2::before{ content:""; display:inline-block; width:4px; height:22px; background:var(--brand); border-radius:2px; }
.cup-card{ background:transparent; border:1px solid var(--line); border-radius:10px; padding:1rem 1.2rem; margin:1.1rem 0; }

/* ===== Tabs: no glow, green underline ===== */
.stTabs [aria-selected="true"],
.stTabs [data-baseweb="tab"]:focus,
.stTabs [data-baseweb="tab"]:active {
  background: transparent;
  box-shadow: none; filter: none;
}
.stTabs [aria-selected="true"] p{ color: var(--brand-2); text-shadow:none; }
.stTabs [data-baseweb="tab"]:hover{ background:transparent; box-shadow:none; }
.stTabs [data-baseweb="tab"]:hover p{ color: rgba(255,255,255,.85); }

/* 바닥 라인은 연하게 */
.stTabs [role="tablist"]{ border-color: rgba(255,255,255,.08); }

/* 각 탭 밑줄 초기화 + 활성/호버 색상 */
.stTabs [data-baseweb="tab"]{ border-bottom: 2px solid transparent; }
.stTabs [data-baseweb="tab"][aria-selected="true"]{ border-bottom-color: var(--brand); }
.stTabs [data-baseweb="tab"]:hover{ border-bottom-color: var(--brand-2); }

/* <<<< 핵심: BaseWeb 탭 하이라이트 바 색 고정 >>>> */
.stTabs [data-baseweb="tab-highlight"]{
  background: var(--brand) !important;   /* #1DB954 */
}
            
/* ===== 비활성 탭 텍스트 밝기 보정 ===== */
.stTabs [data-baseweb="tab"] p {
  color: rgba(255,255,255,0.72) !important;  /* 기본 0.55 → 0.72 정도로 밝게 */
  transition: color .15s ease;
}
.stTabs [data-baseweb="tab"]:hover p {
  color: var(--brand-2) !important;          /* 호버 시 라이트 그린 */
}
            
/* ===== Spotify KPI Custom Style ===== */

/* KPI 숫자 스타일 */
div[data-testid="stMetric"] div[data-testid="stMetricValue"]{
  color: var(--brand) !important;     /* Spotify Green (#1DB954) */
  font-weight: 800 !important;
  font-size: 2.2rem !important;       /* 글씨 크기 키움 */
  line-height: 1.1 !important;
  white-space: nowrap !important;     /* 줄바꿈 방지 */
}

/* KPI 라벨 스타일 */
div[data-testid="stMetric"] div[data-testid="stMetricLabel"] p{
  font-size: 1.05rem !important;      /* 살짝 키움 */
  color: var(--muted) !important;
  letter-spacing:.2px;
}

/* 환경별 DOM 구조 대응 (백업용 선택자) */
div[data-testid="stMetric"] > div:nth-child(2) > div:first-child{
  color: var(--brand) !important;
  font-weight: 800 !important;
}
div[data-testid="stMetric"] > div:first-child p{
  color: var(--muted) !important;
}

/* KPI + 기호 살짝 작게 (super 위치) */
.cup-kpi-plus small{
  font-size:60%;
  opacity:.85;
  vertical-align:super;
}
            
/* KPI 묶음 래퍼 안에서만 간격 제어 */
.kpi-tight [data-testid="stHorizontalBlock"]{ gap:.2rem !important; }   /* 컬럼 간격 */
.kpi-tight [data-testid="column"]{ padding-left:.05rem !important; padding-right:.05rem !important; }
/* metric 자체 여백도 살짝 타이트하게 */
.kpi-tight [data-testid="stMetric"]{ margin-bottom:0 !important; }
            
/* Team Intro 박스 */
.cup-info-box {
  background: rgba(255,255,255,.03);
  border: 1px solid rgba(255,255,255,.10);
  border-radius: 12px;
  padding: 1.6rem 1.8rem;
}

/* 팀원 리스트 문단 스타일 */
.cup-team-line {
  color: rgba(255,255,255,.9);
  font-size: 1.05rem;
  line-height: 2.0;          /* 줄 간격 일정하게 */
  margin: 0.2rem 0;
  display: flex;
  align-items: center;
}

/* 이름 부분만 고정 폭으로 정렬 */
.cup-team-name {
  display: inline-block;
  width: 70px;               /* 이름 간격 통일 */
  font-weight: 600;
  color: white;
}

/* 역할 설명 */
.cup-team-role {
  margin-left: .4rem;        /* 이름 뒤 살짝 띄움 */
}
            
/* About Spotify: 카드 톤(이미 사용중) */
.cup-spotify-box{
  background: rgba(255,255,255,.03);
  border: 1px solid rgba(255,255,255,.10);
  border-radius: 12px;
  padding: 1.2rem 1.4rem;
}

/* Streamlit 마크다운 렌더링 구조 강제 타겟팅 */
div[data-testid="stMarkdownContainer"] > p {
  margin-bottom: 0.15rem !important;   /* 제목과 목록 사이 완전 붙이기 */
}

div[data-testid="stMarkdownContainer"] ul {
  margin-top: 0.05rem !important;
  margin-bottom: 0.4rem !important;
  margin-left: 1.1rem !important;
  padding-left: 0 !important;
}

/* 여전히 위쪽 박스 여백 */
.cup-gap-top {
  margin-top: 1.2rem !important;
}
            
.cup-gap-y { height: 1.2rem; }   /* 필요한 만큼 숫자만 조절: .6~1.0rem 추천 */

</style>       
""", unsafe_allow_html=True)

# ================= Sidebar =================
with st.sidebar:
    st.image("Cup_3_copy_4.png", use_container_width=True)
    st.markdown('<hr class="cup-divider">', unsafe_allow_html=True)
    section = st.radio("", ["PROJECT OVERVIEW","DATA EXPLORATION","AARRR DASHBOARD","INSIGHTS & STRATEGY"])
    st.markdown('<hr class="cup-footer-line">', unsafe_allow_html=True)
    st.markdown(
        '<div class="cup-sidebar-footer">'
        '<a href="https://colab.research.google.com/drive/1kmdOCUneO2tjT8NqOd5MvYaxJqiiqb9y?usp=sharing" '
        'target="_blank" class="cup-link-btn">🔗 Open in Google Colab</a><br>'
        '© DATA CUPBOP | Stay or Skip'
        '</div>', unsafe_allow_html=True
    )

# ================= Demo data =================
np.random.seed(42)
dates = pd.date_range("2025-01-01", periods=60, freq="D")
df = pd.DataFrame({
    "date": np.random.choice(dates, 1000),
    "channel": np.random.choice(["SNS","Search","Ad"], 1000, p=[0.45,0.35,0.20]),
    "event": np.random.choice(["visit","signup","first_play","subscribe"], 1000, p=[0.45,0.25,0.20,0.10]),
    "amount": np.random.gamma(2.2, 6.0, 1000).round(2)
})

# ================= Title =================
def img_to_datauri(path: str) -> str:
    with open(path, "rb") as f:
        import base64
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{b64}"

icon_datauri = img_to_datauri("free-icon-play-4604241.png")
st.markdown(f"""
<style>
   .cup-hero {{
    display:inline-flex; align-items:baseline; gap:0;
    margin:-4.5rem 0 .25rem 0;       /* 위로 올리기: -값으로 */
    transform:translateY(-8px);     /* 미세 조정 */
  }}
   .cup-hero h1 {{
    margin:0; line-height:1; font-weight:800; letter-spacing:-.2px;
    transform:translateY(-2px);     /* 글자만 살짝 더 위로 */
  }}
   .cup-hero img {{
    width:3.05em; height:auto; vertical-align:baseline;
    transform:translateY(0.65em); margin-left:-6px !important;
    display:inline-block;
  }}
  [data-testid="stAppViewContainer"] .main .block-container {{
    padding-top:.1rem !important;
  }}
    .cup-subtitle {{
    color: var(--muted);
    font-size: 1.08rem;
    font-weight: 500;
    margin-top: -1.4rem !important;   /* 🔹 위로 살짝 올림 */
    margin-bottom: 1.0rem !important; /* 하단 간격 유지 */
    letter-spacing: .1px;
    }}
</style>
<div class="cup-hero">
  <h1>Stay or Skip</h1><img src="{icon_datauri}" alt="play icon" />
</div>
<p class="cup-subtitle">Streaming Subscription Analysis with AARRR Framework</p>
""", unsafe_allow_html=True)
vgap(36)   # 12~20px 사이에서 취향대로

# ================= Sections =================
if section == "PROJECT OVERVIEW":
    tabs = st.tabs(["Team Intro", "About Spotify", "Background & Objectives", "Dataset"])

    with tabs[0]:
        st.markdown('<div class="cup-h2">Team Introduction</div>', unsafe_allow_html=True)
        tight_top(-36)  # -6 ~ -12px 정도 추천

        # ① 로고 크기: CSS로만 축소 (리샘플링 X → 안 뿌옇게)
        st.markdown("""
        <style>
        .cup-logo{ display:block; margin: -1.2rem 0 2.2rem 0; width:35%; max-width:520px; height:auto; }
        </style>
        """, unsafe_allow_html=True)

        # ② 기존 st.image(...) 대신 Base64 데이터 URI 사용 (앱 위에서 이미 정의한 함수 재사용)
        logo_uri = img_to_datauri("Cup_8_copy_2.png")   # 파일명/경로만 정확히
        st.markdown(f'<img src="{logo_uri}" class="cup-logo" alt="team logo">', unsafe_allow_html=True)

        # ③ 팀 박스는 그대로
        st.markdown("""
        <div class="cup-info-box">
            <p style="font-weight:600;">빠르지만 든든한 데이터 분석, 인사이트 한 스푼으로 완성하는 데이터컵밥 🍚</p>
            <p class="cup-team-line"><span class="cup-team-name">함께</span><span class="cup-team-role">데이터 탐색(EDA) · 핵심 지표 선정 · 시각화 · 인사이트 도출</span></p>
            <p class="cup-team-line"><span class="cup-team-name">천지우</span><span class="cup-team-role">프로젝트 매니징 & 분석 구조 설계</span></p>
            <p class="cup-team-line"><span class="cup-team-name">이유주</span><span class="cup-team-role">데이터 스토리텔링 & 대시보드 디자인</span></p>
            <p class="cup-team-line"><span class="cup-team-name">김채린</span><span class="cup-team-role">데이터 정제 및 파생 변수 설계</span></p>
            <p class="cup-team-line"><span class="cup-team-name">서별</span><span class="cup-team-role">데이터 수집 및 탐색 과정 지원</span></p>
        </div>
        """, unsafe_allow_html=True)


    with tabs[1]:
        st.markdown('<div class="cup-h2">About Spotify</div>', unsafe_allow_html=True)
        tight_top(-36)  # -6 ~ -12px 정도 추천

        # ================= KPI Cards =================
        st.markdown('<div class="kpi-tight">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)  # ← 여기서는 숫자 리스트(스페이서) 쓰지 마세요!
        with c1: st.metric("Monthly Active Users", "696M")
        with c2: st.metric("Premium Subscribers", "276M")
        with c3: st.metric("Markets", "180+")
        st.markdown('</div>', unsafe_allow_html=True)

        # ================= Introduction =================
        st.markdown("""
        <div class="cup-spotify-box" style="margin-bottom:1.0rem;">
        2008년 스웨덴에서 시작된 글로벌 음악 스트리밍 플랫폼<br>
        Freemium(광고 기반 무료) + Premium(유료 구독) 모델 운영<br>
        청취 로그와 오디오 피처(리듬·밝기·에너지 등 음향 특성) 기반 <b>개인화 추천</b> 제공
        </div>
        """, unsafe_allow_html=True)

        # ================= Business Model & Product =================
        # 👇 이 래퍼로 감싸면 위 CSS가 확실히 적용됨
        st.markdown('<div class="cup-compact cup-gap-top">', unsafe_allow_html=True)

        colA, colB = st.columns(2)
        with colA:
            st.markdown("**Business Model**")
            st.markdown("""
        - Freemium (광고 수익) + Premium (월 구독)
        - 주요 지표: 전환률, 리텐션, 청취 시간, 광고 노출/CTR
        """)

            st.markdown('<div class="cup-gap-y"></div>', unsafe_allow_html=True)
            
            st.markdown("**Content Types**")
            st.markdown("- Music • Podcasts • Audiobooks")

        with colB:
            st.markdown("**Product Surfaces**")
            st.markdown("""
            - Mobile / Desktop / Web
            - Spotify Connect (스피커·TV 등 기기 연동)
            """)

            # ✅ Product Surfaces와 Creator Tools 사이 여백
            st.markdown('<div class="cup-gap-y"></div>', unsafe_allow_html=True)

            st.markdown("**Creator Tools**")
            st.markdown("""
            - Spotify for Artists (지역별 청취자, 플레이리스트 유입, 재생 통계 제공)
            """)

        st.markdown('</div>', unsafe_allow_html=True)  # 👈 래퍼 닫기

        # ================= Pricing Model =================
        st.markdown('<div class="cup-h2" style="margin-top:1.0rem;">Pricing Model</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="cup-spotify-box" style="margin-top:.5rem;">
        <b>Freemium</b>: 광고 기반 무료 서비스 (스트리밍 중 광고 삽입)<br>
        <b>Premium</b>: 월 구독제 — 광고 제거, 오프라인 재생, 고음질, 무제한 스킵<br>
        <small>※ 한국 기준 10,900원/월 (2025년 기준)</small>
        </div>
        """, unsafe_allow_html=True)


        # ================= Caption =================
        st.caption("*Spotify 공식 회사 정보 기준 요약")

    with tabs[2]:
        # 섹션 제목
        st.markdown('<div class="cup-h2">Background & Objectives</div>', unsafe_allow_html=True)
        tight_top(-36)  # -6 ~ -12px 정도 추천

        # 3열 인포그래픽 카드
        # 🎨 Hover 스타일 CSS
        st.markdown("""
        <style>
        .cup-hover-card {
        transition: all .25s ease;
        background: rgba(255,255,255,.03);
        border: 1px solid rgba(255,255,255,.10);
        border-radius: 12px;
        padding: 1.6rem 1.8rem;
        }
        .cup-hover-card:hover {
        background: rgba(255,255,255,.08);
        border-color: rgba(255,255,255,.18);
        transform: translateY(-4px);
        box-shadow: 0 0 15px rgba(29,185,84,.25);
        }
        </style>
        """, unsafe_allow_html=True)

        # 🧭 Background & Objectives 카드
        st.markdown("""
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem;">

        <div class="cup-hover-card" style="text-align:center;">
            <p style="font-size:1.5rem;">📈</p>
            <p style="font-weight:800;font-size:1.1rem;margin-bottom:1rem;">스트리밍 시장 성장과 도전</p>
            <p style="color:rgba(255,255,255,.9);font-size:1.05rem;line-height:1.85;">
            글로벌 시장 급성장, 유입률↑ 이탈률↑<br>
            높은 경쟁 속 체험 후 구독 전환율 하락<br>
            콘텐츠 피로도·사용자 유지가 핵심 과제로 부상
            </p>
        </div>

        <div class="cup-hover-card" style="text-align:center;">
            <p style="font-size:1.5rem;">🎧</p>
            <p style="font-weight:800;font-size:1.1rem;margin-bottom:1rem;">Spotify의 강점</p>
            <p style="color:rgba(255,255,255,.9);font-size:1.05rem;line-height:1.85;">
            세계 최대 규모 청취 로그 및 오디오 피처 데이터 보유<br>
            유저 행동 여정·이탈 패턴 분석에 최적화된 플랫폼
            </p>
        </div>

        <div class="cup-hover-card" style="text-align:center;">
            <p style="font-size:1.5rem;">🧭</p>
            <p style="font-weight:800;font-size:1.1rem;margin-bottom:1rem;">AARRR 기반 분석 방향</p>
            <p style="color:rgba(255,255,255,.9);font-size:1.05rem;line-height:1.85;">
            Acquisition → Retention → Revenue<br>
            단계별 핵심 지표 정의<br>
            데이터 기반 리텐션·LTV 개선 전략 제안
            </p>
        </div>

        </div>
        """, unsafe_allow_html=True)

        with tabs[3]:
            # =========================
            # 🎧 Dataset Overview
            # =========================
            st.markdown('<div class="cup-h2">Dataset Overview</div>', unsafe_allow_html=True)
            tight_top(-36)

            st.markdown("""
            <div class="cup-card">
            <b>데이터셋명</b>: Spotify User Behavior + Revenue Dataset — 2023.01–06<br>
            <b>규모</b>: 3,120행 (6개월 × 520명), 24개 컬럼<br>
            <b>주요 컬럼</b>: userid, month, revenue, subscription_plan, timestamp, fav_music_genre 등<br>
            <b>출처</b>: Kaggle Spotify User Behavior Dataset + 강사 제공 매출지표
            </div>
            """, unsafe_allow_html=True)

            tidy = pd.read_excel("spotify_merged.xlsx")

            # =========================
            # 📂 Dataset Preview
            # =========================
            st.markdown("""
            #### 📂 Dataset Preview  
            <span style="font-size:0.9rem; color:#888;">데이터 상위 5행 미리보기</span>
            """, unsafe_allow_html=True)
            st.dataframe(tidy.head(5))

            # =========================
            # 💹 Monthly Revenue Trend
            # =========================
            st.markdown("""
            #### 💹 Monthly Revenue Trend  
            <span style="font-size:0.9rem; color:#888;">월별 매출 추이</span>
            """, unsafe_allow_html=True)

            import matplotlib.pyplot as plt
            from matplotlib.ticker import FuncFormatter
            plt.rcParams.update({
                "axes.titlesize": 14, "axes.labelsize": 11,
                "xtick.labelsize": 10, "ytick.labelsize": 10
            })

            monthly = tidy.groupby("month")["revenue"].sum().reset_index()
            fmt_million_krw = FuncFormatter(lambda x, pos: f"₩{x/1_000_000:,.0f}M")

            fig_tr, ax_tr = plt.subplots(figsize=(6.5, 3.6))
            ax_tr.plot(monthly["month"], monthly["revenue"], marker="o", linewidth=2.5, color="#1DB954")
            ax_tr.set_xlabel("Month")
            ax_tr.set_ylabel("Revenue (₩, 백만원 단위)")
            ax_tr.yaxis.set_major_formatter(fmt_million_krw)
            ax_tr.grid(alpha=0.2)
            plt.tight_layout()
            st.pyplot(fig_tr, use_container_width=True)

            # =========================
            # 📊 Plan Comparison Overview
            # =========================
            st.markdown("""
            #### 📊 Plan Comparison Overview  
            <span style="font-size:0.9rem; color:#888;">요금제별 매출·이용자 비중 비교</span>
            """, unsafe_allow_html=True)

            col_left, col_right = st.columns(2, gap="medium")

            # 왼쪽: Revenue Share (도넛)
            with col_left:
                plan_rev = tidy.groupby("subscription_plan")["revenue"].sum().reset_index()
                order = ["Free (ad-supported)", "Premium (paid subscription)"]
                plan_rev["subscription_plan"] = pd.Categorical(plan_rev["subscription_plan"], order, True)
                plan_rev = plan_rev.sort_values("subscription_plan")

                fig_rs, ax_rs = plt.subplots(figsize=(5, 3.6))
                pie_out = ax_rs.pie(
                    plan_rev["revenue"],
                    labels=None,
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=["#BFBFBF", "#1DB954"],
                    pctdistance=0.75,
                    wedgeprops=dict(width=0.35)
                )
                # 버전 호환 언패킹
                if len(pie_out) == 3:
                    wedges, texts, autotexts = pie_out
                else:
                    wedges, texts = pie_out
                    autotexts = []

                ax_rs.set_title("Revenue (₩) Share", pad=6)
                ax_rs.legend(
                    wedges,
                    plan_rev["subscription_plan"],
                    loc="lower center", bbox_to_anchor=(0.5, -0.15),
                    ncol=2, frameon=False
                )
                plt.tight_layout()
                st.pyplot(fig_rs, clear_figure=True, use_container_width=True)

            # 오른쪽: Active User Plan Mix (막대)
            with col_right:
                latest = tidy["month"].max()
                users_mix = (
                    tidy[tidy["month"] == latest]
                    .groupby("subscription_plan")["userid"].nunique()
                    .reset_index(name="users")
                    .sort_values("users", ascending=False)
                )

                fig_um, ax_um = plt.subplots(figsize=(5, 3.6))
                colors = ["#1DB954" if "Premium" in x else "#BFBFBF" for x in users_mix["subscription_plan"]]
                ax_um.bar(users_mix["subscription_plan"], users_mix["users"], color=colors)
                ax_um.set_ylabel("Users (Unique)")
                ax_um.set_title(f"Active Users by Plan — {latest}")
                ymax = max(users_mix["users"]) * 1.15
                ax_um.set_ylim(0, ymax)
                for i, v in enumerate(users_mix["users"]):
                    ax_um.text(i, v, f"{int(v):,}", ha="center", va="bottom", fontsize=10)
                plt.tight_layout()
                st.pyplot(fig_um, clear_figure=True, use_container_width=True)

            # =========================
            # 🧹 Data Quality Check
            # =========================
            st.markdown("""
            #### 🧹 Data Quality Check  
            <span style="font-size:0.9rem; color:#888;">데이터 정합성 및 결측치 현황</span>
            """, unsafe_allow_html=True)

            # 1️⃣ 설명 박스
            st.markdown("""
            <div class="cup-card">
            - 병합 기준: <b>userid</b> (매출 ⟷ 원본 설문)<br>
            - 기간/규모: <b>2023-01 ~ 2023-06</b>, <b>3,120행</b> (6개월 × 520명)<br>
            - 매출 기준: <b>Premium만 유료매출</b> (Free=0원)
            </div>
            """, unsafe_allow_html=True)

            # 2️⃣ 그래프 (결측 상위 5개)
            na = tidy.isna().sum().sort_values(ascending=False)
            na_top = na[na > 0].head(5).reset_index()
            na_top.columns = ["column", "na_cnt"]

            fig_na, ax_na = plt.subplots(figsize=(10, 3.6))
            if len(na_top) > 0:
                ax_na.barh(na_top["column"], na_top["na_cnt"], color="#BFBFBF")
                ax_na.invert_yaxis()
                ax_na.set_xlabel("Missing Values")
                ax_na.set_title("Top Missing Columns", pad=6)
                xmax = max(na_top["na_cnt"]) * 1.15
                ax_na.set_xlim(0, xmax)
                for i, v in enumerate(na_top["na_cnt"]):
                    ax_na.text(v, i, f" {int(v):,}", va="center")
            else:
                ax_na.axis("off")
                ax_na.text(0.5, 0.5, "결측치 없음", ha="center", va="center")
            plt.tight_layout()
            st.pyplot(fig_na, clear_figure=True, use_container_width=True)

            # 3️⃣ 결론 박스
            st.markdown(f"""
            <div class="cup-card">
            ✅ <b>정합성 요약</b><br>
            - 중복 행: <b>0</b> · 조인 누락: <b>없음</b> (both = 3120)<br>
            - 사용자 수: <b>{tidy['userid'].nunique():,}</b>명 · 기간: <b>{tidy['month'].min()} ~ {tidy['month'].max()}</b><br>
            - 분석 가능 상태: <b>양호</b>
            </div>
            """, unsafe_allow_html=True)

            st.success("✅ 데이터 병합 및 품질 검증 완료 — 분석에 활용 가능합니다.")



elif section == "DATA EXPLORATION":
    tabs = st.tabs(["Cleaning", "EDA", "Metrics Definition"])

    with tabs[0]:
        st.markdown('<div class="cup-h2">Data Cleaning & Preprocessing</div>', unsafe_allow_html=True)
        tight_top(-36)  # -6 ~ -12px 정도 추천
        st.markdown('<div class="cup-card">결측/이상치 처리, 타입 정규화, 세션 집계, 파생변수 생성 기준을 명시합니다.</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="cup-h2">Exploratory Data Analysis (EDA)</div>', unsafe_allow_html=True)
        tight_top(-36)  # -6 ~ -12px 정도 추천
        st.markdown('<div class="cup-card">채널별 유입 분포, 활동량 분포, 이탈 여부에 따른 차이를 탐색합니다.</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="cup-h2">AARRR Metrics Definition</div>', unsafe_allow_html=True)
        tight_top(-36)  # -6 ~ -12px 정도 추천
        st.markdown("""
| Stage | Metric (예시) | 계산 개념 |
|---|---|---|
| Acquisition | 신규 유저 수 | 특정 기간 내 최초 가입 수 |
| Activation | 첫 재생 완료율 | first_play / signup |
| Retention | N-day 유지율 | 기준일 대비 N일 후 복귀 비율 |
| Revenue | ARPU/LTV | 매출 / 활성 사용자 수, 누적 기여 |
| Referral | 초대/공유율 | 공유 건수 / 활성 사용자 수 |
""")

elif section == "AARRR DASHBOARD":
    st.markdown('<div class="cup-h2">Visual Analytics Dashboard</div>', unsafe_allow_html=True)
    tight_top(-36)  # -6 ~ -12px 정도 추천
    tabs = st.tabs(["Funnel", "Retention", "Cohort", "LTV"])

    with tabs[0]:
        st.subheader("Funnel Analysis")
        st.caption("가입 → 첫 재생 → 구독 전환율을 단계별로 비교합니다.")
        steps = ["visit","signup","first_play","subscribe"]
        counts = [df.query("event==@s").shape[0] for s in steps]
        conv = [100] + [round(counts[i]/counts[i-1]*100,1) if counts[i-1] else 0 for i in range(1,len(steps))]
        fig, ax = plt.subplots(figsize=(6,3))
        ax.plot(steps, conv, marker="o", color="#1DB954")   # brand green
        ax.set_ylim(0,105); ax.set_ylabel("Conversion %", color="#CFE3D8")
        ax.set_facecolor("#191414"); fig.set_facecolor("#121212")
        ax.tick_params(colors="#CFE3D8")
        st.pyplot(fig, use_container_width=True)

    with tabs[1]:
        st.subheader("Retention Analysis")
        st.caption("N-Day/Weekly 커브 예시 (실데이터로 교체 권장).")
        daily = df.groupby("date")["event"].count().sort_index()
        roll = (daily.rolling(7).mean() / (daily.rolling(7).max()+1e-9) * 100).fillna(0)
        fig, ax = plt.subplots(figsize=(6,3))
        ax.plot(roll.index, roll.values, color="#80DEEA")   # cyan sky for 대비
        ax.set_ylabel("Retention-like %", color="#CFE3D8"); ax.set_xlabel("date", color="#CFE3D8")
        ax.set_facecolor("#191414"); fig.set_facecolor("#121212")
        ax.tick_params(colors="#CFE3D8")
        st.pyplot(fig, use_container_width=True)

    with tabs[2]:
        st.subheader("Cohort Analysis")
        st.info("가입월 × 경과주 코호트 유지율 히트맵(추가 예정).")

    with tabs[3]:
        st.subheader("LTV Analysis")
        last30 = df[df["date"] >= (df["date"].max() - pd.Timedelta(days=30))]
        rev = last30["amount"].sum()
        active = max(int(last30["event"].nunique()*100), 1)  # demo only
        arpu = rev / active
        c1, c2 = st.columns(2)
        c1.metric("총 수익(30일, 예시)", f"${rev:,.0f}")
        c2.metric("ARPU(30일, 예시)", f"${arpu:,.2f}")

    st.caption("※ Assumptions: 관찰기간=30일, 환불/부가세 제외, 할인율 0%, 예시 값")


else:
    tabs = st.tabs(["Insights", "Strategy", "Next Steps"])

    with tabs[0]:
        st.markdown('<div class="cup-h2">Key Insights by AARRR Stage</div>', unsafe_allow_html=True)
        tight_top(-36)  # -6 ~ -12px 정도 추천
        st.markdown("""
        <div class="cup-card">
          • Activation: 첫 재생 구간 이탈 높음 → 온보딩·첫 추천 큐레이션 개선<br>
          • Retention: 7일 복귀율 급락 → 리마인드/추천 콘텐츠 자동화<br>
          • Revenue: 상위 사용자 매출 편중 → VIP 업셀링·연간 플랜 제안
        </div>
        """, unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="cup-h2">Data-driven Strategy Proposal</div>', unsafe_allow_html=True)
        tight_top(-36)  # -6 ~ -12px 정도 추천
        st.markdown("""
        <div class="cup-card">
          ① 온보딩 개선(튜토리얼 간소화, 첫 추천 강화)<br>
          ② 휴면 징후 타깃 푸시/이메일 자동화<br>
          ③ VIP 세그먼트 리워드/장기 구독 유도 캠페인<br>
          ④ 추천·공유 인센티브 단순화
        </div>
        """, unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="cup-h2">Limitations & Next Steps</div>', unsafe_allow_html=True)
        tight_top(-36)  # -6 ~ -12px 정도 추천
        st.markdown("""
        <div class="cup-card">
          관찰 기간·외생 변수 제한 → 외부 데이터 결합 및 예측모델(이탈 예측·LTV 추정) 확장
        </div>
        """, unsafe_allow_html=True)