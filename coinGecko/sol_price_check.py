import requests
import json
from datetime import datetime

def get_sol_price():
    # CoinGecko API URL for Solana
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_24hr_change=true"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        price = data['solana']['usd']
        change = data['solana']['usd_24h_change']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"--- JOSH-Collectibles Price Feed ---")
        print(f"Time: {timestamp}")
        print(f"Solana Price: ${price:,.2f}")
        print(f"24h Change: {change:.2f}%")
        
        # Save to a simple log file in your data folder
        with open('data/price_log.txt', 'a') as f:
            f.write(f"{timestamp}, {price}, {change:.2f}%\n")
            
    except Exception as e:
        print(f"Could not fetch price: {e}")

if __name__ == "__main__":
    get_sol_price()