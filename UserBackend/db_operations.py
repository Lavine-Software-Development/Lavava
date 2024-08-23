import sys
sys.path.append('UserBackend\app.py')  # Adjust this path to where your main app file is located

from app import app, db, User, Deck, DeckCard, GameHistory, UserSettings, EloHistory

# Run the script using Python: python db_operations.py

def add_user(username, password, email):
    with app.app_context():
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        print(f"User {username} added successfully.")

def update_user(user_id, **kwargs):
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db.session.commit()
            print(f"User {user.username} updated successfully.")
        else:
            print(f"User with id {user_id} not found.")

def delete_user(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f"User {user.username} deleted successfully.")
        else:
            print(f"User with id {user_id} not found.")

def list_users():
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, ELO: {user.elo}, Bio: {user.bio}")

def add_deck(name, user_id):
    with app.app_context():
        new_deck = Deck(name=name, user_id=user_id)
        db.session.add(new_deck)
        db.session.commit()
        print(f"Deck '{name}' added for user {user_id}.")

def add_card_to_deck(deck_id, ability, count):
    with app.app_context():
        new_card = DeckCard(deck_id=deck_id, ability=ability, count=count)
        db.session.add(new_card)
        db.session.commit()
        print(f"Card '{ability}' added to deck {deck_id}.")

def update_deck_name(user_id, old_name, new_name):
    with app.app_context():
        deck = Deck.query.filter_by(user_id=user_id, name=old_name).first()
        if deck:
            deck.name = new_name
            db.session.commit()
            print(f"Deck name updated from '{old_name}' to '{new_name}' for user {user_id}.")
        else:
            print(f"Deck '{old_name}' not found for user {user_id}.")

def list_users_decks(user_id):
    with app.app_context():
        decks = Deck.query.filter_by(user_id=user_id).all()
        if decks:
            for deck in decks:
                print(f"user_id: {user_id} deck_id: {deck.id} Name: {deck.name}")
        else:
            print("cant find decks")

def update_bio(user_id, new_bio):
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.bio = new_bio
            db.session.commit()
            print(f"user bio updated")

# Example usage
if __name__ == "__main__":
    list_users()
    pass

