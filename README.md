# solo_assessment_2024_CS551Q
# Modupe Mobile Phone Shop
## Overview
This is a solo assessment course work by Samuel Amao for the course CSS551Q at the University of Aberdeen.
The Modupe Mobile Phone Shops is a web application developed using Python with Django Framework, aimed at 
simplifying the process of purchasing mobile phones. The goal is to provide users with an intuitive 
platform where they can effortlessly browse, search for, and order mobile phones. Leveraging open-source data 
from [Kaggle](https://www.kaggle.com/datasets), users have access to a wide range of mobile phone information, including specifications, 
prices, and availability.
The application is deployed on PythonAnyWhere at this site:  <https://samamao.pythonanywhere.com/>

### Installation Steps
   1. Clone or download the repository as follows:
      ``` bash
      git clone https://github.com/kobe5pts/solo_assessment_2024_CS551Q.git
      ```
   2. Use these commands to set things up, this assumes a linux operating system:
      Set up and activate the virtual environment. Navigate to the project folder and execute the following commands in the terminal:
         ``` bash
         cd solo_assessment_2024_CS551Q/
         pyenv local 3.10.7 # This sets the local version of Python to 3.10.7 (Optional)
         python3 -m venv .venv # This creates the virtual environment
         source .venv/bin/activate # This activates the virtual environment

         ```

   3. Install the requirements by executing the following command in the terminal:
         ```
         pip install -r requirements.txt
         ```
   4. start the server by running the command for codio sand-box:
         ```bash
         python3 manage.py runserver 0.0.0.0:8000 # Use Ctrl+C to stop the server.
         python3 manage.py runserver # on local machine
         ```
   5. Launch the application to your browser but change the port to  '8000'    

## Creating Superuser
   You can create an admin user to monitor the customers and orders made in the shop. 
   There is also a dashboard that monitors the orders made by the customers. You can also add more admins or customers. 
   Run this command in your terminal:
```bash
   python3 manage.py createsuperuser
```
   Launch the admin application by adding   /admin   to the web homepage address launched in step 5 above.
## Creating a user
   You create a user by signing up using the [Register] button, however, such user would have to be activated by the superuser in the
   admin dashboard for now. Authentication for new user was not implemented in this project.
### Program Structure
The program is composed of six Django applications: mobile_phones_shop for site basic settings, carts, category, orders, products_shop, and useraccounts applications for the website's detailed content.

**mobile_phones_shop Folder**: Contains basic site settings.

**static Folder**: Contains all the custom Bootstrap css files, which are referenced in other HTML files, as well as picture files for banner, modupeLogo and favicon.

**tests Folder**: Contains all BDD test files and test environment configuration files. 

**templates Folder**: Contains all the HTML files for different functionalities, all inheriting from the 'layout.html' interface, as well as the from the templates in the includes sub-folder.

**products_shop Folder**: Details the store's content.
* The 'dataset' Folder: Stores initial data.
* The 'models.py': Defines the products table with a foreign key set to Category table in the database to ensure data integrity.
* The 'views': Handles site requests with routes to the appropriate templates
* The 'management'/'commands' Folder: Contains 'parse_csv_file.py' for importing initial data into the database according to the models' structure, with error handling and data formatting.
* 'migrations' Folder: Synchronizes the model classes with the database schema. 

**other apps Folder**:All the remaining application folders contain similar contents with the exception of the dataset and management folders.

**The 'manage.py'** file is utilized for starting the server and includes error handling features.

**The db.sqlite3** file is the database file containing the data from 'parse_csv_file.py' and the tables from all the application 'models.py'.


### Implementation
- **Testing**: Behave tests focused on critical functionalities like login, purchase, and search features, 
ensuring the application meets requirements. You can run the behave test as follows:
1. activate the virtual environment: source .venv/bin/activate
2. run the following commands to run each feature behave tests:
```bash
      behave tests/features/modupeLogo.feature  #make sure you are now on solo_assessment_2024_CS551Q/
      behave tests/features/login.feature
      behave tests/features/search.feature
      behave tests/features/purchase.feature  
```      
You may also run the BDD test at once by execute the following commands:

```bash
behave #make sure you are now on solo_assessment_2024_CS551Q/
```
* You will see the BDD test, albeit with a "failing scenarios at tests/features/purchase.feature:3  
Add product to cart and proceed to checkout", for now of which I have not been able to fully implement.
