try:
	import streamlit as st
except Exception:
	# streamlit not installed — provide a minimal stub so the file can be opened/checked
	class _StubSidebar:
		@staticmethod
		def header(*args, **kwargs): pass
		@staticmethod
		def selectbox(label, options, *args, **kwargs):
			return options[0] if options else None
		@staticmethod
		def radio(label, options, *args, **kwargs):
			return options[0] if options else None

	class _Stub:
		sidebar = _StubSidebar()
		def set_page_config(self, *args, **kwargs): pass
		def title(self, *args, **kwargs): pass
		def subheader(self, *args, **kwargs): pass
		def write(self, *args, **kwargs): pass
		def info(self, *args, **kwargs): pass

	st = _Stub()

st.set_page_config(page_title="FinAnalytics", layout="wide")
st.title("FinAnalytics Dashboard")

st.sidebar.header("Controls")
ticker = st.sidebar.selectbox("Select stock", ["AAPL", "MSFT", "NVDA"])
horizon = st.sidebar.radio("Horizon", ["Short", "Mid", "Long"], horizontal=True)

st.subheader("Selection")
st.write({"ticker": ticker, "horizon": horizon})

st.info("Next: load data + run 3 models + show charts + export PDF.")
