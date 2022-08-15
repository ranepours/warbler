from csv import DictReader
from app import db
from models import User, Message, Follows

db.drop_all()
db.create_all()

with open('generator/users.csv') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))
with open('generator/messages.csv') as messages:
    db.session.bulk_insert_mappings(Message, DictReader(messages))
with open('generator/messages.csv') as follows:
    db.session.bulk_insert_mappings(Follows, DictReader(follows))

db.session.commit()