# Proactive Ticketing Queue

A lightweight IT ticketing and worklog system built with **Flask** and **SQL Server**. It's for tracking the proactive and project work that doesn't fit neatly into a service desk ticket.

![Python](https://img.shields.io/badge/Python-Flask-3776AB?logo=python&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-pyodbc-CC2927?logo=microsoftsqlserver&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

## Why it exists

In many IT support environments, project and improvement work can't always be logged as a service desk ticket, so that progress becomes invisible. This project explores how a small ticketing system can:

- encourage better categorisation and structure
- make project work visible
- support proactive documentation and communication
- act as a base for future automation and AI-assisted tooling

## Features

- Create, view, update and delete tickets (REST API + web dashboard)
- Status lifecycle: **Open → In Progress → Resolved → Closed**
- Per-ticket **worklogs** with timestamps
- Parameterised SQL queries via `pyodbc`

## API

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/tickets` | List tickets (newest first) |
| POST | `/tickets` | Create a ticket |
| GET | `/tickets/<id>` | Get one ticket |
| PUT | `/tickets/<id>` | Update title, description, status |
| DELETE | `/tickets/<id>` | Delete a ticket |
| GET | `/tickets/<id>/worklogs` | List worklog entries |
| POST | `/tickets/<id>/worklogs` | Add a worklog entry |

## Getting started

**Prerequisites:** Python 3.11+, SQL Server (Express is fine), [ODBC Driver 17 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

```powershell
git clone https://github.com/raulene-git/proactive-ticketing-queue.git
cd proactive-ticketing-queue
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create the database and tables
sqlcmd -S localhost\SQLEXPRESS -i schema.sql

# Point the app at your database (see .env.example)
$env:PTQ_DB_CONNECTION = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=ProactiveTQ;Trusted_Connection=yes;"
$env:FLASK_DEBUG = "1"
python app.py
```

Then open <http://127.0.0.1:5000>.

## Project structure

```
app.py              Flask app: routes and database access
templates/index.html  Dashboard UI (HTML + JavaScript)
schema.sql          SQL Server schema (Tickets, WorkLogs)
.env.example        Environment variables the app reads
```

## Data and security

- No real ticket data is stored in this repository.
- Connection details come from environment variables, not source code.

## Roadmap

- [ ] Improved worklog UI
- [ ] Basic analytics (repeat issues, time per category)
- [ ] Role-based access
- [ ] Audit-style change history
- [ ] Rebuild as a SharePoint Framework (SPFx) web part, backed by SharePoint lists

## How it was built

Built with AI coding assistants (**Claude** and **GitHub Copilot**). I came up with the idea and the support workflow it models, and I ran, tested and iterated on it in my own environment.

## License

[MIT](LICENSE)
