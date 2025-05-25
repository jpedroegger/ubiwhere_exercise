# Django Traffic Monitor

This project consists in developing a REST API as part of a development exercise, where the developer must build a traffic monitoring system using a sort of tools such as: **Django** and **Django-Rest-Framework**.

---

## Technologies Used

- [Django](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/) + [PostGIS](https://postgis.net/)
- [Docker](https://www.docker.com/)
- [Pandas](https://pandas.pydata.org/) for data import
  
---

## Getting Started

### 1. Clone the repository

```bash
git clone git@github.com:jpedroegger/ubiwhere_exercise.git
cd ubiwhere_exercise
```

### 2. Set up environment variables

Create a `.env` file based on the provided example:

```bash
cp .env.example .env
```

Edit the `.env` file and fill in your local configuration.

---

### 3. Run the project with Docker

```bash
docker compose up --build
```

This will:

- Set up the database with spatial data support
- Start the Django server on port `8000`

Access the app at: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

---

## Create a Superuser

```bash
docker compose exec django-web python manage.py createsuperuser
```

---

## Importing CSV Data

Place your `traffic_speed.csv` file in the project root.

Run the import command:

```bash
docker compose exec django-web python manage.py import_csv --file traffic_speed.csv
```

---

## Project Structure

```bash
.
├── core/      
├── traffic_monitor/
├── .env.example
├── docker-compose.py
├── Dockerfile
├── entrypoint.sh
├── manage.py
├── pytest.ini
├── README.md
├── requirements.txt
├── sensors.csv
└── traffic_speed.csv
```
## Author

Developed by [João Pedro Santiliano](https://github.com/jpedroegger)
