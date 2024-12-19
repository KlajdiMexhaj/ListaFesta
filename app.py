from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Initialize the app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_data.db'  # SQLite database
app.config['SECRET_KEY'] = 'supersecretkey'  # Required for Flask-Admin and flash messages
db = SQLAlchemy(app)

# Define the form data model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emer = db.Column(db.String(100), nullable=False)
    mbiemer = db.Column(db.String(100), nullable=False)
    confirmation = db.Column(db.String(10), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Set up the admin interface
class MyModelView(ModelView):
    # Allow the user to edit and delete records
    can_edit = False
    can_delete = False
    # Optionally, specify which columns should be displayed in the list view
    column_list = ('emer', 'mbiemer', 'confirmation')
    # Allow search by specific columns (optional)
    column_searchable_list = ('emer', 'mbiemer')

# Initialize Admin and add the User model to the admin panel
admin = Admin(app, name='Flask Admin', template_mode='bootstrap3')
admin.add_view(MyModelView(User, db.session))

# Define the route for the form
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        emer = request.form['emer']
        mbiemer = request.form['mbiemer']
        confirmation = request.form['confirmation']

        # Check if the name or surname already exists in the database
        existing_user = User.query.filter((User.emer == emer) | (User.mbiemer == mbiemer)).first()

        if existing_user:
            flash('Ky emër ose mbiemër janë regjistruar më parë. Ju lutem mos e dërgoni përsëri.', 'warning')
            return redirect(url_for('form'))

        # Create a new user and save to the database
        new_user = User(emer=emer, mbiemer=mbiemer, confirmation=confirmation)
        db.session.add(new_user)
        db.session.commit()

        # Display a success message
        flash('Faleminderit që konfirmuat!', 'success')

        return redirect(url_for('form'))  # Redirect back to the form to show the message

    return render_template('index.html')  # Change here to use 'index.html'

if __name__ == '__main__':
    app.run(debug=True)
