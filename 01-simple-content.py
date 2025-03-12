import ollama
import requests

from pypdf import PdfReader
from IPython.display import Markdown

## Download the PDF
def download_pdf(url, output_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"PDF downloaded successfully: {output_path}")
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")

### simple url and saving of file locally
pdf_url = "https://www.fratellinos.com/wp-content/uploads/2024/11/Lunch2024.pdf"
output_file = "menu.pdf"

download_pdf(pdf_url, output_file)


def load_pdf_text(file_path):
    '''Loads text from a PDF file.'''
    reader = PdfReader(file_path)

    # extracting text from page
    pdf_contents = "\n\n".join([page.extract_text() for page in reader.pages])
    
    return pdf_contents
    
pdf_contents = load_pdf_text('menu.pdf')

def ask_llama(question, context):
    prompt = f"""
    Consider the following context:
    {context}

    Answer the following question:
    {question}
    
    Be sure to look at the menu to offer a review.
    """
    response = ollama.chat(
        # using llama3.3 takes a lot of memory so llama3.2 works
        model='llama3.2', 
        messages=[
            {'role': 'user', 'content': prompt},
        ]
    )
    
    return response['message']['content']

question = "What are some of the foods on the menu?"
answer = ask_llama(question, pdf_contents)
Markdown(answer)

print(answer)