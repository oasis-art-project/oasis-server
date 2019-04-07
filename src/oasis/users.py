from flask import request
from .db import get_db

def create_user(user):
        get_db().execute('INSERT INTO users (first_name, last_name, email, user_password, user_role) Values (?, ?, ?, ?, ?)',
			(user["firstName"], user["lastName"], user["email"], user["password"], user["role"]))
	db.commit() 
        
        return user

def get_user(user_id):
	user = get_db().execute(
		'SELECT id, first_name, last_name, email, user_password, user_role FROM users WHERE id = ?',
		(user_id,)
	).fetchone()
	
	return user

def find_user(email):
        user = get_db().execute(
                'SELECT id, first_name, last_name, email, user_password, user_role FROM users WHERE email = ?',
                (email,)
        ).fetchone()

        return user

def edit_user(user_id):
	user = get_user(user_id)

	if request.method == 'POST':
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		email = request.form['email']
		user_password = request.form['user_password']
		user_role = request.form['user_role']  # an integer of 1 represents Admin, 2 is 								Host, 3 is Artist, 4 is Visitor
		error = None
		# some logic to check if the email is valid i.e. long enough, valid characters
		# some logic to check if the password is valid i.e. long enough, valid characters
		# some logic to check if the password matches when it is enterd a second time
		
		if not first_name:
			error = 'A first name must be provided'
		elif not last_name:
			error = 'A last name must be provided'
		elif not email:
			error = 'A valid email must be provided'
		elif not user_password:
			error = 'A valid password must be provided'
		elif not user_role:
			error = 'A valid role must be provided'
		else:
			db = get_db()
			db.execute(
				'UPDATE users SET first_name = ?, last_name = ?, email = ?, 					user_password = ?, user_role = ?'
				'WHERE id = ?',
				(user_id, first_name, last_name, email, user_password, user_role)
			)
			db.commit()
			# return redirect(url_for()) some url to take the user to after editing 
		# return render_template()

def delete_user(user_id):
	get_user(user_id)
	db = get_db()
	db.execute('DELETE FROM users WHERE id = ?', (user_id,))
	db.commit()
	# return redirect(url_for()) some url to take the user back to the guest home page
			
		




