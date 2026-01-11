import requests
import os  # Added to allow Mac to speak
from datetime import datetime

# --- SETTINGS ---
TARGET_PRICE = 150.00  # Set the price you want to be alerted for
# ----------------

def get_sol_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_24hr_change=true"
    try:
        response = requests.get(url)
        data = response.json()
        price = data['solana']['usd']
        change = data['solana']['usd_24h_change']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        output = f"[{timestamp}] SOL: ${price:,.2f} ({change:.2f}%)"
        print(output)
        
        # 1. Save to log
        with open('/Users/joshuadenouden/JOSH-Collectibles/data/price_log.txt', 'a') as f:
            f.write(output + "\n")

        # 2. TRIGGER ALERT IF TARGET MET
        if price >= TARGET_PRICE:
            # This makes the Mac speak
            os.system(f'say "Solana hit {price} dollars. Time to moon."')
            # This plays a system sound (Submarine/Ping)
            os.system('afplay /System/Library/Sounds/Ping.aiff')
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_sol_price()