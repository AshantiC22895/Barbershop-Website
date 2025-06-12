'''This is my first Real World Project for a Client in Hattiesburg,Ms and we gonna break down each and every step and process including the variable to understand on what im doing and 
it will help me practice for future projects down the line

So We just install Flask, built my first rout(/), and ran a web server

from flask import Flask
This imports the Flask class from the Flask library.

You need this to create a Flask app.

Think of it like:
"I'm telling Python I want to use Flask to build a web app."

app = Flask(__name__)
This creates an instance of your Flask app.

__name__ tells Flask where to find your files (used to locate templates/static files).

Shortcut to remember:
app = Flask(__name__) means
"Hey Flask, this file is my web app. Start here."

@app.route('/')
This is called a route decorator.

'/' means this function will run when someone visits the homepage.

Think of it like:
"If someone visits /, show them this."

def home():
You're defining a function called home.

This function controls what happens at the homepage ('/').

return "<h1>Welcome to the Barbershop Website!</h1>"
This sends back HTML to the browser.

This is what the visitor sees when they go to your site.

if __name__ == '__main__':
This checks if you're running this file directly (not importing it).

It’s a Python best practice.

app.run(debug=True)
This starts the Flask server.

debug=True means:

If there's an error, Flask will show it

The server will reload when you change code
'''
from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Cocroft5!",  # Consider using environment variables for production
    database="barbershop_db"
)
cursor = db.cursor()

# Constants
SERVICE_DURATIONS = {
    "KIDS Cutz (Age 1-12)": 30,
    "Beard trim": 15,
    "Haircut": 30,
    "Haircut & Shave": 30,
    "Line": 15,
    "Line and Shave": 30,
    "Senior Cut": 30
}

BARBERS = ["Mr. J", "Jarvis “Fade King”"]

# Utility: Generate available slots
def get_available_slots(barber, selected_date, duration_minutes):
    opening_time = datetime.combine(selected_date, datetime.strptime("09:00", "%H:%M").time())
    closing_time = datetime.combine(selected_date, datetime.strptime("17:00", "%H:%M").time())
    slots = []

    cursor.execute("SELECT appointment_time FROM bookings WHERE barber=%s AND DATE(appointment_time)=%s", (barber, selected_date))
    taken = [row[0] for row in cursor.fetchall()]

    current = opening_time
    while current + timedelta(minutes=duration_minutes) <= closing_time:
        overlap = any(abs((current - t).total_seconds()) < duration_minutes * 60 for t in taken)
        if not overlap:
            slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=15)
    return slots

# Routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    services = list(SERVICE_DURATIONS.keys())
    slots = []

    if request.method == 'POST':
        name = request.form["name"]
        barber = request.form["barber"]
        service = request.form["service"]
        appointment_time = request.form["appointment_time"]

        cursor.execute(
            "INSERT INTO bookings (name, barber, service, appointment_time) VALUES (%s, %s, %s, %s)",
            (name, barber, service, appointment_time)
        )
        db.commit()
        return render_template("confirmation.html", name=name, service=service, time=appointment_time)

    # For GET method — check availability
    selected_service = request.args.get("service")
    selected_barber = request.args.get("barber")
    selected_date_str = request.args.get("date")

    if selected_service and selected_barber and selected_date_str:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        duration = SERVICE_DURATIONS.get(selected_service, 30)
        slots = get_available_slots(selected_barber, selected_date, duration)

    return render_template(
        "book.html",
        services=services,
        barbers=BARBERS,
        slots=slots
    )

@app.route('/bookings')
def bookings():
    cursor.execute("SELECT * FROM bookings")
    all_bookings = cursor.fetchall()
    return render_template("bookings.html", bookings=all_bookings)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cursor.execute("DELETE FROM bookings WHERE id = %s", (id,))
    db.commit()
    return redirect('/bookings')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/barbers')
def barbers():
    return render_template('barbers.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)



''' 
Lesson 2: HTML Templates with Jinja2 + Routing
Goal:
Replace raw HTML in Python with real .html files

Use Flask’s template engine (Jinja2) to render HTML pages

Set up a basic homepage layout

Step 1: Create Folder Structure
In your project folder (barbershop/), create these folders:(in can go for any project, it)
In your project folder (barbershop/), create these folders:(in can go for any project, it)

barbershop/
├── app.py
├── templates/
│   └── index.html
Flask looks for HTML files in a folder called templates by default.'''

'''Lesson 3: Passing Data from Python to HTML using Jinja2
🎯 Goal:
Learn how to send variables (like barber names or services) from Flask to HTML

Use Jinja2, Flask’s built-in template engine, to display that data dynamically

🛠️ Step 1: Update app.py
Replace your current home() function with one that sends data to your template:

python
Copy code
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    barbers = ["Mike", "Jamal", "Eddie"]
    return render_template('index.html', barbers=barbers)

if __name__ == '__main__':
    app.run(debug=True)
🔍 Line-by-Line Breakdown:
python
Copy code
barbers = ["Mike", "Jamal", "Eddie"]
A list of barber names you want to show on the homepage.

python
Copy code
return render_template('index.html', barbers=barbers)
This tells Flask:
🧠 "Pass the barbers list into the HTML file so we can use it there."

🛠️ Step 2: Update index.html
Now open your templates/index.html and use Jinja2 syntax to loop through the barbers.

html
Copy code
<!DOCTYPE html>
<html>
<head>
    <title>Barbershop</title>
</head>
<body>
    <h1>Welcome to the Barbershop</h1>
    <p>Meet our barbers:</p>

    <ul>
        {% for barber in barbers %}
            <li>{{ barber }}</li>
        {% endfor %}
    </ul>
</body>
</html>
Jinja2 Template Breakdown:
{% for barber in barbers %}
This starts a loop in HTML, like a Python for loop.

It goes through each name in the list.

{{ barber }}
This prints out the name of each barber.

Use {{ }} to output any variable in HTML.

{% endfor %}
This ends the loop.

 What You Just Learned:
Concept	What It Does
render_template(..., variable=value)	Sends Python data to the HTML
{% for item in list %}	Loops through a list in the HTML
{{ variable }}	Prints data into the webpage

 Example: Show Services Too
Add this to your home() function:

python
Copy code
services = ["Haircut", "Shave", "Beard Trim"]
return render_template('index.html', barbers=barbers, services=services)
And in your HTML:

html
Copy code
<h2>Services</h2>
<ul>
  {% for service in services %}
    <li>{{ service }}</li>
  {% endfor %}
</ul>
'''

'''Lesson 4: Creating a Booking Form + Receiving User Input (POST Requests)
Goal:
Create a form in HTML to collect booking info (name, date, barber, service)

Use Flask to receive and process form data

Understand the difference between GET and POST

Step 1: Add a Booking Route in app.py
Update your app.py with a new route for booking:

python
Copy code
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    barbers = ["Mike", "Jamal", "Eddie"]
    return render_template('index.html', barbers=barbers)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        barber = request.form['barber']
        service = request.form['service']
        date = request.form['date']
        
        print(f"Booking received: {name}, {barber}, {service}, {date}")
        
        return f"<h2>Thanks {name}, your {service} with {barber} is booked for {date}!</h2>"

    barbers = ["Mike", "Jamal", "Eddie"]
    services = ["Haircut", "Shave", "Beard Trim"]
    return render_template('book.html', barbers=barbers, services=services)

if __name__ == '__main__':
    app.run(debug=True)
Step 2: Create book.html in the templates/ folder
html
Copy code
<!-- templates/book.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Book Appointment</title>
</head>
<body>
    <h1>Book an Appointment</h1>
    <form method="POST" action="/book">
        <label>Your Name:</label><br>
        <input type="text" name="name" required><br><br>

        <label>Choose a Barber:</label><br>
        <select name="barber">
            {% for barber in barbers %}
                <option value="{{ barber }}">{{ barber }}</option>
            {% endfor %}
        </select><br><br>

        <label>Choose a Service:</label><br>
        <select name="service">
            {% for service in services %}
                <option value="{{ service }}">{{ service }}</option>
            {% endfor %}
        </select><br><br>

        <label>Date and Time:</label><br>
        <input type="datetime-local" name="date" required><br><br>

        <button type="submit">Book Now</button>
    </form>
</body>
</html>
Line-by-Line Breakdown
@app.route('/book', methods=['GET', 'POST'])
This allows two types of requests:

GET: when someone visits the page to fill out the form

POST: when they submit the form

request.form['fieldname']
Reads data from the form submission.

You use this in POST to grab what the user entered.

form method="POST"
Tells the browser:
“When this form is submitted, send the data to Flask using POST.”

{{ barber }} / {{ service }}
These show the current value in each list (barbers and services) inside the dropdown.

What You Just Learned:
Concept	What It Does
method="POST"	Submits the form securely
request.form	Lets Flask read the input
select + option	Lets users pick from a dropdown
if request.method == 'POST'	Detects form submission'''


'''<!DOCTYPE html>
Tells the browser that this is an HTML5 document. Required at the top.

<html> and </html>
The root of the web page. All HTML lives inside these tags.

<head> and </head>
The <head> is for info about the page (title, styles, etc.)

Not visible in the browser window.

html
Copy code
<title>Book Appointment</title>
This sets the tab title in the browser.

<body> and </body>
The visible content on the page — headings, forms, buttons, etc.

<h1>Book an Appointment</h1>
A big heading. <h1> is the most important, boldest title on a page.

<form method="POST" action="/book">
Starts a form that sends data to /book using the POST method.

method="POST" is used when sending user input (like booking info).

action="/book" means the form data will be sent to the /book route in Flask.

Input 1: Name
html
Copy code
<label>Your Name:</label><br>
<input type="text" name="name" required><br><br>
<label> is text above the input box

<input type="text"> creates a single-line textbox

name="name" is the key Flask uses to access the value with request.form['name']

required makes the field mandatory

Input 2: Choose a Barber
html
Copy code
<label>Choose a Barber:</label><br>
<select name="barber">
    {% for barber in barbers %}
        <option value="{{ barber }}">{{ barber }}</option>
    {% endfor %}
</select><br><br>
<select> creates a dropdown menu

The {% for barber in barbers %} is a Jinja2 loop — it fills the dropdown with names from Python

Each <option> becomes a dropdown item:

html
Copy code
<option value="Mike">Mike</option>
Input 3: Choose a Service
html
Copy code
<label>Choose a Service:</label><br>
<select name="service">
    {% for service in services %}
        <option value="{{ service }}">{{ service }}</option>
    {% endfor %}
</select><br><br>
Works the same as the barber dropdown

Pulls services like "Haircut", "Shave", etc. from Python into the HTML

Input 4: Date and Time
html
Copy code
<label>Date and Time:</label><br>
<input type="datetime-local" name="date" required><br><br>
<input type="datetime-local"> gives the user a date+time picker

name="date" is how Flask knows where to find the input

Submit Button
html
Copy code
<button type="submit">Book Now</button>
A regular button that submits the form

Triggers the POST request to /book

Summary Table
Tag	Purpose
<form>	Defines where and how to send user data
method="POST"	Sends form data securely to the server
name="..."	Key that Flask uses to retrieve data
<input>	Field where users type or select info
<select> + <option>	Dropdown menus
{{ variable }}	Displays dynamic content (Jinja2)
{% for item in list %}	Loops through Python lists in HTML

'''

'''Lesson 5: Connecting Flask to MySQL and Saving Booking Data
Goal:
Connect your Flask app to a MySQL database

Create a table to store booking info

Save booking form data into the database

Step 1: Set Up MySQL Database & Table
First, create a database and table in MySQL for bookings.

If you have MySQL installed, open your MySQL shell or use a GUI tool like phpMyAdmin or MySQL Workbench, then run:

sql
Copy code
CREATE DATABASE barbershop_db;

USE barbershop_db;

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    barber VARCHAR(50),
    service VARCHAR(50),
    date DATETIME
);
🛠️ Step 2: Install Python MySQL Connector
Run this in your terminal (command line):

bash
Copy code
pip install mysql-connector-python
🛠️ Step 3: Update app.py to Connect and Save Data
Add imports and MySQL connection setup at the top:

python
Copy code
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
db = mysql.connector.connect(
    host="localhost",
    user="your_mysql_username",
    password="your_mysql_password",
    database="barbershop_db"
)
cursor = db.cursor()
Update your /book route to save data to the database:
python
Copy code
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        barber = request.form['barber']
        service = request.form['service']
        date = request.form['date']  # Format: 'YYYY-MM-DDTHH:MM'

        # Convert the date format if needed (remove the 'T')
        date = date.replace('T', ' ')

        # Insert data into MySQL table
        sql = "INSERT INTO bookings (name, barber, service, date) VALUES (%s, %s, %s, %s)"
        values = (name, barber, service, date)
        cursor.execute(sql, values)
        db.commit()

        return f"<h2>Thanks {name}, your {service} with {barber} is booked for {date}!</h2>"

    barbers = ["Mike", "Jamal", "Eddie"]
    services = ["Haircut", "Shave", "Beard Trim"]
    return render_template('book.html', barbers=barbers, services=services)
🔍 Explanation:
We connect to MySQL at the start, and get a cursor to run queries.

When the form is submitted (POST):

We get the user inputs

Format the date string for MySQL

Use an INSERT query to save the data

Commit the transaction with db.commit()'''


'''Lesson 6: Show All Bookings (View Data from MySQL)
Goal:
Create a new route to display all customer bookings

Use a MySQL SELECT query

Show the results in an HTML table

Step 1: Add a New Route in app.py
Inside your existing app.py, add this new route:

python
@app.route('/bookings')
def bookings():
    cursor.execute("SELECT name, barber, service, date FROM bookings")
    results = cursor.fetchall()
    return render_template('bookings.html', bookings=results)
🔍 What this does:
Runs a SELECT query to get all bookings

cursor.fetchall() gets all the results as a list of tuples

Passes that list to an HTML file called bookings.html

Step 2: Create bookings.html in templates/
Inside your templates folder, create a new file called bookings.html:

html
Copy code
<!DOCTYPE html>
<html>
<head>
    <title>All Bookings</title>
</head>
<body>
    <h1>All Bookings</h1>
    <table border="1">
        <tr>
            <th>Name</th>
            <th>Barber</th>
            <th>Service</th>
            <th>Date</th>
        </tr>
        {% for booking in bookings %}
        <tr>
            <td>{{ booking[0] }}</td>
            <td>{{ booking[1] }}</td>
            <td>{{ booking[2] }}</td>
            <td>{{ booking[3] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
Quick Breakdown of bookings.html:
Code	Meaning
<table>	Creates a table
<th>	Table header (bold title)
{% for booking in bookings %}	Loops through each booking
{{ booking[0] }}	Shows name (1st item in row)
{{ booking[1] }}	Shows barber
{{ booking[2] }}	Shows service
{{ booking[3] }}	Shows date'''

'''Lesson: Show All Bookings in a Table
We'll:

Create a new route in Flask

Fetch the bookings from the MySQL database

Show them in a simple HTML table

🗂️ Step 1: Add This Route to app.py
Put this below your /book route:

python
Copy
Edit
@app.route('/bookings')
def bookings():
    cursor.execute("SELECT * FROM bookings")
    all_bookings = cursor.fetchall()
    return render_template('bookings.html', bookings=all_bookings)
✅ This:

Gets every row from the bookings table

Sends the results to the bookings.html page

🗂️ Step 2: Create templates/bookings.html
Inside your templates folder, add:

html
Copy
Edit
<!DOCTYPE html>
<html>
<head>
    <title>All Appointments</title>
</head>
<body>
    <h1>All Bookings</h1>
    <table border="1" cellpadding="8">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Barber</th>
            <th>Service</th>
            <th>Date</th>
        </tr>
        {% for booking in bookings %}
        <tr>
            <td>{{ booking[0] }}</td>
            <td>{{ booking[1] }}</td>
            <td>{{ booking[2] }}</td>
            <td>{{ booking[3] }}</td>
            <td>{{ booking[4] }}</td>
        </tr>
        {% endfor %}
    </table>

    <br>
    <a href="/book">Book Another Appointment</a>
</body>
</html>
🧠 HTML Breakdown
Tag	Explanation
<table>	Displays all bookings in rows/columns
{% for booking in bookings %}	Loops through the list of bookings sent from Flask
{{ booking[1] }}	Displays each booking's name, barber, etc. by index'''


'''Lesson: Delete a Booking
We'll add a delete button next to each booking row.

🗂️ Step 1: Update bookings.html
Add this line inside your table row (right after the last <td>):

html
Copy
Edit
<td>
    <form action="/delete/{{ booking[0] }}" method="POST" onsubmit="return confirm('Are you sure you want to delete this booking?');">
        <button type="submit">Delete</button>
    </form>
</td>
✅ Now your full row looks like this:

html
Copy
Edit
<tr>
    <td>{{ booking[0] }}</td>
    <td>{{ booking[1] }}</td>
    <td>{{ booking[2] }}</td>
    <td>{{ booking[3] }}</td>
    <td>{{ booking[4] }}</td>
    <td>
        <form action="/delete/{{ booking[0] }}" method="POST" onsubmit="return confirm('Are you sure you want to delete this booking?');">
            <button type="submit">Delete</button>
        </form>
    </td>
</tr>
🧱 Step 2: Add the /delete/<id> Route to app.py
Add this below your /bookings route:

python
Copy
Edit
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cursor.execute("DELETE FROM bookings WHERE id = %s", (id,))
    db.commit()
    return redirect('/bookings')
✅ This:

Accepts a POST request from the delete form

Deletes the booking with the matching id

Redirects back to the bookings table'''