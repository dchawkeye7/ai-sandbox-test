import os
import requests
from dotenv import load_dotenv

# Load the hidden variables from the .env file
load_dotenv()

# Securely grab the Todoist token
TODOIST_TOKEN = os.getenv("TODOIST_API_TOKEN")

def create_todoist_task():
    print("Connecting to Todoist...")
    
    # The modern Todoist v1 API endpoint for creating tasks
    url = "https://api.todoist.com/api/v1/tasks"
    
    # Your digital ID badge
    headers = {
        "Authorization": f"Bearer {TODOIST_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # The actual task data we want the AI to eventually generate
    data = {
        "content": "AI Test: Review updated schedule for Surface Parking Lot H",
        "description": "This task was generated automatically by Python.",
        "due_string": "today",
        "priority": 4  # In the API, 4 is the highest priority (Red color)
    }
    
    # Send the POST request to create the task
    response = requests.post(url, json=data, headers=headers)
    
    # Check if it worked
    if response.ok:
        print("✅ Success! The task has been created.")
    else:
        print(f"❌ Connection Failed. Status code: {response.status_code}")
        print(f"Error details: {response.text}")

if __name__ == "__main__":
    create_todoist_task()