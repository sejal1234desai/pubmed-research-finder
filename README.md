A Django Web App and CLI tool for searching and extracting research papers from PubMed. The tool retrieves metadata such as authors, affiliations, and corresponding author emails. Additionally, it identifies non-academic authors based on predefined heuristics.

🔐Features:
Search PubMed Articles by keyword
Extract Author & Affiliation Details
Identify Non-Academic Authors
Save Results as CSV
Command-Line Interface (CLI) Support
Django Web Interface

pubmed-research-finder/
│── pubmed_project/           # Django project
│   │── cli.py                # Command-Line Interface (CLI) script
│   │── settings.py           # Django settings
│   │── urls.py               # Django URL routing
│   │── views.py              # Django views
│   │── templates/            # HTML templates
│   │── static/               # CSS & JS files
│── papers/
│   │── utils.py              # Functions for PubMed API requests
│── tests/
│   │── test_cli.py           # Unit tests for CLI
│── pyproject.toml            # Poetry configuration
│── README.md                 # Project documentation
│── requirements.txt          # Dependencies (alternative to Poetry)
│── manage.py                 # Django management script


Installation
1️⃣ Clone the Repository

git clone - https://github.com/sejal1234desai/pubmed-research-finder
cd pubmed-research-finder

2️⃣ Install Dependencies using Poetry
python -m pip install poetry
python -m poetry install

3️⃣ Run the Web App
python manage.py runserver

4️⃣ Run CLI Commands
python -m poetry run python cli.py "cancer treatment"

Enable Debug Mode
python -m poetry run python cli.py "AI in medicine" --debug

Save Results to CSV
python -m poetry run python cli.py "diabetes research" --file results.csv


🔐Non-Academic Author Identification
This project applies heuristics to classify authors as non-academic based on:
✔ Company Keywords: Inc., Ltd., LLC, Pharma, Biotech, Diagnostics, Solutions
✔ Academic Keywords: University, College, Institute, Faculty, Department
✔ Email Domains: Non-.edu, .gov, .ac domains indicate corporate affiliation

🔐External Tools Used
Tool	           Purpose
PubMed           API	Fetching research paper metadata
Django	         Web interface
Poetry	         Dependency management
Requests	     API communication
XML Parsing	     Extracting author/affiliation data

🔐External Tools Used
During the development of this project, assistance was taken from a Large Language Model (LLM), specifically OpenAI's ChatGPT, to help with debugging, structuring code, and improving the overall functionality of the application. The LLM was used to:

Optimize Python and Django implementation.
Debug errors related to fetching and processing PubMed data.
Improve CLI command execution and ensure adherence to best practices.
Enhance documentation clarity and completeness.
All core functionalities, logic, and implementation decisions were manually reviewed and tested.



🔐Django Installation & Feature Implementation

To install Django, you need to use the pip package manager. If Django is not already installed, you can install it by running the command python -m pip install django.

Once Django is installed, you can create a Django project by running the command django-admin startproject pubmed_project. After creating the project, navigate into the project directory using cd pubmed_project.

In this project, several features have been implemented to fetch and display research papers from PubMed. The search functionality is handled within Django views, specifically in the views.py file. It processes user queries and retrieves PubMed search results using the requests library, which are then displayed in the result.html template.

A CSV download feature has also been added to allow users to export search results. This is done by including a "Download CSV" button in the result.html file. When the button is clicked, a Django view processes the request and generates a CSV file containing the search results. The pandas library is used to format the data into a CSV format, making it easier for users to save and analyze the information.

To identify non-academic authors, the program extracts author affiliations from the XML data returned by the PubMed API. The function extract_non_academic_authors filters affiliations based on specific keywords such as "Inc.", "University", "Institute", and similar terms. Authors with affiliations matching company-related keywords are classified as non-academic authors, while those associated with universities or research institutions are labeled as academic.

To run the Django application, use the command python manage.py runserver. This will start a local development server, and the application can be accessed through the browser at http://127.0.0.1:8000/.


🔐Error Handling in the Application
The CLI tool is designed with robust error handling to ensure smooth execution. It includes the following safeguards:

Empty Query Handling: If the user provides an empty search query, the program will exit with an error message, preventing unnecessary API calls.
No Results Found: If no relevant papers are retrieved from PubMed, the tool will notify the user and exit gracefully without saving an empty file.
File Saving Errors: If an issue occurs while saving the results (e.g., permission denied, invalid file path), the error is caught, and an appropriate message is displayed.
Debug Mode: When enabled, it provides additional insights into the query processing and helps identify issues during execution.


🔐TestPyPI Package
This project has been uploaded to TestPyPI with multiple versions (0.1.0, 0.1.1, 0.1.2, etc.), but these versions have not been fully tested for installation and execution. Further validation is required to ensure their functionality.

You can find the package on TestPyPI here:
🔗 TestPyPI - pubmed-project
https://test.pypi.org/project/pubmed-project/

To install a specific version from TestPyPI, use:
pip install --index-url https://test.pypi.org/simple/ pubmed-project==0.1.0
Replace 0.1.0 with the required version.




🔐Contributing
Fork the repository
Create a feature branch (git checkout -b new-feature)
Commit your changes (git commit -m "Added new feature")
Push to GitHub (git push origin new-feature)
Create a Pull Request