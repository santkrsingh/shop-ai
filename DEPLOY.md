# 🚀 Deploy ShopAI Live (FREE)

## Step 1 — Push to GitHub

```bash
# Already done: repo is initialized in shopping-agent/

# Create a new repo on GitHub: https://github.com/new
# Name: "shop-ai" (or anything)
# Visibility: Public
# DO NOT initialize with README (we already have code)

# Then push:
cd shopping-agent
git remote add origin https://github.com/YOUR_USERNAME/shop-ai.git
git branch -M main
git push -u origin main
```

---

## Step 2 — Deploy Backend to Render (FREE)

1. Go to **https://dashboard.render.com**
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account if not already connected
4. Select the repo: **`shop-ai`**
5. Click **"Apply"**

Render will:
- Read `render.yaml` and auto-create the backend service
- Install Python dependencies from `requirements.txt`
- Run `seed_data.py` on first build to populate SQLite
- Deploy to a URL like: **`https://shopai-backend.onrender.com`**

**Wait 3-5 minutes** for the first deploy. You'll get the live URL.

---

## Step 3 — Deploy Frontend to Vercel (FREE)

1. Go to **https://vercel.com/new**
2. **Import Git Repository** → select **`shop-ai`**
3. **Framework Preset:** Vite
4. **Root Directory:** `frontend`
5. **Environment Variables** → Add:
   - Key: `VITE_API_URL`
   - Value: `https://shopai-backend.onrender.com` (paste your Render URL from Step 2)
6. Click **"Deploy"**

Vercel will:
- Build the React app
- Deploy to a URL like: **`https://shop-ai-xyz.vercel.app`**

**Wait 2-3 minutes**. Done.

---

## Your Live URLs

| Service | URL |
|---|---|
| **🚀 Live Frontend** | https://shop-ai-xyz.vercel.app |
| **Backend API** | https://shopai-backend.onrender.com |
| **API Docs** | https://shopai-backend.onrender.com/docs |

**That's it.** No API keys. No credit card. No config. Fully deployed.

---

## Free Tier Limits

| Platform | Limits | Notes |
|---|---|---|
| **Render** | 750 hrs/month, 512MB RAM | Backend sleeps after 15min inactivity — first request after sleep takes ~30s |
| **Vercel** | 100GB bandwidth/month | Frontend is always instant (served from CDN) |

---

## If Render backend sleeps

The **first API request** after 15min of inactivity will be slow (~30s). After that, it's fast.

To keep it awake 24/7 for free:
1. Use **[UptimeRobot](https://uptimerobot.com)** (free)
2. Add a monitor: `https://shopai-backend.onrender.com/health`
3. Check every 5 minutes

---

## To update after code changes

```bash
# Make changes to code...
git add .
git commit -m "Updated XYZ feature"
git push

# Both Render and Vercel will auto-redeploy within 2-3 minutes
```

No manual steps needed. Push → Auto-deploy.

---

## Architecture

```
User Browser
    ↓
Vercel (React SPA)
    ↓ API calls
Render (FastAPI + SQLite)
    ↓ returns JSON
Vercel renders UI
```

**All free. All automatic. All live.**
