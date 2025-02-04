import os
import csv
from PIL import Image
from datetime import datetime
from dotenv import load_dotenv
import base64
from openai import OpenAI
import mimetypes

# Load environment variables
load_dotenv()

class FBMarketplaceBot:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.required_fields = [
            'TITLE',
            'PRICE',
            'CONDITION',
            'DESCRIPTION',
            'CATEGORY'
        ]
        self.conditions = ['New', 'Used - Like New', 'Used - Good', 'Used - Fair']
        
    def encode_image(self, image_path):
        """Encode image to base64."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
            
    def get_mime_type(self, image_path):
        """Get MIME type of image."""
        mime_type, _ = mimetypes.guess_type(image_path)
        return mime_type or 'application/octet-stream'
        
    def analyze_image(self, image_path):
        """Analyze image using GPT-4 and return structured furniture listing data."""
        system_prompt = """
        You are a furniture listing expert. Analyze the furniture image and provide the following details in a structured format:
        1. Title (up to 150 characters)
        2. Suggested price in USD (whole number)
        3. Condition (choose from: New, Used - Like New, Used - Good, Used - Fair)
        4. Detailed description: Make sure to include the dimensions of the furniature. Also add that I can deliver for a fee (up to 5000 characters)
        5. Category (use format: Furniture/[Subcategory])
        
        Return the data in this exact format:
        TITLE: [title]
        PRICE: [price]
        CONDITION: [condition]
        DESCRIPTION: [description]
        CATEGORY: [category]
        """
        
        try:
            img_type = self.get_mime_type(image_path)
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Updated to use the vision model
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Please analyze this furniture image and provide listing details."},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:{img_type};base64,{self.encode_image(image_path)}"},
                            },
                        ],
                    }
                ],
                max_tokens=1000
            )
            return self.parse_response(response.choices[0].message.content)
        except Exception as e:
            print(f"Error analyzing image {image_path}: {e}")
            return None
            
    def parse_response(self, response_text):
        """Parse the structured response into a dictionary."""
        result = {}
        current_field = None
        
        for line in response_text.split('\n'):
            if line.strip():
                if ':' in line:
                    field, value = line.split(':', 1)
                    field = field.strip().upper()
                    if field in self.required_fields:
                        result[field] = value.strip()
                elif current_field:
                    result[current_field] += ' ' + line.strip()
                    
        return result
        
    def process_folder(self, folder_path, output_csv):
        """Process all images in a folder and create a CSV file."""
        # Create CSV file with headers
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.required_fields)
            writer.writeheader()
            
            # Process each image in the folder
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    image_path = os.path.join(folder_path, filename)
                    print(f"Processing {filename}...")
                    
                    # Analyze image and write results
                    result = self.analyze_image(image_path)
                    if result:
                        writer.writerow(result)
                        print(f"Successfully processed {filename}")
                    else:
                        print(f"Failed to process {filename}")

def main():
    # Initialize the bot
    api_key = os.getenv('OPENAI_API_KEY')
    bot = FBMarketplaceBot(api_key)
    
    # Set your input and output paths
    input_folder = "./data"  # folder containing furniture images
    output_csv = "./fb_marketplace_listings.csv"
    
    # Process the folder
    bot.process_folder(input_folder, output_csv)
    print(f"Processing complete. Results saved to {output_csv}")

if __name__ == "__main__":
    main()