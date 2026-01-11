from solana.rpc.api import Client

# Connect to Solana mainnet
client = Client("https://api.mainnet-beta.solana.com")

# Replace this with your wallet address
wallet_address = "EsAU5xyJFWFGZGwxrtvkxL56VnAknE15sGvLU4f9Gea6"

# Fetch balance
balance = client.get_balance(wallet_address)
sol_balance = balance['result']['value'] / 1_000_000_000

print(f"Balance: {sol_balance} SOL")


