from flask import request
from .db import get_db

def find_user_by_id(user_id):
    user = get_db().execute('SELECT id, first_name, last_name, email, user_password, user_role FROM users WHERE id = ?',(user_id,)
    ).fetchone()
	
    return user

def find_user_by_email(email):
    user = get_db().execute('SELECT id, first_name, last_name, email, user_password, user_role FROM users WHERE email = ?',(email,)
    ).fetchone()

    return user

def create_user(user):
    db = get_db()
    user = db.execute('INSERT INTO users (first_name, last_name, email, user_password, user_role) Values (?, ?, ?, ?, ?)', (user["firstName"], user["lastName"], user["email"], user["password"], user["role"]))
    db.commit()
    
    return user

def edit_user(user):
    db = get_db()
    data = db.execute('UPDATE users SET first_name = ?, last_name = ?, email = ?, user_password = ?, user_role = ? WHERE id = ?', (user['firstName'], user['lastName'],user['email'], user['password'], user['role'], user['id']))
    db.commit()
    
    return data

def delete_user_by_email(email):
    db = get_db()
    data = db.execute('DELETE FROM users WHERE email = ?', (email,))
    db.commit()

    return data
