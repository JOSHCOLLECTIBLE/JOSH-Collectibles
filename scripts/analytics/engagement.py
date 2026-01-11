import pandas as pd
import matplotlib.pyplot as plt
import os

def run_analysis(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found!")
        return
    
    df = pd.read_csv(file_path)
    top_10 = df.sort_values(by='total_droplets', ascending=False).head(10)

    josh_orange = '#FF8C00' 
    bg_color = '#0D0D0D'    

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=bg_color)
    ax.set_facecolor(bg_color)
    
    colors = plt.cm.YlOrBr(pd.Series(range(10, 0, -1)) / 15)
    bars = ax.barh(top_10['username'], top_10['total_droplets'], color=colors, edgecolor=josh_orange, linewidth=0.5)
    
    ax.set_title('JOSH-COLLECTIBLES: TOP SUPPORTERS', fontsize=18, fontweight='bold', pad=30, color=josh_orange)
    ax.set_xlabel('Total Droplets', fontsize=11, color='#666666', labelpad=15)
    ax.invert_yaxis()
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 120, bar.get_y() + bar.get_height()/2, f'{int(width):,}', 
                va='center', fontsize=10, color='white', fontweight='500')

    plt.figtext(0.5, 0.03, 'drip.haus/josh | Growth and Engagement Report', ha='center', fontsize=8, color='#444444')

    for spine in ['top', 'right', 'bottom']:
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_color('#333333')

    plt.tight_layout()
    plt.savefig("josh_top_supporters.png", dpi=300, facecolor=bg_color) 
    print("\n✨ Cleaned report saved as: josh_top_supporters.png\n")

if __name__ == "__main__":
    run_analysis('data/sample.csv')
