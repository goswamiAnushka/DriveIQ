import json
import os

# Define the path where the history will be stored
HISTORY_FILE = 'DriveIQ-backend/data/journey_history.json'

def save_journey(prediction):
    """
    Saves the journey data (prediction result) to the journey history file.
    """
    if not os.path.exists(HISTORY_FILE):
        # If file doesn't exist, create it with an empty list
        with open(HISTORY_FILE, 'w') as f:
            f.write("[]")  # Initialize the file with an empty list

    with open(HISTORY_FILE, 'r+') as f:
        data = json.load(f)  # Load existing history
        data.append(prediction)  # Append new journey prediction
        f.seek(0)  # Move the file pointer to the start of the file
        json.dump(data, f, indent=4)  # Save the updated history

def get_journey_history():
    """
    Retrieves the journey history stored in the journey history file.
    """
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
            return history
    except FileNotFoundError:
        return []  # If the file doesn't exist, return an empty list
