import pdfplumber
import os

def read_oac_agenda(file_path):
    print(f"Opening {file_path}...")
    
    # Check if the file actually exists where we expect it
    if not os.path.exists(file_path):
        print("❌ Error: Could not find the PDF. Make sure it is in the project_data folder and named correctly.")
        return

    extracted_text = ""
    
    # Open the PDF using pdfplumber
    with pdfplumber.open(file_path) as pdf:
        print(f"✅ Successfully opened PDF. Found {len(pdf.pages)} pages.")
        
        # Loop through every page and extract the text
        for i, page in enumerate(pdf.pages):
            print(f"Reading page {i + 1}...")
            text = page.extract_text()
            
            if text:
                extracted_text += text + "\n"
    
    print("\n" + "="*50)
    print("EXTRACTION COMPLETE. HERE IS THE RAW TEXT:")
    print("="*50 + "\n")
    
    # Print the first 1000 characters just to prove it worked without flooding the terminal
    print(extracted_text[:1000])
    print("\n[... End of Preview ...]")

if __name__ == "__main__":
    # Point the script to the PDF you just uploaded
    target_file = "project_data/oac_agenda.pdf"
    read_oac_agenda(target_file)