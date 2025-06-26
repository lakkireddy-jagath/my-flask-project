# app.py
# This file contains the complete Flask application for the To-Do app.
# It integrates features from Part 1 (initial setup), Part 2 (API route conflict resolution),
# and Part 3 (frontend HTML rendering and backend MongoDB integration).

from flask import Flask, jsonify, render_template, request # Necessary Flask components
from pymongo import MongoClient           # For connecting to MongoDB
from pymongo.errors import ConnectionFailure # For handling MongoDB connection errors
import os                                 # For reading environment variables (MongoDB URI)
import datetime                           # For adding timestamps to To-Do items

# Create an instance of the Flask application
app = Flask(__name__)

# --- MongoDB Connection Configuration ---
# These variables define how your Flask app connects to MongoDB.
# MONGO_URI: The connection string for your MongoDB server.
#            It first checks for an environment variable named "MONGO_URI".
#            If not found, it defaults to "mongodb://localhost:27017/"
#            which is the standard URI for a local MongoDB instance.
# DB_NAME: The name of the database where To-Do items will be stored.
# COLLECTION_NAME: The name of the collection (similar to a table in SQL)
#                  within the database where individual To-Do items will reside.
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "todo_app_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "todo_items")

# A global variable to store the MongoDB client instance.
# This ensures that a new connection isn't established for every request,
# promoting efficient resource usage. It's initialized to None.
client = None

def get_mongo_collection():
    """
    Establishes and returns a connection to the specified MongoDB collection.
    It's designed to connect only once and reuse the established client connection.
    Includes basic error handling for connection failures.
    """
    global client # Declare that we intend to modify the global 'client' variable

    # If the client is not yet established (first call or previous connection failed)
    if client is None:
        try:
            # Attempt to connect to MongoDB using the configured URI
            client = MongoClient(MONGO_URI)
            # The 'admin.command('ismaster')' is a lightweight operation to verify
            # that the connection is active and MongoDB is reachable.
            client.admin.command('ismaster')
            print("MongoDB connected successfully!") # Log success to console
        except ConnectionFailure as e:
            # If a connection error occurs, print the error and reset the client
            print(f"MongoDB connection failed: {e}")
            client = None # Reset client so it tries to reconnect on next call
            return None   # Indicate failure by returning None

    # If the client is established (either new connection or reused),
    # get the specific database and then the collection.
    db = client[DB_NAME]
    return db[COLLECTION_NAME] # Return the collection object for database operations

# --- Flask Routes (Application Endpoints) ---

@app.route('/')
def home():
    """
    Handles requests to the application's root URL (e.g., http://127.0.0.1:5000/).
    This route renders the 'index.html' template located in the 'templates/' directory.
    This functionality comes from the 'master_1' branch.
    """
    return render_template('index.html')

@app.route('/api')
def api_route():
    """
    Handles requests to the '/api' endpoint (e.g., http://127.0.0.1:5000/api).
    Returns a JSON response. The content of this response reflects the resolution
    of the merge conflict from Part 2, combining changes from different branches.
    """
    data = {
        "message": "API response from merged branches!", # A new, combined message after conflict resolution
        "version": "1.1",                               # Version picked from the '_new' branch's changes
        "source_branch": "initial_commit",              # Original indicator from initial commit
        "status_new_branch": "updated",                 # New key added by the '_new' branch
        "status_main_branch": "modified"                # New key added by the 'main' branch directly
    }
    # jsonify converts the Python dictionary into a proper JSON HTTP response.
    return jsonify(data)

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    """
    Handles POST requests to the '/submittodoitem' endpoint.
    This route receives To-Do item data submitted from the frontend form (index.html)
    and persists it into the MongoDB database.
    This functionality comes from the 'master_2' branch.
    """
    # Extract form data sent via the POST request.
    # 'request.form.get()' is a safe way to retrieve values, returning None if key is not found.
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')

    # Server-side validation: Ensure that 'Item Name' is provided.
    if not item_name:
        # If 'itemName' is missing, return a JSON error response with a 400 Bad Request status.
        return jsonify({"status": "error", "message": "Item Name is required"}), 400

    # Attempt to get the MongoDB collection.
    collection = get_mongo_collection()
    if collection is None:
        # If there's no successful connection to MongoDB, return a 500 Internal Server Error.
        return jsonify({"status": "error", "message": "Failed to connect to database"}), 500

    try:
        # Construct a dictionary representing the To-Do item to be saved.
        # Includes a timestamp for when the item was created.
        todo_item = {
            "itemName": item_name,
            "itemDescription": item_description,
            "timestamp": datetime.datetime.now() # Adds the current date and time (from server)
        }
        # Insert the new To-Do item document into the MongoDB collection.
        # 'insert_one' returns an InsertOneResult object, which contains the 'inserted_id'.
        result = collection.insert_one(todo_item)

        # Return a success JSON response to the client.
        # Include the unique '_id' generated by MongoDB for the new document (converted to string).
        return jsonify({
            "status": "success",
            "message": "To-Do item added successfully!",
            "item_id": str(result.inserted_id) # Convert MongoDB's ObjectId to string for JSON output
        }), 201 # 201 Created HTTP status code: indicates that a new resource has been successfully created.
    except Exception as e:
        # Catch any other unexpected errors that might occur during the database operation
        # or data processing, and return a generic 500 error.
        return jsonify({"status": "error", "message": f"An error occurred during submission: {e}"}), 500

# --- Application Entry Point ---
# This block ensures that the Flask development server runs only when
# the 'app.py' script is executed directly (e.g., by typing 'python app.py' in the terminal),
# and not when it's imported as a module into another script.
if __name__ == '__main__':
    # Start the Flask development server.
    # debug=True:
    #   - Enables interactive debugger in the browser for detailed error messages.
    #   - Automatically reloads the server when code changes are detected, which is
    #     highly convenient during active development.
    # Make sure your MongoDB service is running on localhost:27017 for this app to connect.
    app.run(debug=True)