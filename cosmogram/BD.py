from random import choice
from string import ascii_uppercase
import sqlite3
DATABASE = 'BD.db'


def get_db(BDD=None):
    global DATABASE
    if BDD is None:
        BDD = DATABASE
    db = sqlite3.connect(BDD)
    db.row_factory = sqlite3.Row
    # db.close()
    return db


def get_question(question, BDD=None):
    if BDD is None:
        db = get_db()
    else:
        db = get_db(BDD)
    data = db.execute(question).fetchall()
    data = [dict(ix) for ix in data]
    return data


def get_insert(question, BDD=None):
    if BDD is None:
        db = get_db()
    else:
        db = get_db(BDD)
    con = db.cursor()
    con.execute(question)
    db.commit()
    # data = [dict(ix) for ix in data]
    # return data


def gen_str(leng):
    return ''.join(choice(ascii_uppercase) for i in range(leng))