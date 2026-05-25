# Multi Species Fishing Challenge


Django web application that allows users to record fish catches for a year.

## Recent Changes & New Features (as of May 2026)

- **User Profiles**: Each user now has a profile with an optional profile picture. Profiles are created automatically for new users, and a management command is available to create missing profiles for existing users.
- **Profile Management**: Users can update their profile picture and change their password from dedicated profile pages (`/profile/picture/`, `/profile/password/`).
- **Catch Pictures**: Catches can now include an uploaded picture. Images are stored in `media/catch_pics/` and displayed in the UI.
- **Catch Comments**: Catches support an optional comments field for additional notes.
- **Admin Improvements**: Admin now supports management of profiles, and all lookup tables (species, venue, method, bait) are editable via the admin interface.
- **Signals**: Automatic profile creation and saving via Django signals ensures every user always has a profile.
- **Management Command**: `python manage.py create_missing_profiles` ensures all users have a profile.
- **URL Structure**: Dedicated URLs for profile management and improved catch/registration URLs.
- **Template/UI**: Profile picture and username are shown in the navbar; profile and password forms are styled. Home page and navigation improvements.
- **Migrations**: Added migrations for profile, catch picture, and comments fields. Legacy length field is now decimal; migration included to clean up old data.
- **Static & Media**: Static and media file handling for user-uploaded images.

## Features

- User authentication (login/logout/register) using Django auth framework
- Create and list catches with fields: date, species, venue, method, bait, weight, length, picture, comments (lookup values now stored in their own tables)
- Filterable list by species, venue, method, bait for each user
- Profile management: users can update their profile picture and password
- Bootstrap 5 styling via `django-bootstrap5` with a custom green theme
- Admin management for all lookup tables and user profiles
- Catch images and comments support

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

3. Run migrations (this will also create lookup tables for species, venue, method and bait and seed them with default values, and add new fields for profile, catch pictures, and comments):

```bash
python manage.py migrate
```

4. Create a superuser (optional):

```bash
python manage.py createsuperuser
```
```

5. (Optional) Ensure all users have a profile (for existing databases):

```bash
python manage.py create_missing_profiles
```

6. Start the development server:

```bash
python manage.py runserver
```


7. Access the site at `http://localhost:8000`

- Home page with links to login, register, record new catches, view your catches, or logout
- After logging in, use the navigation bar to manage catches, update your profile, or log out via the Logout link

## Notes

- The site theme uses green accents and background; static CSS overrides are in `static/css/site.css`.
- Home page includes decorative fishing images served via Unsplash.
- Profile pictures and catch images are stored in `media/profile_pics/` and `media/catch_pics/` respectively.

- The "length" attribute for catches previously used text choices; it is now a decimal field.  A migration is included to null out any legacy non‑numeric values.  Run `python manage.py migrate` to apply the cleanup before working with existing data.
- Comments and pictures can be added to each catch.

- Users only see and can add their own catches.
- Use filters on the catch list page to narrow results.
- Profile and password management available from the navigation bar.

