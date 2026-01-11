import pandas as pd
import matplotlib.pyplot as plt
import os

def run_production_analytics():
    print("🚀 JOSH-Collectibles: Running Production Analytics...")
    data_path = 'data/'
    files = [f for f in os.listdir(data_path) if f.endswith('.csv')]
    
    if not files:
        print("⚠️ No data found.")
        return

    df = pd.read_csv(os.path.join(data_path, files[0]))
    
    # 1. Export the 'Top 50' for an airdrop whitelist
    top_50 = df.nlargest(50, 'total_droplets')
    top_50.to_csv('top_50_whitelist.csv', index=False)
    print("📝 Whitelist saved: 'top_50_whitelist.csv' (Ready for airdrop!)")

    # 2. Visualizing the 'Supporter Gap'
    plt.figure(figsize=(12, 6))
    # Plotting top 20 to see the distribution
    top_20 = df.nlargest(20, 'total_droplets')
    plt.bar(top_20['username'], top_20['total_droplets'], color='purple')
    plt.xticks(rotation=45, ha='right')
    plt.title('Top 20 Supporter Distribution')
    plt.ylabel('Total Droplets')
    
    plt.tight_layout()
    plt.savefig('droplet_distribution.png')
    print("🎨 Distribution chart saved: 'droplet_distribution.png'")

if __name__ == "__main__":
    run_production_analytics()