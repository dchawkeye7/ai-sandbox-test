import os
import requests
import pdfplumber
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the vault
load_dotenv()
TODOIST_TOKEN = os.getenv("TODOIST_API_TOKEN")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_pdf_text(file_path):
    print(f"📄 Reading {file_path}...")
    if not os.path.exists(file_path):
        print("❌ Error: Could not find the PDF.")
        return None

    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

def analyze_minutes(raw_text):
    print("🧠 AI is hunting for your action items...")
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # We give the AI stricter formatting rules so Python can easily read the output
    prompt = f"""
    You are a highly capable Assistant Project Manager reading an OAC meeting agenda. 
    
    Your mission: 
    Extract ALL action items from the text, regardless of who they are assigned to. 
    For each item, identify the "Ball in Court" (the specific person, trade, or entity responsible for completing it).
    
    CRITICAL FORMATTING RULE: 
    Output each action item on its own separate line using exactly this format:
    [Ball in Court] - [Action Item Description]
    
    Example: 
    [Electrical Contractor] - Submit revised switchgear shop drawings.
    [Steven] - Review and approve RFI #42.
    
    Do NOT use bullet points, asterisks, or numbered lists. 
    Do NOT include any introductory or concluding text. Return ONLY the formatted lines.
    
    RAW MEETING TEXT:
    {raw_text}
    """
    
    response = model.generate_content(prompt)
    
    # Split the AI's text block into a neat Python list of individual tasks
    task_list = [task.strip() for task in response.text.strip().split('\n') if task.strip()]
    
    print(f"✅ Found {len(task_list)} action items.")
    return task_list

def send_to_todoist(task_text):
    url = "https://api.todoist.com/api/v1/tasks"
    
    headers = {
        "Authorization": f"Bearer {TODOIST_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "content": task_text,
        "due_string": "today",
        "priority": 4 
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.ok:
        print(f"  -> 🟢 Sent to Todoist: {task_text[:50]}...")
    else:
        print(f"  -> 🔴 Failed to send: {task_text[:50]}...")

if __name__ == "__main__":
    # 1. Point to your file
    target_file = "Minutes/sampleminutes.pdf"  # <-- Make sure this matches your PDF name
    
    # 2. Extract the text
    extracted_text = extract_pdf_text(target_file)
    
    if extracted_text:
        # 3. Have the AI pull the specific tasks
        tasks = analyze_minutes(extracted_text)
        
        # 4. Loop through the AI's list and send each one to your phone
        print("\n🚀 Pushing to Todoist...")
        for task in tasks:
            send_to_todoist(task)
            
        print("\n🎉 WORKFLOW COMPLETE!")