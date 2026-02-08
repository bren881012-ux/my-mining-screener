import streamlit as st
import pandas as pd
import yfinance as yf

# 1. PAGE SETUP
st.set_page_config(page_title="Venture Scout 2026", page_icon="⛏️", layout="wide")

st.title("⛏️ Venture Mining Scout")
st.markdown("---")

# 2. TICKER INPUT
# Note: For TSX Venture, always add '.V' to the ticker symbol.
ticker_input = st.sidebar.text_input("Enter Ticker (e.g., FUU.V):", "FUU.V")

if st.sidebar.button("Analyze Stock"):
    try:
        # 3. FETCH DATA FROM YAHOO FINANCE
        stock = yf.Ticker(ticker_input)
        info = stock.info
        
        # 4. KEY METRIC CARDS
        st.subheader(f"📊 Market Stats: {info.get('longName', ticker_input)}")
        col1, col2, col3, col4 = st.columns(4)
        
        # Cash-to-Burn Calculation (Simplified)
        cash = info.get('totalCash', 0)
        shares = info.get('sharesOutstanding', 0)
        mkt_cap = info.get('marketCap', 0)
        
        col1.metric("Cash (Est)", f"${cash:,}" if cash else "N/A")
        col2.metric("Shares Out", f"{shares/1e6:.1f}M" if shares else "N/A")
        col3.metric("Market Cap", f"${mkt_cap:,}" if mkt_cap else "N/A")
        col4.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")

        # 5. THE VENTURE SCREENER (YOUR BRAIN BANK CRITERIA)
        st.markdown("### 📋 Screener Quick-Score")
        
        # Scoring Logic based on your specific rules
        score = 0
        checks = []
        
        # Cap Structure Check
        if shares and shares < 100e6:
            score += 2
            checks.append("✅ Cap Structure: Tight (<100M shares)")
        else:
            checks.append("⚠️ Cap Structure: High dilution/share count")

        # Cash Check
        if cash and cash > 5e6:
            score += 2
            checks.append("✅ Cash: Sufficient for exploration (>12mo runway)")
        else:
            checks.append("❌ Cash: Low/Unknown (Dilution Risk High)")

        # Result Output
        st.write("\n".join(checks))
        st.progress(score / 10)
        st.write(f"**Venture Score:** {score}/10")

        # 6. PRICE CHART
        st.subheader("📈 Price Action (Lassonde Curve Check)")
        hist = stock.history(period="1y")
        st.line_chart(hist['Close'])

    except Exception as e:
        st.error(f"Error: Could not find data for {ticker_input}. Make sure to include '.V' for Venture stocks.")
