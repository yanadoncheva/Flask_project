import hashlib

from database import SQLite
from errors import ApplicationError


class User:

    def __init__(self, user_id, username, password, email, adress, phone ):
        self.id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.adress = adress
        self.phone = phone

    def create(self):
        with SQLite() as db:
            values = (self.username, self.password, self.email, self.adress, self.phone)
            db.execute('''
                INSERT INTO users (username, password, email, adress, phone)
                VALUES (?, ?, ?, ?, ?)''', values)
            return self

    def to_dict(self):
        user_data = self.__dict__
        del user_data["password"]
        return user_data

    def save(self):
        with SQLite() as db:
            cursor = db.execute(self.__get_save_query())
            self.id = cursor.lastrowid
        return self

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def delete(user_id):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM user WHERE id = ?",
                    (user_id,))
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)

    @staticmethod
    def find(user_id):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT username, password, id FROM user WHERE id = ?",
                    (user_id,))
        user = result.fetchone()
        if user is None:
            raise ApplicationError(
                    "Post with id {} not found".format(user_id), 404)
        return User(*user)

    @staticmethod
    def find_by_username(username):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT username, password, id FROM user WHERE username = ?",
                    (username,))
        user = result.fetchone()
        if user is None:
            raise ApplicationError(
                    "Post with name {} not found".format(username), 404)
        return User(*user)

#	def generate_token(self):
#		s = Serializer(SECRET_KEY, expires_in=600)
#		return s.dumps({'username': self.username})

    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT username, password, id FROM user").fetchall()
            return [User(*row) for row in result]

    def __get_save_query(self):
        query = "{} INTO user {} VALUES {}"
        if self.id == None:
            args = (self.username, self.password)
            query = query.format("INSERT", "(username, password)", args)
        else:
            args = (self.id, self.username, self.password)
            query = query.format("REPLACE", "(id, username, password)", args)
        return query
