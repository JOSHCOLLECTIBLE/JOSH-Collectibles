# 📸 Instagram Automation & Sequential Archive Curation Guide
**Target Account:** `@joshuadenouden` (`https://www.instagram.com/joshuadenouden/`)  
**Archive Milestone:** Starting sequential focus from **JOSH¹ #197 / #199 onwards**

---

## 🤖 1. Can You Automate Instagram Posting via Python Code / Bots?

**YES!** However, there is a critical technical difference between the two methods available in 2026:

| Method | Risk Level | How It Works | Recommended for `@joshuadenouden`? |
| :--- | :--- | :--- | :--- |
| **Official Meta Graph API** (Included in Your Bot) | **0% Risk (100% Safe)** | Uses Instagram's official developer API with an access token. Endorsed by Meta. Never triggers SMS lockouts or shadowbans. | **YES (Highly Recommended)** |
| **Unofficial Scraping Bots (`instagrapi` / Selenium)** | **High Risk (Bans/Shadowbans)** | Logs in using your username and password from a cloud IP address. Instagram's 2026 AI flags cloud logins and blocks account reach. | **NO (Avoid for your core artist account)** |

---

## 🛠️ 2. How to Enable 100% Free Automated Direct Posting (Official Meta API)

Your bot (`src/instagram_bot.py`) is already coded to publish your artwork image and custom technical caption directly to `@joshuadenouden` automatically during your daily GitHub Actions run!

Here is how to connect it in **5 minutes**:

### Step 1: Make Sure Your Instagram Account is a Free Creator/Professional Account
1. Open Instagram on your phone &rarr; go to your `@joshuadenouden` profile &rarr; tap **Settings**.
2. Tap **Account type and tools** &rarr; select **Switch to Professional account** (or **Creator**). *(This is 100% free)*.

### Step 2: Link Your Instagram to a Facebook Page
1. In Instagram settings &rarr; tap **Account Center** &rarr; link your Instagram account to a Facebook Page (you can create a simple artist page called `"JOSH SHOOT - The Archive"` in 10 seconds).

### Step 3: Get Your Official Meta API Token
1. Go to the Meta Developers portal: **[developers.facebook.com](https://developers.facebook.com/)** and log in.
2. Click **My Apps** &rarr; **Create App** &rarr; choose **Other** &rarr; select **Business**.
3. Under **Add Products**, add **Instagram Graph API**.
4. Use the **Graph API Explorer** tool to generate a **Page Access Token** with `instagram_basic` and `instagram_content_publish` permissions.
5. Note down your **`INSTAGRAM_ACCESS_TOKEN`** and your **`INSTAGRAM_ACCOUNT_ID`**.

### Step 4: Add Your Tokens to Your GitHub Repository Secrets
1. Go to your repository on GitHub: **[github.com/JOSHCOLLECTIBLE/JOSH-Collectibles](https://github.com/JOSHCOLLECTIBLE/JOSH-Collectibles)**.
2. Click **Settings** &rarr; **Secrets and variables** &rarr; **Actions** &rarr; **New repository secret**:
   - **Secret 1 Name:** `INSTAGRAM_ACCESS_TOKEN`
   - **Secret 2 Name:** `INSTAGRAM_ACCOUNT_ID`
3. Click **Save**!

🎉 **That's it!** Whenever GitHub Actions runs your workflow, your Python script will detect those credentials and **automatically publish your artwork and caption to your Instagram feed!**

---

## 🔢 3. How Sequential Archive Numbering Works (`#197 / #199 Onwards`)

You mentioned that your Instagram left off at **`JOSH1 198: KP's Window 🇳🇱`**, and you want to focus on **#197 onwards** or **#199 to #222**.

Your bot (`src/storage.py`) now includes an intelligent **Archive Sequence Filter** controlled by `config.yaml`:

```yaml
promotion:
  start_from_number: 199          # Sets your starting sequence number (e.g. 199 to continue after 198)
  sequence_direction: "ascending" # "ascending" (199 -> 222) or "descending" (197 -> 1)
```

### How to use it:
- **To continue forward after KP's Window (#198):** Leave `start_from_number: 199` and `sequence_direction: "ascending"`. Your bot will automatically promote `#199`, then `#200`, then `#201`... all the way up to `#222`!
- **To catch up on earlier prints from #197 backwards:** Change `start_from_number: 197` and `sequence_direction: "descending"`. The bot will promote `#197`, then `#196`, then `#195`... sequentially down to `#1`!

You can change `start_from_number` in `config.yaml` anytime you want to shift the bot's focus to a different section of **The JOSH¹ Archive**!
