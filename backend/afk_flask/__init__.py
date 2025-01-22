from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# create db connection
def get_db():
    db = mysql.connector.connect(
            host='localhost',
            user='jcandrews2',
            password='jca2CC66.',
            database='AFK'
    )
    return db

# This function decorator defines what URL someone needs to type to access this endpoint
# In this case, someone accessing the URL "http://<PUBLIC IP>:8080/" will get this endpoint
@app.route('/')
def welcome():
    # All Flask routes need to return some data that the browser knows how to handle
    # This can be raw strings, serialized JSON, HTML content, etc.
    # The "render_template" function will load an HTML file from the "templates/" dir
    return render_template('index.html')

# Here's the function that will get called when someone accesses "http://<PUBLIC IP>:8080/messages/"
@app.route('/messages/')
def get_messages():
    # First, get a connection to the MySQL DB
    db = get_db()
    # Here's the MySQL command we want to run; this is just the string you'd type into a mysql session!
    sql_cmd = 'SELECT * FROM messages'
    # Then we need to get Cursor that we'll use to execute the command and fetch the results
    cursor = db.cursor()
    cursor.execute(sql_cmd)
    results = []
    # Each row in the SELECT result will have two pieces of data (corresponding to the two columns in my DB)
    for row in cursor.fetchall():
        # Since I want to return a raw string, I'll parse the tuple into a single string by accessing the elements
        results.append(f'Title: {row[0]}, Contents: {row[1]}')
    # Finally, join the strings for each record into a single string!
    # Note: browsers don't render "\n" as a linebreak - they use HTML rendering, so you need a <br/>
    return '<br/>'.join(results)


# Here's a route that supports two types of requests:
#   GET: this is the standard HTTP request type that requests data FROM the server,
#        unless otherwise specified, all routes support GET requests by default
#   POST: this is a different request type that sends data TO the server
@app.route('/submit/', methods=['GET', 'POST'])
def get_form():
    # the "request" variable (imported from flask) is a global variable that stores the current request data
    # One of the important attributes that it stores is what type of request we're currently processing!
    if request.method == 'GET':
        # If a user sends a GET request (by accessing the URL), give them back the blank form
        return render_template('form.html')
    elif request.method == 'POST':
        # However, if they send a POST request (from the submit button on the form), parse their data
        # All POST requests triggered by HTML <form> elements will store the data in a dict request.form
        title = request.form['title']
        contents = request.form['content']

        # Once we've retrieved the submitted form data, all that's left to do is load it into a MySQL INSERT
        db = get_db()
        cursor = db.cursor()
        # We can use string formatting to insert dynamic values into a fixed MySQL command
        # You'll need to update this command to match your table name and schema!
        sql = 'INSERT INTO messages (Title, Message) VALUES (%s, %s)'
        data = (title, contents)
        cursor.execute(sql, data)
        # Don't forget to commit your DB updates!
        db.commit()
        return "I'm not quite sure what to do here..."


# Note that we are running on port 8080 specifically here!!
app.run(host='0.0.0.0', port=8080, debug=True)

