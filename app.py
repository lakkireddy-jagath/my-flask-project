# app.py
# This is your main Flask application file

from flask import Flask, jsonify # Import necessary components from the Flask library

# Create an instance of the Flask application
# __name__ is a special Python variable that gets the name of the current module.
# Flask uses it to determine the root path of the application.
app = Flask(__name__)

# Define a route for the home page.
# When a user navigates to the base URL (e.g., http://127.0.0.1:5000/),
# the 'home' function will be executed.
@app.route('/')
def home():
    """
    This function handles requests to the root URL of the web application.
    It simply returns a string as the response.
    """
    return "Welcome to the Flask Project! This is the home page."

# Define a route for a basic API endpoint.
# When a user navigates to /api (e.g., http://127.0.0.1:5000/api),
# the 'api_route' function will be executed.
@app.route('/api')
def api_route():
    data = {
        "message": "API response from the NEW branch!", # CHANGED message
        "version": "1.1",                               # CHANGED version
        "source_branch": "initial_commit",
        "status_new_branch": "updated"                  # ADDED a new key
    }
    return jsonify(data)

# This block checks if the script is being run directly (not imported as a module).
# If it is, the Flask development server will start.
if __name__ == '__main__':
    # app.run() starts the Flask development server.
    # debug=True: This enables debug mode.
    #   - If an error occurs, it provides a detailed traceback in the browser.
    #   - It automatically reloads the server whenever you save changes to your code,
    #     which is very convenient for development.
    app.run(debug=True)