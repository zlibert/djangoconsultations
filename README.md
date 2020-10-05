
# Medical Consultation Ticket System

  

Django medical consultation ticket system

TODO:

- Create Profile CRUD (specially password change)

- Avoid repeating some things in templates (DRY or using some Forms)

- Use a Model for Consultation.status instead a choice attribute

  

**Deploying with Docker:**

To start running a dev environment with postgres db, nginx and gunicorn containers you may use:

```
docker-compose -f docker-compose.yml up -d --build
```

Simple production environment could be run using:
```
docker-compose -f docker-compose.prod.yml up -d --build
```
By default port is 1337 to avoid conflicts if your server is already using 80 port with another service.

If it's the first time you run it, you need to create basic groups and users:
- Set your .env* files parameters correctly (database name, ports, etc)
- Create your database
- Get inside the web container:
- Create admin user:
    
```
docker exec -ti djangoconsultations_web_1 sh

python manage.py flush --no-input  #  delete database content
python manage.py migrate  #  apply migrations to the DB
python manage.py collectstatic  #  create static files - not for development -
python manage.py createsuperuser  # create new admin user
```
- Go to your browser, open URL: yourdomain:port/admin
- Login with your superuser and create this groups: requesters, supervisors, agents
- Add your superuser to the supervisors group and you may create another user and add it as an agent (the one that respond consultations)
- After that your ready to test/use registering users. By default all registered users are requesters, not agents neither supervisors.


**Requires:**

  

Python 3.8.2

Django 3.1.1
