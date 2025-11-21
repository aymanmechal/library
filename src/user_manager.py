import json
from src.models import User
from src.exceptions import ErreurBibliotheque

class UserManager:
    def __init__(self, json_path="data/users.json"):
        self.json_path = json_path
        self.users = []

    def add_user(self, user: User):
        self.users.append(user)

    def save(self):
        data = [u.to_data() for u in self.users]

        try:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

        except PermissionError:
            raise ErreurBibliotheque("Permission refusée !")

    def load(self):
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

        except FileNotFoundError:
            self.users = []
            return

        except PermissionError:
            raise ErreurBibliotheque("Permission refusée !")

        except json.JSONDecodeError:
            raise ErreurBibliotheque("JSON invalide !")

        self.users = [User(u["username"], u["password"], u["is_admin"]) for u in data]
