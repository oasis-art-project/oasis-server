from flask import request
from . import db

def create_event():
	if request.method == 'POST':
		event_name = request.form['event_name']
		description = request.form['description']
		start_date = request.form['start_date']
		end_date = request.form['end_date']
		photo = request.form['photo']
		error = None
		# event_id = some logic to generate an event id
		# place_id = the place id
		
		if not event_name:
			error = 'An event name is required'
		elif not start_date:
			error = 'A start date is required'
		else:
			db = get_db()
			db.execute(
				'INSERT INTO events (id, place_id, event_name, description, 					start_date, end_date, photo)'	
				' Values (?, ?, ?, ?, ?, ?, ?)',
				(event_id, place_id, event_name, description, start_date, 					end_date, photo)
			)
			db.commit()
			# return redirect(url_for()) some url to take the user to after submitting 				# an event
	# return render_template()

def get_event(id):
	event = get_db().execute(
		'SELECT e.id, place_id, event_name, description, start_date, end_date, photo'
		'WHERE e.id = ?',
		(id,)
	).fetchone()
	
	if event is None:
		# abort(404, "Event id {0} doesn't exist.".format(id)) code to handle falure
	
	return event

def edit_event(id):
	event = get_event(id)

	if request.method == 'POST':
		event_name = request.form['event_name']
		description = request.form['description']
		start_date = request.form['start_date']
		end_date = request.form['end_date']
		photo = request.form['photo']
		error = None
		
		if not event_name:
			error = 'An event name is required'
		elif not start_date:
			error = 'A start date is required'
		else:
			db = get_db()
			db.execute(
				'UPDATE events SET event_name = ?, description = ?, start_date 					= ?, end_date = ?, photo = ?'
				'WHERE id = ?',
				(event_id, place_id, event_name, description, start_date, 					end_date, photo)
			)
			db.commit()
			# return redirect(url_for()) some url to take the user to after submitting 				# an event
	# return render_template()

def delete_event(id):
	get_event(id)
	db = get_db()
	db.execute('DELETE FROM events WHERE id = ?', (id,))
	db.commit()
	# return redirect(url_for()) some url to take the user back to the home page
	

