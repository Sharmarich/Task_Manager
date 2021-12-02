# Author - Richa 

from flask import Flask, render_template,redirect,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

# CREATING SERVER
app = Flask(__name__)

# SETTING UP DATABASE
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///initial_database.db'
db = SQLAlchemy(app)

# THIS IS FOR BOOTSTRAP LIBRARY
bootstrap = Bootstrap(app)

# THERE IS ONLY ONE TABLE WITH TASKLIST
class NewWatch(db.Model):
	watch_id = db.Column(db.Integer,primary_key=True)
	task = db.Column(db.String(100),nullable=False)

	def __repr__(self):
		return '<Watch %r >' % self.watch_id

@app.route('/',methods=['GET','POST'])
def index():
	if request.method == 'POST':
		# CREATES ENTRY FOR TASK
		watch_task = request.form['task']
		newWatch = NewWatch(task=watch_task)
		try:
			db.session.add(newWatch)
			db.session.commit()
			return redirect('/')

		except Exception:
			return 'There was an issue updating database'
	else:
		# THIS IS GET REQUEST
		# THIS SHOWS ALL TASKS THAT ARE CURRENTLY AVAILABLE
		watchlist = NewWatch.query.order_by(NewWatch.watch_id).all()
		return render_template('index.html',watchlist=watchlist)

@app.route('/delete/<int:watch_id>')
def delete(watch_id):
	# DELETES TASK ENTRY
	taskToDelete = NewWatch.query.get_or_404(watch_id)
	try:
		db.session.delete(taskToDelete)
		db.session.commit()
		return redirect('/')

	except Exception:
		return 'Error in deleting'

if __name__ == '__main__':
	# Running the web app in debug mode    
	app.run(port=4004, debug=False, host='0.0.0.0')