import re
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from src.integrations.marketaux import get_ticker_and_industry_news


TICKERS = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Conagra Brands": "CAG.US",
    "Hershey": "HSY.US",
    "Coca-Cola Europacific Partners": "CCEP.US",
    "Kroger": "KR.US",
    "Sysco": "SYY.US",
    "Campbell Soup Company": "CPB.US",
    "Keurig Dr Pepper": "KDP.US",
    "PepsiCo": "PEP.US",
    "Tyson Foods": "TSN.US",
    "JM Smucker": "SJM.US",
    "Kraft Heinz": "KHC.US",
    "Philip Morris International": "PM.US",
    "Altria": "MO.US",
    "Hormel Foods": "HRL.US",
    "Estée Lauder": "EL.US",
    "Colgate-Palmolive": "CL.US",
    "Kellogg": "K.US",
    "General Mills": "GIS.US",
    "Kimberly-Clark": "KMB.US",
    "Clorox": "CLX.US",
    "McCormick & Company": "MKC.US",
    "Coca-Cola": "KO.US",
    "Walmart": "WMT.US",
    "Costco": "COST.US",
    "Dollar General": "DG.US",
    "Dollar Tree": "DLTR.US",
    "Walgreens Boots Alliance": "WBA.US",
    "Monster Beverage": "MNST.US",
    "Constellation Brands": "STZ.US",
    "Mondelez International": "MDLZ.US",
    "Molson Coors": "TAP.US",
    "Lamb Weston": "LW.US",
    "Church & Dwight": "CHD.US",
    "Brown-Forman": "BF.B.US",
}

LOGO_DIR = Path(__file__).resolve().parent / "assets" / "logos"


def ticker_to_logo_filename(ticker: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9]+", "_", ticker).strip("_")
    return f"{safe}.png"


def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


@st.cache_data
def generate_dummy_price_series(ticker: str) -> pd.DataFrame:
    np.random.seed(hash(ticker) % 2**32)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=60)
    prices = np.cumsum(np.random.randn(len(dates)) * 0.5 + 0.2) + 100
    return pd.DataFrame({"Tarih": dates, "Fiyat": prices})


@st.cache_data
def run_dummy_models(ticker: str) -> dict:
    np.random.seed((hash(ticker) + 1337) % 2**32)
    metrics = {
        "expected_return": float(np.round(np.random.uniform(-5, 10), 2)),
        "volatility": float(np.round(np.random.uniform(2, 8), 2)),
        "confidence": float(np.round(np.random.uniform(50, 100), 2)),
    }
    scenario = pd.DataFrame({
        "Senaryo": ["Ayı", "Baz", "Boğa"],
        "Getiri (%)": np.random.uniform(-15, 25, size=3).round(2)
    })
    return {"metrics": metrics, "scenario": scenario}


@st.cache_data
def dummy_news_summaries(ticker: str) -> list[str]:
    np.random.seed((hash(ticker) + 42) % 2**32)
    eylemler = ["beklentiyi aştı", "beklentinin altında kaldı", "yönlendirme paylaştı", "duyurdu", "genişledi"]
    konular = ["finansal sonuçlar", "marj görünümü", "maliyet optimizasyonu", "yeni ürün hattı", "bölgesel büyüme"]
    haberler = []
    for i in range(5):
        e = np.random.choice(eylemler)
        k = np.random.choice(konular)
        haberler.append(f"{ticker} sahte haber {i+1}: Şirket {k} konusunda {e}.")
    return haberler


@st.cache_data
def dummy_sector_summary(ticker: str) -> str:
    np.random.seed((hash(ticker) + 7) % 2**32)
    sektorler = ["Temel Tüketim", "İhtiyari Tüketim", "Sağlık", "Sanayi"]
    tonlar = ["istikrarlı", "karma", "hafif pozitif", "hafif negatif"]
    return f"Sektör özeti (sahte): {np.random.choice(sektorler)} tarafında kısa vadeli sinyaller {np.random.choice(tonlar)}."


@st.cache_data
def compute_dummy_score(news: list[str], sector_summary: str) -> tuple[int, str]:
    s = sum(len(n) for n in news) + len(sector_summary)
    score = int(s % 101)
    etiket = "Pozitif" if score > 60 else "Nötr" if score > 40 else "Negatif"
    return score, etiket


@st.cache_data
def dummy_ticker_about(ticker: str) -> str:
    np.random.seed((hash(ticker) + 2026) % 2**32)
    profiller = [
        "istikrarlı nakit akışı üreten defansif bir şirket",
        "fiyatlama gücü dinamikleri olan olgun bir marka portföyü",
        "marj hassasiyeti yüksek, dağıtım odaklı bir operasyon",
        "kur riskine açık, global ölçekte tüketiciye dönük bir yapı",
        "mevsimsellik etkileri bulunan, talep dayanıklılığı yüksek bir şirket",
    ]
    riskler = [
        "girdi maliyeti oynaklığı", "kur dalgalanmaları", "rekabetçi fiyat baskısı",
        "dağıtım kısıtları", "regülasyon kaynaklı gündem riski"
    ]
    katalizorler = [
        "yönlendirme güncellemeleri", "beklenti üstü finansal sonuçlar", "fiyatlama aksiyonları",
        "maliyet azaltım programları", "kategori büyümesinde hızlanma"
    ]

    p = np.random.choice(profiller)
    r1, r2 = np.random.choice(riskler, size=2, replace=False)
    c1, c2 = np.random.choice(katalizorler, size=2, replace=False)

    return (
        f"{ticker} (sahte profil) bu şablonda {p} olarak kurgulanmıştır.\n\n"
        f"İzlenmesi gerekenler (sahte): {r1}, {r2}.\n\n"
        f"Olası katalizörler (sahte): {c1}, {c2}.\n\n"
        "TODO: Bu alanı gerçek şirket/sektör açıklaması, temel veriler ve model yorumlarıyla değiştir."
    )


def render_logo_or_placeholder(ticker: str) -> None:
    logo_path = LOGO_DIR / ticker_to_logo_filename(ticker)

    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
        return

    st.markdown(
        """
        <div style="
            width: 100%;
            aspect-ratio: 16/10;
            border: 2px dashed rgba(255,255,255,0.25);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: rgba(255,255,255,0.55);
            font-size: 12px;
        ">
            Logo (PNG) eklenecek
        </div>
        """,
        unsafe_allow_html=True
    )


@st.cache_data(ttl=600)
def fetch_marketaux_news(selected_ticker: str) -> dict:
    return get_ticker_and_industry_news(selected_ticker, country="us", n=10, per_req=3)


def render_news_block(prefix: str, idx: int, it: dict) -> None:
    title = (it.get("title") or "").strip()
    published_at = (it.get("published_at") or "").strip()
    source = (it.get("source") or "").strip()
    desc = (it.get("description") or "").strip()
    snippet = (it.get("snippet") or "").strip()
    url = (it.get("url") or "").strip()

    st.write(f"{prefix} {idx}. {title}")
    if published_at or source:
        st.write(f"{published_at} | {source}".strip(" |"))
    if desc:
        st.write(desc)
    if snippet:
        st.write(snippet)
    if url:
        st.write(url)


st.set_page_config(page_title="FinAnalytics", layout="wide")
st.title("FinAnalytics Dashboard")

st.sidebar.header("Kontroller")

selected_label = st.sidebar.selectbox("Hisse seçin", [""] + list(TICKERS.keys()))
selected_ticker = TICKERS.get(selected_label, "")

email = st.sidebar.text_input(
    "E-posta (raporlar için) — Mailiniz tarafınıza düzenli olarak rapor gönderilmesi için istenmektedir.",
    key="email_input"
)

if st.sidebar.button("E-postayı Kaydet"):
    if email and is_valid_email(email):
        st.session_state["saved_email"] = email
        st.sidebar.success("E-posta kaydedildi.")
    else:
        st.sidebar.error("Geçersiz e-posta formatı.")

saved_email = st.session_state.get("saved_email", "")

if not selected_ticker:
    st.write(
        "FinAnalytics, seçilen hisse için kısa/orta/uzun vadeli model çıktıları, "
        "LLM tabanlı haber ve sektör özetleri ile e-posta üzerinden raporlama akışlarını "
        "sunmayı hedefleyen bir Streamlit dashboard şablonudur. "
        "Dashboard bölümlerini açmak için soldan bir hisse seçin."
    )
    st.stop()

left, right = st.columns([5, 1.5], vertical_alignment="center")
with left:
    st.markdown(f"## {selected_label} ({selected_ticker})")
with right:
    render_logo_or_placeholder(selected_ticker)

tabs = st.tabs(["Hakkında", "Model Çıktıları", "Haber & Sektör", "Raporlar"])

with tabs[0]:
    st.header("Hakkında")
    st.write(dummy_ticker_about(selected_ticker))

with tabs[1]:
    st.header("Model Çıktıları (Sahte)")

    results = run_dummy_models(selected_ticker)
    metrics = results["metrics"]
    scenario = results["scenario"]

    news_list = dummy_news_summaries(selected_ticker)
    sector_s = dummy_sector_summary(selected_ticker)
    score, sentiment = compute_dummy_score(news_list, sector_s)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Beklenen Getiri", f"{metrics['expected_return']}%")
    c2.metric("Volatilite", f"{metrics['volatility']}%")
    c3.metric("Güven", f"{metrics['confidence']}%")
    c4.metric("Bileşik Skor", score, sentiment)

    df_prices = generate_dummy_price_series(selected_ticker)
    fig = px.line(df_prices, x="Tarih", y="Fiyat", title=f"{selected_ticker} Fiyat (Sahte)")
    st.plotly_chart(fig, use_container_width=True)

    st.write("Senaryo Çıktıları")
    st.dataframe(scenario, use_container_width=True)

with tabs[2]:
    st.header("Haber & Sektör")

    use_marketaux = st.toggle("Marketaux ile gerçek haberleri çek", value=True)

    if use_marketaux:
        try:
            with st.spinner("Marketaux haberleri çekiliyor..."):
                result = fetch_marketaux_news(selected_ticker)

            st.caption(f"Symbol: {result['symbol']} | Industry: {result['industry']}")

            st.subheader("Ticker Haberleri (Son 10)")
            for i, it in enumerate(result["ticker_news"], start=1):
                render_news_block("Ticker", i, it)
                st.write("---")

            st.subheader("Industry Haberleri (Son 10)")
            for i, it in enumerate(result["industry_news"], start=1):
                render_news_block("Industry", i, it)
                st.write("---")

        except Exception as e:
            st.error(f"Marketaux hata: {e}")
            st.info("Kontrol: set -a && source .env && set +a (MARKETAUX_API_TOKEN yüklü mü?)")
    else:
        st.info("Gerçek haberleri görmek için toggle'ı aç.")

with tabs[3]:
    st.header("Rapor Yönetimi")

    st.write("Kayıtlı e-posta:")
    st.write(saved_email if saved_email else "Kayıtlı e-posta yok.")

    if st.button("Test Raporu Gönder"):
        st.success("Test raporu gönderildi (sahte).")

    st.write("Rapor planla (sahte):")
    st.date_input("Rapor Tarihi")
