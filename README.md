# Black-Scholes Options Pricing Dashboard 
An interactive Streamlit dashboard that visualizes European call and put option prices under the Black-Scholes model. Users can tweak key inputs (spot price, strike, volatility, risk-free rate, time to maturity) and immediately see pricing heatmaps and P/L surfaces :contentReference[oaicite:0]{index=0}.

[🔗 Live Website](https://tleblackschole.streamlit.app)


## About the Project
I built this project to deepen my understanding of quantitative finance, Python-based modeling, and interactive data visualization. It combines theoretical finance with practical tools—allowing users to tweak key variables and immediately visualize their impact on option prices.

## Tech Stack
- **Dashboard:** Streamlit (`app.py`)  
- **Pricing Logic:** `BSfunctions.py` implements the Black-Scholes formula  
- **Market Data:** Fetched via yfinance library, imlplemented Alpha Vantage API for future expansion. 
- **Database:** MariaDB/MySQL via `database.py`  
- **ETL:** `producer.py` for scheduled writes into the DB  *(pending)*
- **Visuals:** matplotlib (heatmaps) & Plotly (optional 3D surfaces)  

---

