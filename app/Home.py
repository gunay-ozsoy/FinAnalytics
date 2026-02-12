import streamlit as st

st.set_page_config(page_title="FinAnalytics", layout="wide")
st.title("FinAnalytics Dashboard")

st.sidebar.header("Controls")
ticker = st.sidebar.selectbox("Select stock", ["AAPL", "MSFT", "NVDA"])
horizon = st.sidebar.radio("Horizon", ["Short", "Mid", "Long"], horizontal=True)

st.subheader("Selection")
st.write({"ticker": ticker, "horizon": horizon})

st.info("Next: load data + run 3 models + show charts + export PDF.")
