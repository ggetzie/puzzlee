# Puzzlee

An Art Puzzle Game

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Getting started locally

There are few steps to get your project up and running locally for development.

1. Make sure Postgres is installed. This project assumes the use of the [PostgreSQL database](https://www.postgresql.org/download/). Install it and create a superuser for your local account.

   ```±sql
   CREATE USER my_local_username WITH SUPERUSER;
   ```

   As long as your Postgres installation is configured to allow login by the `ident` method (i.e. the Postgres username is the same as the account username), you should be able to login without a password. Check the `pg_hba.conf` file to confirm. On Ubuntu systems it's usually found in `/etc/postgres/15/data/pg_hba.conf` (replace 15 with the version of Postgres you're using).

2. Create a virtual environment and install the requirements. Use the `requirements_nover.txt` file if you want to allow pip to use the most recent compatible versions of the installed libraries.
   ```±bash
   python -m venv .venv --prompt puzzlee
   source .venv/bin/activate
   pip install -r requirements_nover.txt
   ```
3. Export the environment variables from the `.env` file and set up the database
   ```±bash
   source ./export_dotenv
   ./utility/setup_db
   ./manage.py makemigrations
   ./manage.py migrate
   ```

4. Install node modules and run gulp
   ```±bash
   # install gulp globally if it's not available
   npm install -g gulp
   npm install
   gulp # should start development server at localhost:3000
   ```
   

   



### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy puzzlee

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.
### Custom Bootstrap Compilation

The generated CSS is set up with automatic Bootstrap recompilation with variables of your choice.
Bootstrap v5 is installed using npm and customised by tweaking your variables in `static/sass/custom_bootstrap_vars`.

You can find a list of available variables [in the bootstrap source](https://github.com/twbs/bootstrap/blob/main/scss/_variables.scss), or get explanations on them in the [Bootstrap docs](https://getbootstrap.com/docs/5.1/customize/sass/).

Bootstrap's javascript as well as its dependencies is concatenated into a single file: `static/js/vendors.js`.
