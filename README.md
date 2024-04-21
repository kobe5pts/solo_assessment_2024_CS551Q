# solo_assessment_2024_CS551Q
# Modupe Mobile Phone Shop

[Provide a brief description of the project.]

## Overview
Modupe Mobile Phone Shops is a web application developed using Python with Django, aimed at 
simplifying the process of purchasing mobile phones. The goal is to provide users with an intuitive 
platform where they can effortlessly browse, search for, and order mobile phones. Leveraging open-source data 
from Kaggle, users have access to a wide range of mobile phone information, including specifications, 
prices, and availability.
## Design
- **Architecture**: The application follows a modular approach, with distinct apps like Cart, Category, Orders, Product, and Useraccounts. 
Built on Django, it provides a robust foundation for web development.
- **Database Schema**: The schema includes tables for managing carts, categories, orders, products, and user accounts, 
ensuring data integrity and efficient querying.

## Development
- **Technologies Used**: Django Framework, Python Programming Language, SQLite3 Database, HTML, CSS, JavaScript, Bootstrap Framework(customized), 
Git Version Control, Codio Sandbox IDE.
- **Features Implemented**: Comprehensive search, seamless store browsing, category sorting, secure register and sign-in, 
visually appealing logo-homepage, and convenient cart management.

## Implementation
- **Testing**: Behave tests focused on critical functionalities like login, purchase, and search features, 
ensuring the application meets requirements. You can run the behave test as follows:
1.

## Installation
### Prerequisites
   - Find the list of prerequisites or dependencies required to run this application in the requirements.txt file.

### Installation Steps
   1. Clone or download the repository as follows:
      git clone git@github.com:kobe5pts/solo_assessment_2024_CS551Q.git
   2. Use these commands to set things up:
      pyenv local 3.10.7 # this sets the local version of python to 3.10.7
      python3 -m venv .venv # this creates the virtual environment for you
      source .venv/bin/activate # this activates the virtual environment
      pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.
      pip install django==4.1.2
      pip install requirements.txt
      python3 manage.py migrate
   3. [Step 3]
      ...

## Usage
- **User Guide**: [Include a brief user guide on how to use the application.]
- **Demo**: [If available, provide a link to a demo or screenshots.]

## Future Enhancements
- No anticipated enhancements as it was developed as part of a class project coursework.

## Contributors
- Samuel Amao

## License
CSRF_TRUSTED_ORIGINS =  [https://scharlau.pythonanywhere.com]