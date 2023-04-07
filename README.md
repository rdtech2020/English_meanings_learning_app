# English Meanings Learning Flask App

This is a Flask web application that helps users learn English meanings. The application is designed to allow users to learn correct English words and get performance also.

Project is live on [Pratik Python Pathshala](https://pratik-pathshala.onrender.com)

### Prerequisites
Before running this application, you must have the following installed:
* Python 3.8
* Flask
* requests

### Installation

* Clone the repository:
```cmd
git clone https://github.com/rdtech2020/English_meanings_learning_app.git
```
* Install dependencies:
```cmd
pip install -r requirements.txt
```
* Insert token for email check in `email_validation.py` 8 no. line.
```py
 self.key = '' #insert your key
```

### Usage
To run the application, navigate to the root directory of the project and run the following command:
```cmd
gunicorn app:app
```
After running the above command, open your web browser and navigate to `http://127.0.0.1:8000` to access the application.

### Features
The application has the following features:
* User-friendly interface
* Easy to use
* Learn english words
* Performance count

### License
This project is licensed under the MIT License - see the LICENSE file for details.
