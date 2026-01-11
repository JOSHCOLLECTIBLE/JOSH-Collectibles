import requests
from datetime import datetime
import os

def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana,jupiter-exchange-solana&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        
        # Rounding for clean logs
        sol_price = round(data['solana']['usd'], 2)
        jup_price = round(data['jupiter-exchange-solana']['usd'], 4)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - SOL: ${sol_price} | JUP: ${jup_price}\n"
        
        os.makedirs('data', exist_ok=True)
        with open("data/price_log.txt", "a") as f:
            f.write(log_entry)
            
        print(f"✅ Logged: {log_entry}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_crypto_prices()
