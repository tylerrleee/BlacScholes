import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from numpy import log, sqrt, exp 
import matplotlib.pyplot as plt
import seaborn as sns

class BlackScholes:
    def __init__(
        self,
        time_to_maturity: float, # T
        strike: float, # K
        current_price: float, # S
        volatility: float, # sigma
        interest_rate: float, # r
        vol_range: np.ndarray = np.arange(0.1, 1.0, 0.1), 
        spot_range: np.ndarray = np.arange(50, 150, 10),

        C_buy: float = 0.0, # Call option purchase price
        P_buy: float = 0.0, # Put option purchase price
        call_price: float = 0.0, # Initial call price
        put_price: float = 0.0,# Initial put price
    ):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate
        self.vol_range = vol_range
        self.spot_range = spot_range
        self.P_buy = P_buy
        self.C_buy = C_buy
        self.call_price = call_price
        self.put_price = put_price

    def calculate_prices(self):
        d1 = (
            log(self.current_price / self.strike) +
            (self.interest_rate + 0.5 * self.volatility ** 2) * self.time_to_maturity
            ) / (
                self.volatility * sqrt(self.time_to_maturity)
            )
        d2 = d1 - self.volatility * sqrt(self.time_to_maturity)

        call_price = self.current_price * norm.cdf(d1) - (
            self.strike * exp(-(self.interest_rate * self.time_to_maturity)) * norm.cdf(d2)
        )
        put_price = (
            self.strike * exp(-(self.interest_rate * self.time_to_maturity)) * norm.cdf(-d2)
        ) - self.current_price * norm.cdf(-d1)

        self.call_price = call_price
        self.put_price = put_price

        # GREEKS
        # Delta
        self.call_delta = norm.cdf(d1)
        self.put_delta = 1 - norm.cdf(d1)

        # Gamma
        self.call_gamma = norm.pdf(d1) / (
            self.strike * self.volatility * sqrt(self.time_to_maturity)
        )
        self.put_gamma = self.call_gamma

        return call_price, put_price
    


    def plot_heatmap(self):
        call_prices = np.zeros((len(self.vol_range), len(self.spot_range)))
        put_prices = np.zeros((len(self.vol_range), len(self.spot_range)))
        for i, vol in enumerate(self.vol_range):
            for j, spot in enumerate(self.spot_range):
                bs_temp = BlackScholes(
                    time_to_maturity=self.time_to_maturity,
                    strike=self.strike,
                    current_price=spot,
                    volatility=vol,
                    interest_rate=self.interest_rate
                )
                call_price, put_price = bs_temp.calculate_prices()
                call_prices[i, j] = call_price
                put_prices[i, j] = put_price

        # Plotting Call Price Heatmap
        fig_call, ax_call = plt.subplots(figsize=(10, 8))
        vcall = np.abs(call_prices).max()
        sns.heatmap(call_prices, xticklabels=np.round(self.spot_range, 2), vmin=-vcall, vmax=vcall, yticklabels=np.round(self.vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call)
        ax_call.set_xlabel('Spot Price')
        ax_call.set_ylabel('Volatility')
        
        # Plotting Put Price Heatmap
        vput = np.abs(put_prices).max()
        fig_put, ax_put = plt.subplots(figsize=(10, 8))
        sns.heatmap(put_prices, xticklabels=np.round(self.spot_range, 2), vmin=-vput, vmax=vput, yticklabels=np.round(self.vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put)
        ax_put.set_xlabel('Spot Price')
        ax_put.set_ylabel('Volatility')
        
        return fig_call, fig_put

    def calculate_pnl(self):
        call_price, put_price = self.calculate_prices()
        # P&L = (option value - purchase price)
        pnl_call = call_price - self.C_buy
        pnl_put = put_price - self.P_buy
        return pnl_call, pnl_put

    def call_pnl_heatmap(self):
        pnl_matrix = np.zeros((len(self.vol_range), len(self.spot_range)))
        for i, vol in enumerate(self.vol_range):
            for j, spot in enumerate(self.spot_range):
                bs_temp = BlackScholes(
                    time_to_maturity=self.time_to_maturity,
                    strike=self.strike,
                    current_price=spot,
                    volatility=vol,
                    interest_rate=self.interest_rate,
                    C_buy=self.C_buy
                )
                call_price, _ = bs_temp.calculate_prices()
                pnl_matrix[i, j] = call_price - self.C_buy

        fig, ax = plt.subplots(figsize=(10, 8))
        v = np.abs(pnl_matrix).max()
        sns.heatmap(
            pnl_matrix,
            xticklabels=np.round(self.spot_range, 2),
            yticklabels=np.round(self.vol_range, 2),
            vmin=-v,
            vmax=v,
            annot=True,
            fmt=".2f",
            cmap="RdYlGn",
            center=0,
            ax=ax
        )
        ax.invert_yaxis()
        ax.set_title('P&L Heatmap (Call)')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')
        return fig

    def put_pnl_heatmap(self):
        pnl_matrix = np.zeros((len(self.vol_range), len(self.spot_range)))
        for i, vol in enumerate(self.vol_range):
            for j, spot in enumerate(self.spot_range):
                bs_temp = BlackScholes(
                    time_to_maturity=self.time_to_maturity,
                    strike=self.strike,
                    current_price=spot,
                    volatility=vol,
                    interest_rate=self.interest_rate,
                    C_buy=self.C_buy,
                    P_buy=self.P_buy
                )
                call_price, put_price = bs_temp.calculate_prices()
                pnl = (call_price - self.C_buy) + (put_price - self.P_buy)
                pnl_matrix[i, j] = pnl

        fig, ax = plt.subplots(figsize=(10, 8))
        v = np.abs(pnl_matrix).max()
        sns.heatmap(
            pnl_matrix,
            xticklabels=np.round(self.spot_range, 2),
            yticklabels=np.round(self.vol_range, 2),
            vmin= -v,
            vmax= v,
            annot=True,
            fmt=".2f",
            cmap="RdYlGn",
            center=0,
            ax=ax
        )
        ax.invert_yaxis()
        ax.set_title('P&L Heatmap (Put)') 
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')
        return fig

    def pnl_3d_surface(self):
        pnl_matrix = np.zeros((len(self.vol_range), len(self.spot_range)))
        for i, vol in enumerate(self.vol_range):
            for j, spot in enumerate(self.spot_range):
                bs_temp = BlackScholes(
                    time_to_maturity=self.time_to_maturity,
                    strike=self.strike,
                    current_price=spot,
                    volatility=vol,
                    interest_rate=self.interest_rate,
                    C_buy=self.C_buy,
                    P_buy=self.P_buy
                )
                call_price, put_price = bs_temp.calculate_prices()
                pnl = (call_price - self.C_buy) + (put_price - self.P_buy)
                pnl_matrix[i, j] = pnl

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection = '3d')
        surf = ax.plot_surface(self.spot_range, self.vol_range, pnl_matrix, cmap='RdYlGn', edgecolor='k', alpha=1)
        ax.set_title('3D P&L Surface Plot')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')
        ax.set_zlabel('P&L')
        fig.colorbar(surf, ax=ax, label = "PNL", shrink=0.5, aspect=5)
        return fig
    
    def pnl_3d_interactive_surface(self):
        pnl_matrix = np.zeros((len(self.vol_range), len(self.spot_range)))
        for i, vol in enumerate(self.vol_range):
            for j, spot in enumerate(self.spot_range):
                bs_temp = BlackScholes(
                    time_to_maturity=self.time_to_maturity,
                    strike=self.strike,
                    current_price=spot,
                    volatility=vol,
                    interest_rate=self.interest_rate,
                    C_buy=self.C_buy,
                    P_buy=self.P_buy
                )
                call_price, put_price = bs_temp.calculate_prices()
                pnl = (call_price - self.C_buy) + (put_price - self.P_buy)
                pnl_matrix[i, j] = pnl

        fig = go.Figure(data=[go.Surface(
            z=pnl_matrix,
            x=self.spot_range,
            y=self.vol_range,
            colorscale='RdYlGn',
            colorbar=dict(title='P&L'),
        )])
        fig.update_layout(
            title="P&L Volatility Map",
            scene=dict(
                xaxis_title='Spot Price (x)',
                yaxis_title='Volatility (y)',
                zaxis_title='P&L (z)'
            ),
            width=1000,
            height=800
        )
        return fig
    
    def delta(self):
        d1 = (
            log(self.current_price / self.strike) +
            (self.interest_rate + 0.5 * self.volatility ** 2) * self.time_to_maturity
            ) / (
                self.volatility * sqrt(self.time_to_maturity)
            )
        call_delta = norm.cdf(d1)
        put_delta = 1 - norm.cdf(d1)
        return call_delta, put_delta

    def delta_3d_surface(self):
        delta_matrix = np.zeros((len(self.vol_range), len(self.spot_range)))
        for i, vol in enumerate(self.vol_range):
            for j, spot in enumerate(self.spot_range):
                bs_temp = BlackScholes(
                    time_to_maturity=self.time_to_maturity,
                    strike=self.strike,
                    current_price=spot,
                    volatility=vol,
                    interest_rate=self.interest_rate,
                    C_buy=self.C_buy,
                    P_buy=self.P_buy
                )
                call_delta, put_delta = bs_temp.delta()
                delta_matrix[i, j] = call_delta

        X, Y = np.meshgrid(self.spot_range, self.vol_range)        
        fig = plt.figure(figsize=(10, 8))        
        ax = fig.add_subplot(111, projection = '3d')
        surf = ax.plot_surface(X, Y, delta_matrix, cmap='RdYlGn', edgecolor='k', alpha=1)
        ax.set_title('3D DELTA Surface Plot')
        ax.set_xlabel('Spot Price')
        ax.set_ylabel('Volatility')
        ax.set_zlabel('DELTA')
        fig.colorbar(surf, ax=ax, label = "DELTA", shrink=0.5, aspect=5)
        return fig
    
    def delta_3d_interactive_surface(self):
        delta_matrix = np.zeros((len(self.vol_range), len(self.spot_range)))
        for i, vol in enumerate(self.vol_range):
            for j, spot in enumerate(self.spot_range):
                bs_temp = BlackScholes(
                    time_to_maturity=self.time_to_maturity,
                    strike=self.strike,
                    current_price=spot,
                    volatility=vol,
                    interest_rate=self.interest_rate,
                    C_buy=self.C_buy,
                    P_buy=self.P_buy
                )
                call_delta, put_delta = bs_temp.delta()
                delta_matrix[i, j] = call_delta

        fig = go.Figure(data=[go.Surface(
            z=delta_matrix,
            x=self.spot_range,
            y=self.vol_range,
            colorscale='RdYlGn',
            colorbar=dict(title='P&L'),
        )])
        fig.update_layout(
            title="Delta Volatility Map",
            scene=dict(
                xaxis_title='Spot Price (x)',
                yaxis_title='Volatility (y)',
                zaxis_title='DELTA (z)'
            ),
            width=1000,
            height=800
        )
        return fig
# Call the function  