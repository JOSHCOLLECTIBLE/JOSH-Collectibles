# 🚀 Step-by-Step Guide: Integrating with your existing `JOSH-Collectibles` GitHub Repository

Since you already started your GitHub repository months ago (**[JOSHCOLLECTIBLE/JOSH-Collectibles](https://github.com/JOSHCOLLECTIBLE/JOSH-Collectibles)**) for your Solana NFT collectibles (`JOSHSHOOT.SOL` / `@joshuadenouden`), you **do not** need to create a new repository! 

We can add this JOSHSHOOT PRINTS marketing engine directly into your existing `JOSH-Collectibles` repo so your NFT prototype scripts and your INPRNT automated marketing engine live together under **The JOSH Archive**.

---

## 🛠️ From Step One: Updating `JOSH-Collectibles` (Command Line Instructions)

### Step 1: Open Your Terminal & Clone Your Existing Repository
If you don't already have your repo cloned on your local computer, open your terminal (Terminal on macOS/Linux, or PowerShell/Git Bash on Windows) and run:

```bash
git clone https://github.com/JOSHCOLLECTIBLE/JOSH-Collectibles.git
cd JOSH-Collectibles
```

*(If you already have `JOSH-Collectibles` on your computer, simply `cd` into it and run `git pull origin main` to make sure you have the latest version).*

---

### Step 2: Copy the Bot Files into Your Repository
Copy the entire `inprnt_marketing_bot/` directory from this workspace into your `JOSH-Collectibles` folder. Your project folder structure will look like this:

```text
JOSH-Collectibles/
├── ... (your existing prototype scripts, NFT analytics, Solana name service files)
└── inprnt_marketing_bot/
    ├── README.md
    ├── SETUP_GUIDE.md
    ├── GITHUB_SETUP_JOSH_COLLECTIBLES.md
    ├── MARKET_TRENDS_2026.md
    ├── config.yaml
    ├── requirements.txt
    ├── .github/
    │   └── workflows/
    │       └── daily_art_promotion.yml
    ├── src/
    │   ├── scraper.py
    │   ├── content_generator.py
    │   ├── storage.py
    │   ├── notifier.py
    │   └── main.py
    └── output/
        ├── full_campaign_dashboard.html
        ├── latest_campaign_report.html
        ├── pinterest_bulk_queue.csv
        └── ...
```

---

### Step 3: Set Up the GitHub Actions Workflow in Your Repository Root
For GitHub Actions to detect the daily automation workflow automatically, copy the `.github/` folder from inside `inprnt_marketing_bot/` to the very root of your `JOSH-Collectibles` repository:

```bash
# Inside JOSH-Collectibles/
mkdir -p .github/workflows
cp inprnt_marketing_bot/.github/workflows/daily_art_promotion.yml .github/workflows/daily_art_promotion.yml
```

Now, open `.github/workflows/daily_art_promotion.yml` and verify that the `run` command points to the `inprnt_marketing_bot` folder:

```yaml
      - name: 🎨 Run INPRNT Daily Promotion Bot
        working-directory: ./inprnt_marketing_bot
        run: |
          python -m src.main --action daily-promo --config config.yaml
```

---

### Step 4: Commit and Push Your Updates to GitHub
Now let's push your new JOSHSHOOT PRINTS marketing engine and automated workflow to `https://github.com/JOSHCOLLECTIBLE/JOSH-Collectibles`:

```bash
git add .
git commit -m "🏛️ Add JOSHSHOOT PRINTS editorial INPRNT marketing engine & JOSHSHOOT.SOL Web3 integration"
git push origin main
```

*(If prompted for your GitHub login, authenticate with your username `JOSHCOLLECTIBLE` and your Personal Access Token).*

---

### Step 5: Enable Write Permissions & Test Your Free Cloud Automation
1. Go to your repository on GitHub: **[github.com/JOSHCOLLECTIBLE/JOSH-Collectibles](https://github.com/JOSHCOLLECTIBLE/JOSH-Collectibles)**.
2. Click **Settings** (top navigation bar) &rarr; **Actions** (left sidebar) &rarr; **General**.
3. Scroll down to **Workflow permissions**.
4. Select **Read and write permissions** (this allows the bot to update `history.json` automatically after each promotion so it never repeats the same print).
5. Click **Save**.
6. Now click the **Actions** tab at the top of your repository &rarr; select **🎨 Daily INPRNT Art Promotion (100% Free Cloud Automation)** &rarr; click **Run workflow**.

🎉 **You are done!** Every day at 2 PM UTC (or whenever you click **Run workflow**), your bot will scrape your INPRNT gallery, generate JOSHSHOOT PRINTS editorial copy linking **JOSHSHOOT.SOL** and **INPRNT**, and upload your daily HTML report and Pinterest CSV queue!
