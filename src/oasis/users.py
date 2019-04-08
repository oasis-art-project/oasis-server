from flask import request
from .db import get_db

"""
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
"""

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
    data = db.execute('UPDATE users SET first_name = ?, last_name = ?, email = ?, user_password = coalesce(?, user_password), user_role = ? WHERE id = ?', (user['firstName'], user['lastName'],user['email'], user.get('password',None), user['role'], user['id']))
    db.commit()
    
    return data

def delete_user_by_email(email):
    db = get_db()
    data = db.execute('DELETE FROM users WHERE email = ?', (email,))
    db.commit()

    return data
