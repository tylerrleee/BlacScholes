from BSfunctions import BlackScholes
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from numpy import log, sqrt, exp 
import matplotlib.pyplot as plt
import seaborn as sns

    # Heat Map Function
def plot_heatmap(bs_model, spot_range, vol_range, strike):
        call_prices = np.zeros((len(vol_range), len(spot_range)))
        put_prices = np.zeros((len(vol_range), len(spot_range)))
        
        for i, vol in enumerate(vol_range):
            for j, spot in enumerate(spot_range):
                bs_temp = BlackScholes(
                    time_to_maturity=bs_model.time_to_maturity,
                    strike=strike,
                    current_price=spot,
                    volatility=vol,
                    interest_rate=bs_model.interest_rate
                )
                bs_temp.calculate_prices()
                call_prices[i, j] = bs_temp.call_price
                put_prices[i, j] = bs_temp.put_price
        
        # Plotting Call Price Heatmap
        fig_call, ax_call = plt.subplots(figsize=(10, 8))

        vcall = np.abs(call_price).max()

        sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), vmin = -vcall, vmax = vcall, yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call)
        ax_call.set_xlabel('Spot Price')
        ax_call.set_ylabel('Volatility')
        
        # Plotting Put Price Heatmap

        vput = np.abs(put_prices).max()
        fig_put, ax_put = plt.subplots(figsize=(10, 8))
        sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), vmin = -vput, vmax = vput, yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put)
        ax_put.set_xlabel('Spot Price')
        ax_put.set_ylabel('Volatility')
        
        return fig_call, fig_put

def pnl_heatmap(current_price, strike, time_to_expiry, volatility, interest_rate, C_buy, P_buy, spot_range, vol_range):
    pnl_matrix = np.zeros((len(vol_range), len(spot_range)))
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(
                time_to_maturity=time_to_expiry,
                strike=strike,
                current_price=spot,
                volatility=vol,
                interest_rate=interest_rate
            )
            call_price, put_price = bs_temp.calculate_prices()
            # P&L = (option value - purchase price)
            pnl = (call_price - C_buy) + (put_price - P_buy)
            pnl_matrix[i, j] = pnl

    fig, ax = plt.subplots(figsize=(10, 8))
    v = np.abs(pnl_matrix).max()
    sns.heatmap(
        pnl_matrix,
        xticklabels=np.round(spot_range, 2),
        yticklabels=np.round(vol_range, 2),
        vmin= -v,
        vmax= v,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        center=0,
        ax=ax
    )
    ax.invert_yaxis()
    ax.set_title('P&L Heatmap (Call + Put)') 
    ax.set_xlabel('Spot Price')
    ax.set_ylabel('Volatility')
    return fig


# Title of the app
st.set_page_config(
    page_title="Tyle|Black-Scholes Option Pricing Model",
    page_icon="😹",
    layout="wide",
    initial_sidebar_state="expanded")

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


# Sidebar for User Inputs
with st.sidebar:
    st.title("Black-Scholes Model")
    st.markdown("-----")

    if st.toggle("Manual Inputs", value=False):
        current_price     = st.number_input("Current/Underlying Price (S)", min_value=0.0, value=100.0)
        strike     = st.number_input("Strike Price", min_value = 0.0, value=100.0)
        time_to_expiry     = st.number_input("Time to Expiry", min_value=0.0, value=1.0)
        volatility = st.number_input("Volatility",   min_value=0.0, value=0.2)
        interest_rate     = st.number_input("Risk-free Interest Rate", value=0.05)
    else:
        # Placeholder for real-time data inputs
        current_price = 100.0
        strike = 100.0
        time_to_expiry = 1.0
        volatility = 0.2
        interest_rate = 0.05

        # Placeholder for real-time data retrieval w/ stock ticker input
        st.text_input("Enter Stock Ticker", placeholder="e.g., AAPL, TSLA, BTC-USD")
    # Display current inputs
    


    st.markdown("-----")

    st.header("Heatmap Parameters")
    # Toggle for P&L Graph
    PL_toggle_on = st.toggle("P/L Graph", value=False)
    # Utilize real time data (pending)
    if PL_toggle_on:
        C_buy = st.sidebar.number_input("Purchase Price of Call", min_value=0.0, value=5.0, step=0.1)
        P_buy = st.sidebar.number_input("Purchase Price of Put",  min_value=0.0, value=3.0, step=0.1)

    
   # calculate_btn = st.button('Heatmap Parameters')
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price*0.8, step=0.01)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price*1.2, step=0.01)
    vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*0.5, step=0.01)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*1.5, step=0.01)
    
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

# Main Page for Output

st.title("Black-Scholes Pricing Model")

# Table of Inputs (not needed for now)

# Calculate Call and Put Values
bs_model = BlackScholes(
    time_to_maturity=time_to_expiry,
    strike=strike,
    current_price=current_price,
    volatility=volatility,
    interest_rate=interest_rate
)
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
    pnl_heatmap_fig = pnl_heatmap(
        current_price=current_price,
        strike=strike,
        time_to_expiry=time_to_expiry,           
        volatility=volatility,
        interest_rate=interest_rate,
        C_buy=C_buy,
        P_buy=P_buy,
        spot_range=spot_range,
        vol_range=vol_range
    )
    with col1:
        st.subheader("P&L Heatmap (Call + Put)")
        st.pyplot(pnl_heatmap_fig)

else:
    fig_call, fig_put = plot_heatmap(bs_model, spot_range, vol_range, strike)

    with col1:
        st.subheader("Call Price Heatmap")
        st.pyplot(fig_call)

    with col2:
        st.subheader("Put Price Heatmap")
        st.pyplot(fig_put)
        

# real market data -> use an API and populate underlying price
# Implied Volatility solver | Input market option price -> solve for implied volatility -> plot implied vol curve for a range of strikes
# Greek Calculations | Plot Delta HeatMap or Vega Heatmap

