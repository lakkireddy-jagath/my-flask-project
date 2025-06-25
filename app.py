# app.py
# This is your main Flask application file

from flask import Flask, jsonify, render_template, request # Import necessary components from the Flask library

# Create an instance of the Flask application
# __name__ is a special Python variable that gets the name of the current module.
# Flask uses it to determine the root path of the application.
app = Flask(__name__)

# Define a route for the home page.
# When a user navigates to the base URL (e.g., http://127.0.0.1:5000/),
# the 'home' function will be executed.
# app.py (modified in master_1)
# ...

@app.route('/')
def home():
    return render_template('index.html') # Now renders the HTML file
# ...

# Define a route for a basic API endpoint.
# When a user navigates to /api (e.g., http://127.0.0.1:5000/api),
# the 'api_route' function will be executed.
# ...
# app.py (AFTER RESOLVING CONFLICT)
# ...
@app.route('/api')
def api_route():
    data = {
        "message": "API response from merged branches!", # New combined message
        "version": "1.1",                               # Version from new branch
        "source_branch": "initial_commit",
        "status_new_branch": "updated",                 # From new branch
        "status_main_branch": "modified"                # From main branch
    }
    return jsonify(data)
# ...
# ...

# This block checks if the script is being run directly (not imported as a module).
# If it is, the Flask development server will start.
if __name__ == '__main__':
    # app.run() starts the Flask development server.
    # debug=True: This enables debug mode.
    #   - If an error occurs, it provides a detailed traceback in the browser.
    #   - It automatically reloads the server whenever you save changes to your code,
    #     which is very convenient for development.
    app.run(debug=True)