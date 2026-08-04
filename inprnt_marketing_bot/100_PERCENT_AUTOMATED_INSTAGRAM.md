# 🚀 100% Hands-Free Automated Instagram Posting Guide
**Target Account:** `@joshuadenouden`  
**Goal:** Have your GitHub Actions bot automatically publish your daily sequential artwork (`#197 -> #1` or `#199 -> #222`) directly to your Instagram feed without you copying a CSV or touching a button!

---

## 🌟 Method 1: The 3-Minute Make.com Webhook Bridge (Easiest — ZERO Meta Developer Account Needed!)

Why fight with Meta's developer portal when **[Make.com](https://www.make.com/)** (formerly Integromat) is already an official Meta-approved developer partner? 

Make.com has a **100% Free Plan** that lets your GitHub Actions bot trigger automated Instagram posts via a simple Webhook!

### How to wire it up in 3 minutes:

#### **Step 1: Create a Free Account on Make.com**
1. Go to **[make.com](https://www.make.com/)** and sign up for free.
2. Click **Create a new scenario** (top right button).

#### **Step 2: Add the Webhook Trigger**
1. Click the big **+** circle in the center &rarr; search for **Webhooks** &rarr; select **Custom webhook**.
2. Click **Create a webhook** &rarr; name it `JOSH1 Instagram Bot`.
3. **What about "API Key authentication / Add API key"?**
   - **You can leave API keys completely blank!** Just click **Save**! *(By default, any request with your unique webhook URL is accepted).*
   - **OR if you want to use an API Key for extra security:** Click **Add API key**, generate a key (e.g. `josh_secret_123`), and save it.
4. Copy the Webhook URL it gives you *(e.g., `https://hook.us1.make.com/abc123xyz`)*.

#### **Step 3: Connect to Instagram & Map the Photo URL and Caption**
1. In Make.com, right-click your Webhook module and click **"Run this module only"** (or **Run once** at the bottom left).
2. On your Mac Terminal, run:
   ```bash
   python3 -m src.instagram_bot --verify
   ```
   *(Make.com will instantly receive a sample artwork test payload containing `image_url` and `caption`!)*
3. Now click the **+** next to your webhook to add a second module &rarr; search for **Instagram for Business** &rarr; select **Create a Photo Post**.
4. Click **Add connection** &rarr; log in to your `@joshuadenouden` Instagram account *(Make.com is official, so this is 100% safe!)*.
5. In the module fields:
   - **Photo URL\*:** Click inside the box and select **`1. image_url`** from the dropdown list.
   - **Caption:** Click inside the box and select **`1. caption`** from the dropdown list.
   - **User Tags / Location ID:** Leave both completely blank!
6. Click **OK** and turn the scenario toggle **ON** at the bottom left!

#### **Step 4: Put Your Webhook Secrets into GitHub**
1. Go to **[github.com/JOSHCOLLECTIBLE/JOSH-Collectibles](https://github.com/JOSHCOLLECTIBLE/JOSH-Collectibles)** &rarr; **Settings** &rarr; **Secrets and variables** &rarr; **Actions** &rarr; **New repository secret**:
   - **Name:** `MAKE_INSTAGRAM_WEBHOOK_URL`
   - **Value:** *(paste your Make.com webhook URL)*
2. *(Optional — only if you created an API key in Step 2)*: Add a second secret:
   - **Name:** `MAKE_WEBHOOK_API_KEY`
   - **Value:** *(paste your API key string)*
3. Click **Save**!

🎉 **YOU ARE 100% AUTOMATED!** 
Every day at 16:30 UTC, your GitHub Actions bot will automatically send the artwork image URL and your exact curatorial caption to Make.com, which will instantly publish it to `@joshuadenouden`! Zero CSVs, zero manual work!

---

## 🔧 Method 2: Official Meta Graph API (How to Fix the "You don't have access" Error)

If you still want to generate your own Meta Developer token on `developers.facebook.com`:

### Why did Meta say "You don’t have access. This feature isn't available to you yet"?
Meta requires every personal Facebook account to **Register as a Meta Developer** before creating apps.

### How to fix it in 60 seconds:
1. Go to **[developers.facebook.com](https://developers.facebook.com/)** &rarr; look at the top right corner and click **Register** (or **Get Started**).
2. Agree to the Meta Platform Terms and verify your phone number or email address.
3. Once registered, click **My Apps** &rarr; **Create App** &rarr; choose **Other** &rarr; **Business** &rarr; add **Instagram Graph API**.
4. Use the Graph API Explorer to generate your token and add `INSTAGRAM_ACCESS_TOKEN` and `INSTAGRAM_ACCOUNT_ID` to your GitHub Secrets!
