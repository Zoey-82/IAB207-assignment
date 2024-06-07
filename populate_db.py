from your_application_package import create_app, db
from your_application_package.models import User, Event
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = create_app()
app.app_context().push()

# create random users
user1 = User(
    first_name="John",
    last_name="Pork",
    user_name="johnpork",
    email="john@example.com",
    password=generate_password_hash("password123"),
    contact_number="1234567890",
    street_address="123 Queen St"
)

user2 = User(
    first_name="Clay",
    last_name="Smith",
    user_name="claysmith",
    email="clay@example.com",
    password=generate_password_hash("password123"),
    contact_number="0987654321",
    street_address="456 Lint St"
)

# Create sample events
event1 = Event(
    title="Sample Event 1",
    description="This is a description for Sample Event 1.",
    date=datetime.now() + timedelta(days=5),
    owner_id=1,  # Assuming user1's ID is 1
    status="Open"
)

event2 = Event(
    title="Sample Event 2",
    description="This is a description for Sample Event 2.",
    date=datetime.now() + timedelta(days=10),
    owner_id=2,  # Assuming user2's ID is 2
    status="Open"
)

db.session.add_all([user1, user2, event1, event2])
db.session.commit()
print("Database populated with sample data.")