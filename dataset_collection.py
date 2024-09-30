import os
import PyPDF2
import google.generativeai as genai
from api_key import GOOGLE_API_KEY
import csv
import json
import time
genai.configure(api_key=GOOGLE_API_KEY)


def textbook_path_generation():
    """ Creates a list of paths for each PDF textbook."""
    textbook_path_list = []
    directory = "Textbooks"
    

    # Iterate over files in directory
    for name in os.listdir(directory):
        # Appending path of textbook to list
            if name.endswith(".json"):  # Only include PDF files
                textbook_path_list.append(os.path.join(directory, name))

    return textbook_path_list


def append_to_csv(x, y, csv_filename="dataset.csv"):
    # Ensure both lists have the same length
    if len(x) != len(y):
        raise ValueError("Both lists must have the same length")
    
    # Open the CSV file in append mode
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Iterate over both lists and write rows
        for i in range(len(x)):
            writer.writerow([x[i], y[i]])


def main():
    # Creating lists
    textbook_content = []
    textbook_content_sumarised = []

    # Create the model
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash"  
    )

    # Grabbing textbook paths
    textbook_paths = textbook_path_generation()
    
    # Calling Gemini API
    prompt = "Give a detailed summary of these textbook content."
    count = 0
    for i in range(len(textbook_paths)):
        
        with open(textbook_paths[i], 'r')as file:
            textbook = json.load(file)
       
        for value in textbook.values():
            if count == 12:
                time.sleep(60)
                count = 0
            else:
                summarised_response = model.generate_content([prompt, value])
                textbook_content.append(value)
                textbook_content_sumarised.append(summarised_response.text)
                count += 1
                print(count)
            
            
      
        append_to_csv(textbook_content, textbook_content_sumarised)
        print("Finished a textbook")
        break
        
        

    
        

if __name__ == "__main__":
    main()