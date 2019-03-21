from flask import request
from . import db

def create_place():
	if request.method == 'POST':
		place_name = request.form['place_name']
		owner_id = request.form['owner_id']
		loc_lon = request.form['loc_lon']
		loc_lat = request.form['loc_lat']
		error = None
		# place_id = some logic to generate a place id
		
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
		
