# chat_app
![Screenshot (27)](https://user-images.githubusercontent.com/26871045/161295565-99878d74-0aa6-4c33-86e6-5c5b782d358d.png)

A small functional person-to-person message center application built using Django.

## Run ##
1. move to project root folder

2. Create and activate a virtualenv (Python 3)
```bash
virtualenv venv
```
3. Install requirements
```bash
pip install -r requirements.txt
```
5. Migrate database
```bash
./manage.py migrate
```
7. Create admin user
```bash
./manage.py createsuperuser
```

8. Run development server
```bash
./manage.py runserver
```
