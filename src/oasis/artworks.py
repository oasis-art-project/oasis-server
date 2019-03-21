from flask import request
from . import db

def create_artwork():
	event_name = request.form['event_name']
		artist_id = request.form['artist_id']
		art_name = request.form['art_name']
		description = request.form['description']
		photo = request.form['photo']
		error = None
		# art_id = some logic to generate an event ID
		# artist_id = the owner of the art's ID
		
		if not artist_id:
			error = 'An artist ID is required'
		elif not art_name:
			error = 'A name for the artwork is required'
		elif not photo:
			error = 'A photo must be provided for the artwork'
		else:
			db = get_db()
			db.execute(
				'INSERT INTO artworks (id, artist_id, art_name, description, 					photo)'	
				' Values (?, ?, ?, ?, ?)',
				(art_id, artist_id, art_name, description, photo)
			)
			db.commit()
			# return redirect(url_for()) some url to take the user to after submitting 				# an artwork
	# return render_template()


def get_artwork(art_id):
	artwork = get_db().execute(
		'SELECT id, artist_id, art_name, description, photo'
		'WHERE id = ?',
		(id,)
	).fetchone()

	if artwork is None:
		# abort(404, "Artwork ID {0} doesn't exist.".format(id)) code to handle failure
	return artwork

def edit_artwork(art_id):
	artwork = get_artwork(art_id)

	if request.method == 'POST':
		artist_id = request.form['artist_id']
		art_name = request.form['art_name']
		description = request.form['description']
		photo = request.form['photo']
		error = None
		
		if not artist_id:
			error = 'An artist ID is required'
		elif not art_name:
			error = 'A name for the artwork is required'
		elif not photo:
			error = 'A photo must be provided for the artwork'
		else:
			db = get_db()
			db.execute(
				'UPDATE artworks SET artist_id = ?, art_name = ?, description 					= ?, photo = ?'
				'WHERE id = ?',
				(art_id, artist_id, art_name, description, photo)
			)
			db.commit()
			# return redirect(url_for()) some url to take the user to after editing 			# an artwork
	# return render_template()

def delete_artwork(art_id):
	get_artwork(art_id)
	db = get_db()
	db.execute('DELETE FROM artworks WHERE id = ?', (art_id,))
	db.commit()
	# return redirect(url_for()) some url to take the user back to the relevant page

