import math
import numpy as np
from numpy import log, sqrt, exp
from scipy.stats import norm

# (Include the BlackScholes class definition here)

class BlackScholes:
    def __init__(
        self,
        time_to_maturity: float, # T
        strike: float, # S
        current_price: float, # K
        volatility: float, # sigma
        interest_rate: float, # r
    ):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

    def calculate_prices(
        self,
    ):
        time_to_maturity = self.time_to_maturity
        strike = self.strike
        current_price = self.current_price
        volatility = self.volatility
        interest_rate = self.interest_rate

        d1 = (
            log(current_price / strike) +
            (interest_rate + 0.5 * volatility ** 2) * time_to_maturity
            ) / (
                volatility * sqrt(time_to_maturity)
            )
        d2 = d1 - volatility * sqrt(time_to_maturity)

        call_price = current_price * norm.cdf(d1) - (
            strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(d2)
        )
        put_price = (
            strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(-d2)
        ) - current_price * norm.cdf(-d1)

        self.call_price = call_price
        self.put_price = put_price

        # GREEKS
        # Delta
        self.call_delta = norm.cdf(d1)
        self.put_delta = 1 - norm.cdf(d1)

        # Gamma
        self.call_gamma = norm.pdf(d1) / (
            strike * volatility * sqrt(time_to_maturity)
        )
        self.put_gamma = self.call_gamma

        return call_price, put_price
    


