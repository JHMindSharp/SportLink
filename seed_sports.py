# seed_sports.py
from app import create_app
from app.extensions import db
from app.models import Sport

app = create_app()
with app.app_context():
    sports = ['Football', 'Basketball', 'Tennis', 'Natation', 'Cyclisme', 'Course à pied', 'Yoga', 'Danse', 'Escalade', 'Boxe', 'Rugby', 'Golf', 'Badminton', 'Ping-pong', 'Ski', 'Snowboard', 'Surf', 'Karate', 'Judo', 'Pilates']
    for sport_name in sports:
        sport = Sport(name=sport_name)
        db.session.add(sport)
    db.session.commit()
    print('Sports ajoutés à la base de données.')
