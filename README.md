# Reeve's Holy Rentals - HolyKeanuReeves
[![Status](https://img.shields.io/badge/status-In%20Development-red.svg)]() [![Version](https://img.shields.io/badge/version-0.0.0-blue.svg)]()

_SOEN 341: Software Process - Term Project - Concordia University_ <br/>
_Presented to Dr. Rodrigo Morales_

## Table of Contents
- [Team Members](#team-members)
- [Project Description](#project-description)
- [Project Requirements](#project-requirements)
- [Coding Style](#coding-style)

## Team Members

- [Adam Ousmer - 40246695](https://www.github.com/adamousmer)
- [David Martinez - 29556869](https://github.com/iluvpomeranians)
- [Sheng Han Wang - 40173425](https://github.com/sean49)
- [Victor Okoro - 40073134](https://github.com/Okwilo)
- [Joseph Aladas - 40156616](https://github.com/JosephAladas)
- [Omar Abouelatta - 40191023](https://github.com/Omar-Abouelatta)

## Installation

```bash
# Clone the repository

# Navigate to the project directory
cd src/Reeves_Holy_Rentals

# Install dependencies
python -m pip install --upgrade pip
pip install django
pip install django-paypal
pip install beautifulsoup4
python -m pip install Pillow

# Run the Django development server
python manage.py runserver

# Access the application at http://127.0.0.1:8000/
```

## Project Description

Our project consists of creating a full-stack web application for an online car rental service by way of HTMX, Vanilla JS, and Hyperscript to handle client-side processing and Django for backend management of our rental database. 
Our goal is to generate a platform that would facilitate the vehicle renting process for our customers based on, but not limited to: 

- Location (i.e find near-by rental branches//drop-off venues via a dynamic geolocation map API)
- Date
- Vehicle type (i.e. SUVs/Vans/Trucks/etc)
- Category (i.e Compact/Standard/etc)
- Price
- Ratings
- Extra add-on features or services
- Optional monthly paid subscription tier system (potentially a bonus program)

Check-in processes will be handled securely by implementing Django's native middleware security tokens & autorization mechanisms to ensure that each new reservation, rental agreement, and payment process
will all be treated seriously and with careful consideration. In turn, we will implement a privacy & authentication structure that will differentiate and specify varying levels of access for system adminitrators as well as user accounts whilst on our site. 

With sqlite3 pre-packaged with Django as well as the option to migrate to any other database type, we will securely store and manage all user & rental data in our backend local server. We will make database modifications by way of CRUD/HTTP requests that will come in various forms, depending on the level of priority. We will leverage Django's ORM to simplify how we communicate with our sql database syntactically using both python and Django's templating language. Also, when applicable, for simpler HTTP request implementations, HTMX & JS will be leveraged to handle all HTTP requests to our server. 

## Coding Style

In order to maintain a consistent coding style, we will be using the following guidelines:
- [Structure](#structure)
- [Branching](#branching)
- [Frontend](src/frontend_readme.md/#coding-style)
- [Backend](src/backend_readme.md/#coding-style)

### Structure

In order to maintain a consistent structure, we will be using the following guidelines:

- Each file should have a header comment at the top of the file, which includes the following information:
  - The name of the file
  - The author of the file
  - The date the file was created
  - A brief description of the file


### Branching

In order to maintain a consistent branching strategy, we will be using the following guidelines:

We will be using the [Trunk Based Development](https://trunkbaseddevelopment.com/) branching strategy. This strategy is based on the idea that all development should happen on a single branch, called the "trunk". This allows for faster feedback and easier integration of changes.
