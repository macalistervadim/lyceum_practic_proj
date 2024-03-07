# How to get started with the application 📝

[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/students/197286-macalistervadim-course-1112/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/students/197286-macalistervadim-course-1112/commits/main)

## Run the app 🚀

To run the app locally, follow these steps:

1. Clone the repository: `git clone {repository_url}`
2. Navigate to the project directory: `cd lyceum`
3. Create and activate a virtual environment:
   - Linux/macOS: `python3 -m venv venv && source venv/bin/activate`
   - Windows: `python3 -m venv venv && venv\Scripts\activate`
4. Install the main dependencies for production: `pip3 install -r requirements/prod.txt`
5. Set up your database: `python3 manage.py migrate`
6. Create a superuser: `python3 manage.py createsuperuser`
7. Create a `.env` file in the root of your project and define your environment variables (see below for example variables)
8. Run the development server: `python3 manage.py runserver`
9. Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Database
The project uses a ready-made database for educational purposes.

1. Perform database migrations:

```
python3 manage.py migrate
```

2. To use superuser, use the following data:
```
login: `admin`
password: `admin`
```

*note: mail is not used in the project for superuser*

## Environment Variables

The project uses a `.env` file to store confidential or environment variables required for the application to run. Below is the format of the `.env` file.
To get started with the project, you'll need to copy the `.env.example` file and configure it accordingly.

1. Copy the `.env.example` file:
   
   Linux:
   ```bash
   cp .env.example .env
   ```
   Windows:
   ```cmd
   copy .env.example .env
   ```

2. Open the `.env` file and set the required environment variables:
   ```plaintext
   # Example .env file

   # Django secret key
   `DJANGO_SECRET_KEY=your_secret_key_here`
   
   # Django debug
   `DJANGO_DEBUG=True/False`

   # DJANGO allowed hosts
   `DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost`

   # Other environment variables...
   ```

## Managing Translations

1. Create translation files: `django-admin makemessages -l ru` and `django-admin makemessages -l en`
2. Edit translation files: Use a text editor to modify the `.po` files and add translations for the strings.
3. Compile translation files: `django-admin compilemessages`

Replace <language_code> with the desired language code for the translation. For example, for English, you can use en, and for Spanish, you can use es.

Standard Language Codes
Here are some standard language codes that you can use:
```
en: English
es: Spanish
fr: French
de: German
ru: Russian
```
Predefined Translations
Additionally, Django provides predefined translations for certain languages. You can find the list of available languages in the Django documentation:

[Django - Available languages](http://www.lingoes.net/en/translator/langcode.htm)

When using the makemessages command, Django will automatically create translation files for the specified language using the predefined translations if available.

## Fixtures

To use fixtures in your Django project, follow these steps:

1. Create fixture files containing serialized data for your models. You can generate fixture files using the `dumpdata` management command:

   ```bash
   python -Xutf8 manage.py dumpdata --indent 2 -o fixtures/data.json (or you optional dir_name)
2. Load fixture data into your database using the loaddata management command:
   ```bash
      python3 manage.py loaddata fixtures/data.json (or you optional dir_name)
## ER Diagram
Here is a visual ER diagram of the existing project database

![ER Diagram](ER.jpg)

**Note**: This app is intended as a demonstration and might not be suitable for production use without further modifications and security considerations.
