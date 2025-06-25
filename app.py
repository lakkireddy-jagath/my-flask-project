# app.py
# This file contains the complete Flask application, including:
# - A home page that renders an HTML To-Do form.
# - A basic API endpoint.
# - A backend route to submit and store To-Do items in MongoDB.
# - MongoDB connection setup.

from flask import Flask, jsonify, render_template, request # Import necessary Flask components
from pymongo import MongoClient           # Import MongoClient for MongoDB connection
from pymongo.errors import ConnectionFailure # Import for handling MongoDB connection errors
import os                                 # Import os for environment variables (for MongoDB URI)
import datetime                           # Import datetime for adding timestamps to To-Do items

# Create an instance of the Flask application
# __name__ helps Flask find resources like templates relative to this file.
app = Flask(__name__)

# --- MongoDB Connection Configuration ---
# It's highly recommended to use environment variables for sensitive information
# like database connection strings in a real application.
# For this assignment, we provide a default for a local MongoDB instance.
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "todo_app_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "todo_items")

# Global variable to hold the MongoClient instance.
# Initialized to None, will be set upon first successful connection attempt.
client = None

def get_mongo_collection():
    """
    Establishes and returns a connection to the MongoDB collection.
    It attempts to connect only once and reuses the client.
    Handles connection failures gracefully.
    """
    global client # Declare intent to modify the global 'client' variable
    if client is None: # If client is not yet established
        try:
            client = MongoClient(MONGO_URI)
            # The ismaster command is a lightweight way to check if the connection is active.
            client.admin.command('ismaster')
            print("MongoDB connected successfully!")
        except ConnectionFailure as e:
            # If connection fails, print an error and reset client to None
            print(f"MongoDB connection failed: {e}")
            client = None
            return None # Indicate failure by returning None

    # If connection is successful (or already established), return the collection
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

# --- Flask Routes ---

@app.route('/')
def home():
    """
    Handles requests to the root URL (e.g., http://127.0.0.1:5000/).
    Renders the 'index.html' template which contains the To-Do form.
    This part was developed in the master_1 branch.
    """
    return render_template('index.html')

@app.route('/api')
def api_route():
    """
    Handles requests to the /api URL (e.g., http://127.0.0.1:5000/api).
    Returns a JSON response with information.
    This route's content reflects the resolution of the merge conflict from Part 2.
    """
    data = {
        "message": "API response from merged branches!", # Message from conflict resolution
        "version": "1.1",                               # Version from new branch in Part 2
        "source_branch": "initial_commit",              # Original source indication
        "status_new_branch": "updated",                 # Key from new branch in Part 2
        "status_main_branch": "modified"                # Key from main branch in Part 2
    }
    return jsonify(data)

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    """
    Handles POST requests to the /submittodoitem URL.
    This route receives To-Do item data from the frontend form and stores it in MongoDB.
    This part was developed in the master_2 branch.
    """
    # Extract data from the POST request form.
    # 'request.form.get()' is used to safely retrieve form field values.
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')

    # Basic server-side validation: ensure 'Item Name' is not empty.
    if not item_name:
        return jsonify({"status": "error", "message": "Item Name is required"}), 400 # 400 Bad Request

    # Attempt to get the MongoDB collection.
    collection = get_mongo_collection()
    if collection is None:
        # If the MongoDB connection failed, return an appropriate error response.
        return jsonify({"status": "error", "message": "Failed to connect to database"}), 500 # 500 Internal Server Error

    try:
        # Create a dictionary representing the To-Do item to be stored.
        # Includes a timestamp for when the item was created.
        todo_item = {
            "itemName": item_name,
            "itemDescription": item_description,
            "timestamp": datetime.datetime.now() # Adds the current date and time
        }
        # Insert the new To-Do item into the MongoDB collection.
        result = collection.insert_one(todo_item)
        # Return a success response, including the unique ID generated by MongoDB.
        return jsonify({
            "status": "success",
            "message": "To-Do item added successfully!",
            "item_id": str(result.inserted_id) # Convert MongoDB's ObjectId to string for JSON
        }), 201 # 201 Created status code indicates successful resource creation
    except Exception as e:
        # Catch any other unexpected errors during the database operation.
        return jsonify({"status": "error", "message": f"An error occurred during submission: {e}"}), 500

# --- Application Entry Point ---
if __name__ == '__main__':
    # This block executes when the script is run directly (e.g., 'python app.py').
    # It starts the Flask development server.
    # debug=True:
    # - Provides detailed error messages in the browser if something goes wrong.
    # - Automatically reloads the server when you save changes to your code, which is
    #   very convenient during development.
    app.run(debug=True)