# 🚀 Solana Price Autopilot

An automated data funnel that tracks Solana (SOL) prices in real-time using GitHub Actions.

## 🛠️ The Funnel
1. **Source:** CoinGecko API
2. **Engine:** GitHub Actions (Python 3.9)
3. **Storage:** Flat-file logging in `/data/price_log.txt`
4. **Schedule:** Runs automatically every hour

## 📁 Structure
- `scripts/`: Core Python logic.
- `.github/workflows/`: Automation configuration.
- `data/`: Historical price datasets.

---
*Maintained by [JOSHCOLLECTIBLE](https://github.com/JOSHCOLLECTIBLE)*
