import sqlite3
from flask import redirect, session
from functools import wraps
import re


class SQL:
    def __init__(self, path):
        self.path = path

    def execute(self, query, params=None, fetch_as_dictionary=True):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        conn.commit()

        data = None
        if fetch_as_dictionary:
            if cur.description:
                # Check if there are results before accessing to avoid errors
                columns = [column[0] for column in cur.description]
                data = [dict(zip(columns, row)) for row in cur.fetchall()]
        else:
            data = cur.fetchall()
        cur.close()
        conn.close()

        # return the data
        return data


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def validate_password(password):
    # Check if the password is at least 8 characters long
    if len(password) < 8:
        return False

    # Check if the password contains at least one uppercase letter
    if not any(c.isupper() for c in password):
        return False

    # Check if the password contains at least one lowercase letter
    if not any(c.islower() for c in password):
        return False

    # Check if the password contains at least one digit
    if not any(c.isdigit() for c in password):
        return False

    # Check if the password contains at least one special character
    if not re.search(r"[!@#$%^&*()\-_=+{}[\]:;,.<>?/\\|]", password):
        return False

    return True


def encrypt(text):
    hash = ""
    for c in text:
        hash += chr(int(ord(c)) + 100000)
    return str(hash)


def decrypt(text):
    hash = ""
    for c in text:
        hash += chr(int(ord(c)) - 100000)
    return str(hash)
