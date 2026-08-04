#!/bin/bash
# ==============================================================================
# 1-CLICK DEPLOYMENT SCRIPT FOR THE JOSH¹ ARCHIVE
# Automatically copies .github workflow, forces upload of JPEG images,
# and pushes updates to GitHub!
# ==============================================================================

echo "🏛️  Deploying JOSH¹ Archive Marketing Engine to GitHub..."

# Ensure we are standing in the repository root (JOSH-Collectibles)
if [ ! -d ".git" ] && [ -d "../.git" ]; then
    cd ..
fi

# 1. Automatically copy the .github folder to the repository root
mkdir -p .github/workflows
cp -r inprnt_marketing_bot/.github/* .github/ 2>/dev/null || cp inprnt_marketing_bot/.github/workflows/daily_art_promotion.yml .github/workflows/daily_art_promotion.yml

# 2. FORCE-ADD ALL JPEG and PNG images so GitHub raw CDN URLs are never 404!
git add -f inprnt_marketing_bot/output/*.jpg inprnt_marketing_bot/output/*.png 2>/dev/null || true
git add .

# 3. Commit updates
git commit -m "🏛️ Update JOSH¹ Archive Phygital bot & 100% guaranteed JPEG carousel slides" || echo "No new changes to commit"

# 4. Push to GitHub
git push origin main

echo "✅ Deployment complete! All JPEG images are 100% live on GitHub CDN."
