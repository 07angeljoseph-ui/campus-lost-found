# Deployment Guide — Render (free tier)

This guide gets you from local code to a public, live URL in about 5–10 minutes.
Render is used because it has a genuinely free tier for both the web service
and a small Postgres database, and it deploys straight from GitHub with no
credit card required for the free tier.

## 1. Push the code to GitHub

```bash
cd lost-found-system
git init
git add .
git commit -m "Initial commit: Campus Lost & Found Intelligence System"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

Make sure the repo is **Public** (required by the submission checklist).

## 2. Create a Postgres database on Render

1. Go to https://dashboard.render.com → **New +** → **PostgreSQL**.
2. Name it (e.g. `lost-found-db`), leave region/plan on the free defaults, **Create Database**.
3. Once it's up, open it and copy the **Internal Database URL** (starts with `postgres://`).
   Keep this tab open — you'll need it in step 4.

## 3. Create the web service

1. **New +** → **Web Service** → connect your GitHub account → select the repo.
2. Fill in:
   - **Name:** `campus-lost-found` (this becomes part of your URL)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app`
   - **Instance Type:** Free
3. Don't click Create yet — add environment variables first (next step).

## 4. Environment variables

Under **Environment** on the web service setup screen, add:

| Key | Value |
|---|---|
| `DATABASE_URL` | the Internal Database URL you copied in step 2 |
| `SECRET_KEY` | any long random string, e.g. generate with `python -c "import secrets; print(secrets.token_hex(32))"` |

Click **Create Web Service**. Render will build and deploy automatically —
watch the logs; the first deploy takes a couple of minutes.

## 5. Verify

Once the deploy finishes, Render gives you a URL like:

```
https://campus-lost-found.onrender.com
```

Open it. You should see the landing page. The database tables are created
automatically on first app startup (`db.create_all()` runs inside the app
factory), so there's nothing extra to run — but if you'd like demo data:

1. On the web service page, open the **Shell** tab.
2. Run: `python seed.py`
3. Refresh the site — you'll see seeded items and can log in as
   `admin@campus.edu` / `admin123`.

## 6. Put the live link in your README / submission

Replace the placeholder at the top of `README.md` with:

```markdown
**🔗 Live Demo:** https://campus-lost-found.onrender.com
```

## Notes on the free tier

- Render's free web services spin down after ~15 minutes of inactivity and
  take ~30–50 seconds to wake back up on the next request. This is normal
  and fine for a hackathon demo — just mention it if a judge hits a slow
  first load.
- Uploaded images are stored on local disk on Render's free tier, which is
  **ephemeral** (cleared on redeploy/restart). For a hackathon submission
  this is acceptable; for a production version, swap `_save_image` in
  `app/routes/items.py` for an S3-compatible object store (e.g. Cloudflare R2,
  Backblaze B2, or Supabase Storage).

## Alternative: Railway

Railway works almost identically — connect the GitHub repo, it detects the
`Procfile` automatically, add a Postgres plugin, set `DATABASE_URL` and
`SECRET_KEY`, deploy. Railway's free tier is usage-credit based rather than
sleep-based, so it may suit a live judging session better if you have credit
available.
