# 🎒 Campus Lost & Found Intelligence System

A centralized web platform that lets students and staff report lost and found
items, and automatically suggests matches between them using a transparent,
explainable scoring algorithm — replacing manual, scattered lost-and-found
handling with a single searchable system.

**Ministry / Division context:** Ministry of Education / General Administration
**Problem addressed:** Campus lost-and-found handling is manual and fragmented,
making it hard for students/staff to report items and for administrators to
match lost items with found ones.

---

## ✨ Features

| Requirement from the problem statement | How it's implemented |
|---|---|
| 📝 Lost-item reporting | `/report/lost` form: title, category, description, location, date, photo |
| 📦 Found-item reporting | `/report/found` form: same fields + current holding location |
| 🔍 Intelligent matching | Weighted scoring engine (category + text similarity + location + date proximity) run automatically on every new report |
| 📍 Location/details | Every report carries a specific location and free-text description |
| 🖼️ Item images | Optional photo upload, stored and shown on item detail pages |
| 👨‍💼 Admin workflow | Dedicated `/admin` dashboard: confirm/reject matches, view all reports, view users, stats |
| 🔔 Match notifications | In-app notification bell; users are notified when a match crosses a confidence threshold |
| 📊 Centralized system | Single database of all lost/found reports, searchable and filterable by anyone |

## 🧠 How the matching engine works

No black-box ML is needed to make this "intelligent" — the scoring is
explainable, which matters more for a real lost-and-found office. Every time
a report is submitted, it's compared against all open reports of the
opposite type:

```
Score (0–100) =
    30 pts  if categories match exactly
  + 40 pts  × text similarity of title+description (difflib SequenceMatcher)
  + 15 pts  × text similarity of location strings
  + 15 pts  × date-proximity bonus (decays to 0 over a 14-day window)
```

- Scores ≥ **40** are stored as a candidate match and shown on both items' detail pages.
- Scores ≥ **60** additionally trigger an in-app notification to both reporters.
- Admins see all pending matches ranked by score on `/admin` and can **Confirm**
  (closes both reports as resolved and notifies both users) or **Reject**.

See `app/matching.py` for the full implementation — it's about 90 lines and
intentionally simple to read and defend in a demo/viva.

## 🗂️ Project structure

```
lost-found-system/
├── app/
│   ├── __init__.py        # app factory
│   ├── models.py          # User, LostItem, FoundItem, Match, Notification
│   ├── matching.py         # the matching engine
│   ├── routes/
│   │   ├── auth.py         # register/login/logout
│   │   ├── main.py         # home, dashboard, browse/search, notifications
│   │   ├── items.py        # report lost/found, item detail, resolve
│   │   └── admin.py        # admin dashboard, confirm/reject matches
│   ├── templates/          # Jinja2 + Bootstrap 5 UI
│   └── static/             # CSS + uploaded item images
├── config.py               # env-based config (SQLite locally, Postgres in prod)
├── run.py                  # entry point
├── seed.py                 # demo data (admin + 2 users + 3 items with a live match)
├── requirements.txt
├── Procfile                 # for Render/Railway/Heroku-style deploys
└── .env.example
```

## 🚀 Run it locally

Requires Python 3.10+.

```bash
git clone <your-repo-url>
cd lost-found-system
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# optional: load demo data (admin + sample users + a pre-made match)
python seed.py

python run.py
```

Visit **http://127.0.0.1:5000**.

Demo accounts after `python seed.py`:
- Admin: `admin@campus.edu` / `admin123`
- User: `alice@campus.edu` / `password123`
- User: `bob@campus.edu` / `password123`

Without seeding, just click **Sign Up** and create your own account — the
first report you file (lost or found) is matched against everything already
in the database.

## ☁️ Deployment

This app is deployed as a live web application — see the **Live Demo** link
at the top of this repo. To deploy your own copy for free on **Render**:

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com) → **New +** → **Web Service** → connect the repo.
3. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app`
4. Add a free **PostgreSQL** instance on Render (New + → PostgreSQL), copy its
   **Internal Database URL**, and set it as the `DATABASE_URL` environment
   variable on the web service. Also set `SECRET_KEY` to any random string.
5. Deploy. The app auto-creates its tables on first boot (`db.create_all()`
   in the app factory) — no manual migration step needed for the first deploy.
6. (Optional) Run `python seed.py` once via Render's shell to load demo data.

Full step-by-step with screenshots-equivalent instructions is in
[`DEPLOYMENT.md`](DEPLOYMENT.md).

## 🛣️ Future work (out of scope for this MVP, by design)

- Visual (image-based) similarity matching using computer vision, on top of
  the current text/category/location/date scoring
- SMS/email notifications in addition to in-app ones
- Multi-campus / multi-tenant support
- QR-code claim tickets for found items held at the admin office

## 🧪 Tech stack

Flask · Flask-SQLAlchemy · Flask-Login · SQLite (dev) / PostgreSQL (prod) ·
Bootstrap 5 · Gunicorn

## 📄 License

MIT — free to use and adapt for your submission.
