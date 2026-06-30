from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Secret key for session management and flash messages
app.secret_key = 'edu_pulse_secret_key'

# MySQL Database Configurations
app.config['MYSQL_HOST'] = 'localhost'        # Database host (usually localhost)
app.config['MYSQL_USER'] = 'root'             # Database username (default is root)
app.config['MYSQL_PASSWORD'] = 'root'             # Database password (leave empty by default for local MySQL setup)
app.config['MYSQL_DB'] = 'studentdb'          # The name of our database

# Initialize MySQL connection using the configured Flask application
mysql = MySQL(app)


# ----------------- ROUTE 1: VIEW ALL STUDENTS (READ) -----------------
@app.route('/')
def index():
    """
    Renders the home page (student directory dashboard) 
    by fetching all records from the 'students' table.
    """
    try:
        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()
        
        # Execute query to fetch all student records
        cur.execute("SELECT * FROM students ORDER BY id DESC")
        data = cur.fetchall()
        
        # Close the connection cursor to free up resources
        cur.close()
        
        # Render index.html with the list of student records
        return render_template('index.html', students=data)
    
    except Exception as e:
        # Handle cases where database is not running or credentials are wrong
        flash(f"Database connection error: {str(e)}. Please check if your MySQL server is running and the database is created.", "danger")
        return render_template('index.html', students=[])


# ----------------- ROUTE 2: ADD NEW STUDENT (CREATE) -----------------
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    """
    GET: Displays the registration form to add a student.
    POST: Processes the form data and inserts a new student into the database.
    """
    if request.method == 'POST':
        # Retrieve form data submitted by the user
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        try:
            # Create a cursor to perform database insertion
            cur = mysql.connection.cursor()
            
            # Execute parameterized INSERT query to prevent SQL Injection
            cur.execute("INSERT INTO students (name, email, course) VALUES (%s, %s, %s)", (name, email, course))
            
            # Commit the transaction to save changes to the database
            mysql.connection.commit()
            
            # Close the connection cursor
            cur.close()

            # Display a success notification
            flash('Student registered successfully!', 'success')
            
            # Redirect back to the dashboard home page
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f"Error occurred while inserting student: {str(e)}", "danger")
            return redirect(url_for('index'))
            
    # If the request method is GET, just render the empty add form
    return render_template('add.html')


# ----------------- ROUTE 3: EDIT STUDENT DETAILS (UPDATE) -----------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    """
    GET: Fetches the student details by ID and renders them inside the form.
    POST: Updates the student details in the database using the submitted form.
    """
    try:
        cur = mysql.connection.cursor()
        
        if request.method == 'POST':
            # Retrieve updated form details
            name = request.form['name']
            email = request.form['email']
            course = request.form['course']
            
            # Execute parameterized UPDATE query
            cur.execute("UPDATE students SET name=%s, email=%s, course=%s WHERE id=%s", (name, email, course, id))
            mysql.connection.commit()
            cur.close()
            
            flash('Student details updated successfully!', 'success')
            return redirect(url_for('index'))
            
        else:
            # Execute SELECT query to fetch student details by ID
            cur.execute("SELECT * FROM students WHERE id = %s", (id,))
            student_data = cur.fetchone()
            cur.close()
            
            # Render the edit form, passing the student details to pre-populate inputs
            return render_template('edit.html', student=student_data)
            
    except Exception as e:
        flash(f"Error occurred: {str(e)}", "danger")
        return redirect(url_for('index'))


# ----------------- ROUTE 4: DELETE STUDENT (DELETE) -----------------
@app.route('/delete/<int:id>', methods=['GET'])
def delete_student(id):
    """
    Deletes the student matching the provided ID and redirects to the home page.
    """
    try:
        cur = mysql.connection.cursor()
        
        # Execute parameterized DELETE query
        cur.execute("DELETE FROM students WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        
        flash('Student record deleted successfully!', 'success')
        
    except Exception as e:
        flash(f"Error deleting record: {str(e)}", "danger")
        
    return redirect(url_for('index'))


# Run the Flask app
if __name__ == '__main__':
    # Set debug to True for auto-reload on changes
    app.run(debug=True)
    
