[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/students/197286-macalistervadim-course-1112/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/students/197286-macalistervadim-course-1112/commits/main)
# Getting Started
# To run the app locally, follow these steps:

- Clone the repository: git clone {repository_url}
- Navigate to the project directory: cd dashboard
- Create and activate a virtual environment: python -m venv venv and then source venv/bin/activate (Linux/macOS) or venv\Scripts\activate (Windows)
- Install the main dependencies for production: pip install -r requirements/prod.txt
- Set up your database: python manage.py migrate
- Create a superuser: python manage.py createsuperuser
- Create a .env file in the root of your project and define your environment variables
- Load environment variables in your Python code
- Run the development server: python manage.py runserver
- Access the app at http://127.0.0.1:8000/ in your browser.
# **Contribution**
Thank you for your interest in this repository! Your contributions are highly appreciated. If you encounter any issues or have suggestions, please feel free to create an issue or pull request. We hope this app aids in your understanding and experience.

- _Note_: This app is intended as a demonstration and might not be suitable for production use without further modifications and security considerations.
