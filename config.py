import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

    # Render/Heroku-style Postgres URLs start with postgres://, SQLAlchemy needs postgresql://
    _db_url = os.environ.get("DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'instance', 'app.db')}")
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    # Matching thresholds (0-100 score)
    MATCH_MIN_SCORE = 40       # store as a candidate match
    MATCH_NOTIFY_SCORE = 60    # trigger a notification to the user
