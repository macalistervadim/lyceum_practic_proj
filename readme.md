# How to get started with the application 📝

[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/students/197286-macalistervadim-course-1112/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/students/197286-macalistervadim-course-1112/commits/main)

## Run the app 🚀

To run the app locally, follow these steps:

Open your terminal.
1. Navigate to the "projects" directory: `cd ~/projects` (to select this folder, create this directory in your directory or specify any of your previously created ones)
2. Clone the repository: `git clone {repository_url}`
3. Navigate to the project directory: `cd lyceum`
4. Create and activate a virtual environment:
   - Linux/macOS: `python3 -m venv venv && source venv/bin/activate`
   - Windows: `python -m venv venv && venv\Scripts\activate`
5. Install the main dependencies for production: `pip3 install -r requirements/prod.txt`
6. Set up your database: `python3 manage.py migrate`
7. Create a superuser: `python3 manage.py createsuperuser`
8. Create a `.env` file in the root of your project and define your environment variables (see below for example variables)
9. Run the development server: `python3 manage.py runserver`
10. Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

# Important note
Please note that all the following points below are executed strictly in the base directory of the project, in which you have compiled the repository earlier in the paragraph above

## Database
The project uses a ready-made database for educational purposes.

Open your terminal.
1. Perform database migrations:
```
python3 manage.py migrate
```

2. To use superuser, use the following data:
```
login: admin
password: admin
```

*note: mail is not used in the project for superuser*

## Collectstatic

To work correctly and display static files in prod mode, you need to perform a couple of procedures before starting the project

1. Generate static files
```
python3 manage.py collectstatic
```

*note: Please note that the folder where static files will be collected is specified in the project settings under the name "STATIC_ROOT"*

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

    # DJANGO_MAIL
    `DJANGO_MAIL=admin@admin.ru`

    # DJANGO_ALLOW_REVERSE
    `DJANGO_ALLOW_REVERSE=True/False`
   
    # DEFAULT_USER_IS_ACTIVE
    `DEFAULT_USER_IS_ACTIVE=True/False`
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

   Windows:
   ```
   python -Xutf8 manage.py dumpdata catalog feedback auth sessions --indent 2 -o fixtures/data.json
   ```
   Linux:
   ```
   python3 manage.py dumpdata catalog feedback auth sessions --indent 2 -o fixtures/data.json 
   ```
   
2. Load fixture data into your database using the loaddata management command:
   ```
   python3 manage.py loaddata fixtures/data.json 
   ```
*note: you can also specify fixtures/data instead of the name.json your folder if desired. But it must be located along the path: BASE_DIR / dir_name*

## ER Diagram
Here is a visual ER diagram of the existing project database

![ER Diagram](ER.jpg)

**Note**: This app is intended as a demonstration and might not be suitable for production use without further modifications and security considerations.
