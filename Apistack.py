import requests
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Stack Overflow Data', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1)

    def chapter_body(self, link, view_count, profile_image):
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f'Question Link: {link}', 0, 1)
        self.cell(0, 10, f'View Count: {view_count}', 0, 1)
        self.image(profile_image, 10, self.get_y(), 25, 25)
        self.ln(30)

def extract_stackoverflow_data():



    # Define the API endpoint URL
    api_url = input('Enter your endpoint')

    # we first Set the parameters for the API request
    params = {
        'site': 'stackoverflow',
      
        'pagesize': 50  # Number of results per page
    }
        # we use try and exception to arest any error that may crasch our code 
    try:
        # Make the API request
        response = requests.get(api_url, params=params)

        # we write this line of code to Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            # to create a new PDF document
            pdf = PDF()

            # Set the document properties
            pdf.set_auto_page_break(auto=True, margin=15)

            # Extract the required information from the response
            for item in data['items']:
                question_link = item['link']
                question_title = item['title']
                view_count = item['view_count']
                profile_image = item['owner']['profile_image']

                # Add the extracted information to the PDF document
                pdf.add_page()
                pdf.chapter_title(question_title)
                pdf.chapter_body(question_link, view_count, profile_image)

            # Save the PDF document
            pdf.output('stackoverflow_data.pdf')
            print('task completed successfully')

        else:
            print('Error:', response.status_code)

    except requests.exceptions.RequestException as e:
        print('Error:', e)

# Call the function to extract Stack Overflow data and save as PDF
extract_stackoverflow_data()
