# Item Catalog Web App
By Boyapati Sravani

# In This Project
This project has one main Python module `statesmain.py` which runs the Flask application. A SQL database is created using the `StatesData_Setup.py` module and you can populate the database with test data using `states_init.py`.
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application.

# Dependencies
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

# Skills Required
1. Python
2. HTML
3. CSS
4. OAuth2client
5. Flask Framework
6.DataBaseModels
# Installation
There are some dependancies and a few instructions on how to run the application.
Seperate instructions are provided to get GConnect working also.

# How to Install
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repo or download and place zip here
3. Launch the Vagrant VM (`vagrant up`)
4. Log into Vagrant VM (`vagrant ssh`)
5. Navigate to `cd /vagrant` as instructed in terminal
6. The app imports requests which is not on this vm. Run pip install requests

Or you can simply Install the dependency libraries (Flask, sqlalchemy, requests,psycopg2 and oauth2client) by running 
`pip install -r requirements.txt`

7. Setup application database `python /StatesStore/StatesData_Setup.py`
8. *Insert sample data `python /StateStore/states_init.py`
9. Run application using `python /StatesStore/statesmain.py`
10. Access the application locally using http://localhost:4444

*Optional step(s)

## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'StatesStore'
7. Authorized JavaScript origins = 'http://localhost:4444'
8. Authorized redirect URIs = 'http://localhost:4444/login' && 'http://localhost:4444/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in book-store directory that you cloned from here
14. Run application using `python /StatesStore/statesmain.py`

## JSON Endpoints
The following are open to the public:

 all States & district details JSON:`/states/JSON `
    - Displays the whole states names.

states Categories JSON: `/States/states/JSON`
    - Displays all states details
All statedistricts: `/States/name/JSON`
	- Displays all  statedistrict details
	
statedistrict details JSON: `/States/<path:state_name>/names/JSON`
    - Displays states  for a specific district details

states Edition JSON:`/States/<path:state_name>/<path:edition_name>/JSON`
    - Displays a specific states district category.

## Miscellaneous

This project is inspiration from [gmawji](https://github.com/gmawji/item-catalog).
