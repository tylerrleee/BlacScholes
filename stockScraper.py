from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random
from selenium_stealth import stealth
from datetime import datetime
from bs4 import BeautifulSoup


class StockScraper:
    def __init__(self, ticker):
        self.ticker = ticker
        self.url = f"https://finance.yahoo.com/quote/{ticker}"
        self.info = {"Ticker": ticker, "current_price": None}

    def initialize_driver(self):
        # Use a real user agent string
        user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        user_agent = random.choice(user_agents)

        chrome_options = Options()
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_argument("--headless")  # run in the background
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        return driver

    def fetch_info(self):
        driver = self.initialize_driver()

        try:
            driver.get(self.url)
            time.sleep(5)  # Wait for the page to load completely
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")


            # Current Price
            #price_span = soup.find("span", {"data-testid": "qsp-price"})
            price_span = soup.find("span", {"data-testid": "qsp-price"})
            if price_span:
                self.info['current_price'] = float(price_span.text.replace(',', ''))
            else:
                self.info['current_price'] = None


        except Exception as e:
            print(f"An error occurred with URL {self.url}: {e}")
            self.info['current_price'] = None

        finally:
            driver.quit()
            return self.info
        
    def get_spot_price(self):
        info = self.fetch_info()
        return info.get('current_price', None)
    
    def calculate_time_to_maturity(self, maturity_date_str):
        today = datetime.today().date()
        maturity_date = datetime.strptime(maturity_date_str, '%Y-%m-%d').date()
        delta = maturity_date - today
        return max(delta.days / 365.0, 0.0)  # Convert days to years | 1.0 = a year | return 0.0 if negative


# Example usage:
if __name__ == "__main__":
    apple = StockScraper("AAPL")

    print(apple.calculate_time_to_maturity('2025-06-20'))
    print((20-16)/365)

