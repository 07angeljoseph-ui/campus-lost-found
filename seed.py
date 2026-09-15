"""
Seed the database with a demo admin account and a few sample lost/found
reports so the matching engine has something to show immediately.

Usage:
    python seed.py
"""
from datetime import date, timedelta

from app import create_app, db
from app.models import User, LostItem, FoundItem
from app.matching import run_matching_for_lost, run_matching_for_found

app = create_app()

with app.app_context(), app.test_request_context():
    db.drop_all()
    db.create_all()

    admin = User(name="Admin", email="admin@campus.edu", role="admin")
    admin.set_password("admin123")

    alice = User(name="Alice Sharma", email="alice@campus.edu", role="user")
    alice.set_password("password123")

    bob = User(name="Bob Verma", email="bob@campus.edu", role="user")
    bob.set_password("password123")

    db.session.add_all([admin, alice, bob])
    db.session.commit()

    today = date.today()

    lost1 = LostItem(
        title="Black Dell Laptop",
        category="Electronics",
        description="Dell Inspiron 15, black, has a small crack on the lid and a college sticker.",
        location="Central Library, 2nd floor",
        date_lost=today - timedelta(days=2),
        reporter_id=alice.id,
    )
    db.session.add(lost1)
    db.session.commit()
    run_matching_for_lost(lost1)

    found1 = FoundItem(
        title="Dell laptop found in library",
        category="Electronics",
        description="Found a black Dell laptop with a cracked lid near the reading area.",
        location="Central Library",
        holding_location="Security Office, Main Gate",
        date_found=today - timedelta(days=1),
        reporter_id=bob.id,
    )
    db.session.add(found1)
    db.session.commit()
    run_matching_for_found(found1)

    lost2 = LostItem(
        title="Blue water bottle",
        category="Water Bottles / Flasks",
        description="Milton steel blue bottle with a dent on the bottom.",
        location="Sports Ground",
        date_lost=today - timedelta(days=5),
        reporter_id=bob.id,
    )
    db.session.add(lost2)
    db.session.commit()
    run_matching_for_lost(lost2)

    print("Seeded database with demo users and items.")
    print("Admin login: admin@campus.edu / admin123")
    print("User logins: alice@campus.edu / password123, bob@campus.edu / password123")
