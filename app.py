from BSfunctions import BlackScholes
#from producer import StockProducer
#from keys import alpha_vantage_api_key
from stockScraper import StockScraper
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from numpy import log, sqrt, exp 
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


# Title of the app
st.set_page_config(
    page_title="Tyle|Black-Scholes Option Pricing Model",
    page_icon="😹",
    layout="wide",
    initial_sidebar_state="expanded")
    # Heat Map Function

# Custom CSS for styling the CALL and PUT values
st.markdown("""
<style>
/* Adjust the size and alignment of the CALL and PUT value containers */
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px; /* Adjust the padding to control height */
    width: auto; /* Auto width for responsiveness, or set a fixed width if necessary */
    margin: 0 auto; /* Center the container */
}

/* Custom classes for CALL and PUT values */
.metric-call {
    background-color: #90ee90; /* Light green background */
    color: black; /* Black font color */
    margin-right: 10px; /* Spacing between CALL and PUT */
    border-radius: 10px; /* Rounded corners */
}

.metric-put {
    background-color: #ffcccb; /* Light red background */
    color: black; /* Black font color */
    border-radius: 10px; /* Rounded corners */
}

/* Style for the value text */
.metric-value {
    font-size: 1.5rem; /* Adjust font size */
    font-weight: bold;
    margin: 0; /* Remove default margins */
}

/* Style for the label text */
.metric-label {
    font-size: 1rem; /* Adjust font size */
    margin-bottom: 4px; /* Spacing between label and value */
}

</style>
""", unsafe_allow_html=True)

# BS Default Values
C_buy = 0.0
P_buy = 0.0 
current_price = 100.0
strike = 100.0
time_to_maturity = 1.0
volatility = 0.2
interest_rate = 0.0
call_price = 0.0
put_price = 0.0
# Create an instance of the BlackScholes class with default values
bs_model = BlackScholes(
                time_to_maturity = time_to_maturity,
                strike = strike,
                current_price = current_price,
                volatility = volatility,
                interest_rate = interest_rate,
                C_buy = C_buy,
                P_buy = P_buy,
                call_price = call_price,
                put_price = put_price)

# Sidebar for User Inputs
with st.sidebar:
    st.title("Black-Scholes Dashboard")
    linkedin_url = "linkedin.com/in/tylerle-uf"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Le, Tyler`</a>', unsafe_allow_html=True)

    st.markdown("-----")
        
    manualInput = st.toggle("Stock Ticker Input", value=True)
    if manualInput:
        
        st.header("Real-time Data Inputs")

        ticker_symbol = st.text_input("Stock Ticker", placeholder="e.g., AAPL, TSLA, BTC-USD")
        producer = StockScraper(ticker_symbol)


        # Strike Price - Prompt user (enabled only if price is available)
        strike = st.number_input(
            "Strike Price",
            min_value=0.0,
            value= 100.0,
            disabled=(current_price is None)
        )

        # Time to Expiry - Date picker (enabled only if price is available)
        expiry_date = st.date_input(
            "Time to Expiry",
            value=datetime.date.today(),
            disabled=(current_price is None)
        )
        time_to_expiry = producer.calculate_time_to_maturity(str(expiry_date)) if current_price else 1.0

        # Volatility - Historical volatility (enabled only if price is available)
        volatility = st.number_input("Volatility",   min_value=0.0, value=0.2)

        # Interest Rate
        interest_rate = st.number_input("Risk-free Interest Rate", value=0.05, step=0.01)

        

        # Placeholder for real-time data retrieval w/ stock ticker input
    else:
        current_price     = st.number_input("Current/Underlying Price (S)", min_value=0.0, value=100.0)
        strike     = st.number_input("Strike Price", min_value = 0.0, value=100.0)
        time_to_expiry     = st.number_input("Time to Expiry", min_value=0.0, value=1.0)
        volatility = st.number_input("Volatility",   min_value=0.0, value=0.2)
        interest_rate     = st.number_input("Risk-free Interest Rate", value=0.05)

    # Calculate Call and Put Values
    callput_button = st.button("Calculate")
    
        
    st.markdown("-----")
    st.header("Heatmap Parameters")
        # Toggle for P&L Graph
    PL_toggle_on = st.toggle("P/L Graph", value=False)
        # Utilize real time data (pending)
    if PL_toggle_on:
            C_buy = st.sidebar.number_input("Purchase Price of Call", min_value=0.0, value=5.0, step=0.1)
            P_buy = st.sidebar.number_input("Purchase Price of Put",  min_value=0.0, value=3.0, step=0.1)

        
    # calculate_btn = st.button('Heatmap Parameters')
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price*0.8, step=0.01, )
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price*1.2, step=0.01,)
    vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*0.5, step=0.01,)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*1.5, step=0.01,)
        
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)


# Main Page for Output

st.title("Black-Scholes Pricing Model")
if callput_button:
    if ticker_symbol:
        try:
            current_price = producer.get_spot_price()
            if current_price is None or np.isnan(current_price):
                error_msg = "Could not fetch price for this ticker."
        except Exception as e:
                error_msg = f"Error fetching price: {e}"
                print(error_msg)
                
    bs_model = BlackScholes(
                time_to_maturity = time_to_maturity,
                strike = strike,
                current_price = current_price,
                volatility = volatility,
                interest_rate = interest_rate,
                C_buy = C_buy,
                P_buy = P_buy,
                call_price = call_price,
                put_price = put_price)


# Table of Inputs
input_data = {
    "Current Asset Price": [current_price],
    "Strike Price": [strike],
    "Time to Maturity (Years)": [time_to_maturity],
    "Volatility (σ)": [volatility],
    "Risk-Free Interest Rate": [interest_rate],
}
input_df = pd.DataFrame(input_data)
st.table(input_df)

call_price, put_price = bs_model.calculate_prices()

# Display Call and Put Prices

col1, col2 = st.columns([1,1])

with col1:
    # Using the custom class for CALL value
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Value</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Using the custom class for PUT value
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Value</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("")

    # Generate Heatmap
if PL_toggle_on:
    callpnl_heatmap_fig = bs_model.call_pnl_heatmap()
    putpnl_heatmap_fig = bs_model.put_pnl_heatmap()

    pnl_3d_intsurface_fig = bs_model.pnl_3d_interactive_surface()

    st.subheader("3D Price Heatmap")
    st.plotly_chart(pnl_3d_intsurface_fig, use_container_width=True)
    """
    with col1:
        st.subheader("P&L Heatmap (CALL)")
        st.pyplot(callpnl_heatmap_fig)
    with col2:
        st.subheader("P&L Heatmap (PUT)")
        st.pyplot(putpnl_heatmap_fig)
"""
else:
    fig_call, fig_put = bs_model.plot_heatmap()
    
    with col1:
        st.subheader("Call Price Heatmap")
        st.pyplot(fig_call)

    with col2:
        st.subheader("Put Price Heatmap")
        st.pyplot(fig_put)
      
# 3D Surface Plot for P&L  

# real market data -> use an API and populate underlying price
# Implied Volatility solver | Input market option price -> solve for implied volatility -> plot implied vol curve for a range of strikes
# Greek Calculations | Plot Delta HeatMap or Vega Heatmap

# Clear All
# Back