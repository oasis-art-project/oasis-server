from flask import request
from . import db

def create_place():
	if request.method == 'POST':
		place_name = request.form['place_name']
		owner_id = None # some logic to determine who is submitting this form
		loc_lon = request.form['loc_lon']
		loc_lat = request.form['loc_lat']
		error = None
		place_id = None # some logic to generate a place id or will None cause sql to auto generate an ID?
		
		if not place_name:
			error = 'A place name is required'
		elif not owner_id:
			error = 'An owner ID is required'
		elif not loc_lon:
			error = 'A longitudinal coordinate corresponding to the location is 					required'
		elif not loc_lat:
			error = 'A latitudinal coordinate corresponding to the location is 					required'
		else:
			db = get_db()
			db.execute(
				'INSERT INTO places (id, place_name, owner_id, loc_lon, loc_lat)'
				'Values (?, ?, ?, ?, ?)',
				(place_id, place_name, owner_id, loc_lon, loc_lat)
			)
			db.commit()
			# return redirect(url_for()) some url to take the user to after submitting 				# a place
	# return render_template()

def get_place():
	place = get_db().execute(
		'SELECT id, place_name, owner_id, loc_lon, loc_lat'
		'WHERE id = ?',
		(place_id,)
	).fetchone()
	
	if place is None:
		# abort(404, "Place ID {0} doesn't exist.".format(id)) code to handle failure
	return place

def edit_place(place_id):
	place = get_place(plalce_id)
	
	if request.method == 'POST':
		place_name = request.form['place_name']
		owner_id = request.form['owner_id']
		loc_lon = request.form['loc_lon'] # should a user even be able to edit the 
						  # longitude or latitude? Shouldn't they just 							  # delete this place and create a new one if 							  # location changes?
		loc_lat = request.form['loc_lat']
		error = None

		if not place_name:
			error = 'A place name is required'
		elif not owner_id:
			error = 'An owner ID is required'
		elif not loc_lon:
			error = 'A longitudinal coordinate corresponding to the location is 					required'
		elif not loc_lat:
			error = 'A latitudinal coordinate corresponding to the location is 					required'
		else:
			db = get_db()
			db.execute(
				'UPDATE places SET place_name = ?, owner_id = ?, loc_lon = ?, 					loc_lat = ?'
				'WHERE id = ?',
				(place_id, place_name, owner_id, loc_lon, loc_lat)
			)
			db.commit()
			# return redirect(url_for()) some url to take the user to after editing
	# return render_template()

def delete_place(place_id):
	get_place(place_id)
	db = get_db()
	db.execute('DELETE FROM places WHERE id = ?', (placeid,))
	db.commit()
	# return redirect(url_for()) some url to take the user back to the relevant page


UPLOAD_FOLDER = '/places_uploads/'
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


        


