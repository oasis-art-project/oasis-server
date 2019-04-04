from flask import request
from .db import get_db

def create_user(data):
        return None
        """
        if request.method == 'POST':
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		email = request.form['email']
		user_password = request.form['user_password'] # MD5 hash this
		user_role = request.form['user_role'] # an integer of 1 represents Admin, 2 is 								Host, 3 is Artist, 4 is Visitor
		user_id = None # some logic to generate a user ID or will None cause sql to auto generate an ID?
		# some logic to check if the email is valid i.e. long enough, valid characters
		# some logic to check if the password is valid i.e. long enough, valid characters
		# some logic to check if the password matches when it is enterd a second time
		error = None
		
		if not first_name:
			error = 'A first name must be provided'
		elif not last_name:
			error = 'A last name must be provided'
		elif not email:
			error = 'A valid email must be provided'
		elif not user_password:
			error = 'A valid password must be provided' 
		elif not user_role:
			error = 'A valid user role must be provided'
		else:
			db = get_db()
			db.execute(
				'INSERT INTO users (id, first_name, last_name, email, 					user_password, user_role)'
				' Values (?, ?, ?, ?, ?, ?)',
				(user_id, first_name, last_name, email, user_password, user_role)
			)
			db.commit()
			# return redirect(url_for()) some url to take the user to the homepage
	# return render_template()
        """
def get_user(user_id):
	user = get_db().execute(
		'SELECT id, first_name, last_name, email, user_password, user_role'
		'WHERE id = ?',
		(user_id,)
	).fetchone()
	
	if user is None:
            return None
            # abort(404, "User ID {0} doesn't exist.".format(id)) code to handle failure
	return user

def find_user(email):
        user = get_db().execute(
                'SELECT id, first_name, last_name, email, user_password, user_role FROM users WHERE email = ?',
                (email,)
        ).fetchone()

        if user is None:
            return None

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
			
		

UPLOAD_FOLDER = '/users_uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
        if request.method == 'POST':
                # ensure the file has been provided
                if 'file' not in request.files:
                        flash('No file')
                        return redirect(request.url)
                file = request.files['file']
                # if the user does not provide a file, the browser will submit empty part w/o filename
                if file.filename == '':
                        flash('No selected file')
                        return redirect(request.url)
                if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename) # secure filename ensures for security reasons that the filename hasn't been forged
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        return redirect(url_for('uploaded_file', filename=filename))
                return '''
                <!doctype html>
                <title>Upload new File</title>
                <h1>Upload new File</h1>
                <form method=post enctype=multipart/form-data>
                      <input type=file name=file>
                      <input type=submit value=Upload>
                </form>
                '''
                # replace with frontend
@app.route('/uploads/<filename>')
def uploaded_file():
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


        




