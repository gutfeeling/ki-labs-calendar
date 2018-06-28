# KI Labs Calendar

A REST calendar API that lets interviewers and candidates do the following:

1. Create accounts 
2. Specify time slots when they are available for an interview. 
3. Fetch time slots when a particular candidate and a group of interviewers are all available together.

## Try it out without the fuss

The API is available publicly at http://ki-labs.herokuapp.com/. 

The API is running on a free dyno on Heroku, so it might take a few seconds to start up when you make the first request.
Please be patient.

The database has already been populated with some users and time slots.

## Documentation 

The API is documented at /docs/. The publicly available docs are at http://ki-labs.herokuapp.com/docs/.

## Try it out locally (some fussing involved)

To test the API in your machine, first make sure you have `git`, `python3` and `python-virtualenv` installed. Then 
follow these steps.

1. Clone the repository
  
  ```
  git clone https://github.com/gutfeeling/ki-labs-calendar.git
  cd ki-labs-calendar
  ```

2. Create and activate a virtualenv

  ```
  virtualenv -p python3 venv
  source venv/bin/activate
  ```
  
3. Install Python related requirements

  ```
  pip install -r requirements.txt
  ```

4. Run migrations 

  ```
  cd ki_labs_backend
  python manage.py makemigrations
  python manage.py migrate
  ```

5. Launch the Django development server

  ```
  python manage.py runserver 127.0.0.1:8000
  ```

When you complete these steps, the API will be available for use at http://127.0.0.1:8000. 
