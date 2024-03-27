# Backend application

## API

We use Django as a primary backend framework, and Django Rest Framework as a primary API framework.
However, we do not use Django views for page generation, rather we serve React web app as a set of static files,
which serves as a client for the API, populating data about personalities, 
organizations and media sources.
We do not manage users, authentication and authorization in the API, also we do not create and update any data,
so our application is read-only.
However, we offer admin panel for the API, which is used to manage data in the database, by the address
https://subjective.agency/admin/

## Release process

We host our server on Railway, and rely on Railway pipelines to deploy the application.
Railway requires `runtime.txt` file to be present in the root directory of the repository, 
in order to have the same Python version on the server and developer's machine.
For the deployment and starting server, we use `Procfile` file, which specifies the command to run the server.
Example:
```bash
web: python manage.py collectstatic --noinput && python manage.py fetchstatic 0.2.14 --noinput && gunicorn wganda.wsgi --log-level=info --log-file=-
```

We use `requirements.txt` file to specify Python dependencies.

### Django and Railway

We make use of Django/Railway integrations, which allow us to use `manage.py` commands on the server.
We use `manage.py` to run migrations, collect static files, and fetch static files from the frontend releases.
Also, we add some custom commands to `manage.py` (as a single deployment entry point), 
which are used to populate the frontend:
```bash
python manage.py fetchstatic 0.2.14 --noinput
```
where `0.2.14` is a version of frontend application, which is fetched from CDN.

Railway offers functional database integration for Django projects, which is not necessary for our project,
since we use external PostgreSQL database and do not manage it from the Django application.
