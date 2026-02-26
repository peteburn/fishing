# Multi Species Fishing Challenge

Django web application that allows users to record fish catches for a year.

## Features

- User authentication (login/logout) using Django auth framework
- Create and list catches with fields: date, species, venue, method, bait, weight
- Filterable list by species, venue, method, bait for each user
- Bootstrap 5 styling via `django-bootstrap5` with a custom green theme

## Setup

1. Create and activate a Python virtual environment (already configured).

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Create a superuser (optional):

```bash
python manage.py createsuperuser
```
```

5. Start the development server:

```bash
python manage.py runserver
```

6. Access the site at `http://localhost:8000`

- Home page with links to login, record new catches, view your catches, or logout
- After logging in, use the navigation bar to manage catches or log out via the Logout link

## Notes

- The site theme uses green accents and background; static CSS overrides are in `static/css/site.css`.
- Home page includes decorative fishing images served via Unsplash.

- Users only see and can add their own catches.
- Use filters on the catch list page to narrow results.

