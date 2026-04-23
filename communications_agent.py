import urllib.parse

def generate_outlook_draft(to_email, subject, body):
    print("🖨️ Generating Outlook Draft Link...")
    
    # We have to "URL encode" the text so spaces and paragraphs don't break the link
    safe_subject = urllib.parse.quote(subject)
    safe_body = urllib.parse.quote(body)
    
    mailto_link = f"mailto:{to_email}?subject={safe_subject}&body={safe_body}"
    
    print("\n✅ Success! Ctrl+Click (or Cmd+Click) the link below to open your Outlook draft:\n")
    print(mailto_link)

# --- TEST THE GENERATOR ---
if __name__ == "__main__":
    test_recipient = "contractor@example.com" 
    test_subject = "Action Required: RFI #42 Update"
    test_body = """Good morning,
    
Please provide an update on the RFI submitted yesterday regarding the switchgear specs.

Best,
Assistant PM Bot"""
    
    generate_outlook_draft(test_recipient, test_subject, test_body)