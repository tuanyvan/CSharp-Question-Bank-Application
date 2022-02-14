#! python3

# Import PDFMiner and other relevant files
from statistics import correlation
from types import NoneType
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from io import StringIO

import re

# Create Question class
class Question:

    def __init__(self, regex_match : str):
        self.regex_match = regex_match

        # Store all fields as strings parse from regex matching.
        self.question = re.match('[1-9]\. (.+\n)', self.regex_match)[1]
        self.answers = ''.join(re.findall('[a-e]\).+\n*', self.regex_match))
        self.correct_answer = ''.join(re.findall('Answer: ([a-e]|True\.(?:.+\.)*(?:.+\n.+)?|False\.(?:.+\.)*(?:.+\n.+)?)', self.regex_match))

# Read the PDF using pdfminer docs.
question_bank = StringIO()
with open('questions.pdf', 'rb') as input_file:

    # Fetch PDF object from stream
    parser = PDFParser(input_file)
    # Parse documentation with dynamic data import
    doc = PDFDocument(parser)
    # Create resource allocator for fonts and images
    rsrcmgr = PDFResourceManager()
    # Build the text conversion object using resource allocator, question_bank, and default layout parameters.
    device = TextConverter(rsrcmgr, question_bank, laparams=LAParams())

    # Build interpreter using information gathered above.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)

# Parse every question and answer from PDF using Regex
question_regex = r'[1-9]\. (?:.+\n){1,2}(?:(?:[a-e]\).+\n)*)?Answer: (?:[a-e]|True\.(?:.+\.)*|False\.(?:.+\.)*(?:.+\n.+)?)'
question_matches = re.findall(question_regex, question_bank.getvalue())
print(f'{len(question_matches)} questions were found.')

# Pass each Regex match to Question class for further parsing
questions = []
for index, match in enumerate(question_matches):
    questions.append(Question(match))
    print(repr(questions[index].correct_answer))

# Use the instance variables from Question class to fill out a CSV or equivalent file for question/answer storage.
