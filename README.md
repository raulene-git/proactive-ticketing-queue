# Proactive-Ticketing-Queue

## Overview
Proactive‑Ticketing‑Queue is my personal IT ticketing system built to explore proactive* service desk practices rather than purely reactive support.

The focus of this project is not just ticket handling, but:
- Structured workflows
- Visibility of repeat issues
- Building foundations for automation and insight‑driven support

This project is intentionally lightweight and practical, reflecting real-world support environments.

---

## Why This Project Exists
In many IT support environments, tickets can not be always be logged for project tickets so keeping progress of personal work that cannot be categorised into a 'Service Desk' Ticket is difficult

This project explores how a ticketing system can:
- Encourage better categorisation and structure
- Make projects more visible
- Support proactive documentation and communication
- Act as a base for future automation and AI-assisted tooling

---

## Current Functionality
- Ticket creation and retrieval
- Status lifecycle handling  
  *(Open → In Progress → Resolved → Closed)*
- Flask-based backend logic
- HTML / JavaScript frontend
- Database-backed design (local development)

---

## Tech Stack
- **Python** (Flask)
- **HTML / JavaScript**
- **SQL** (via `pyodbc`)
- **GitHub Copilot** (assisted development)

---

## Planned Enhancements
- Improved Worklog UI
- Basic analytics for projects I work on
- API endpoints for automation
- Role-based access concepts
- Audit-style change tracking

---

## Data & Security
This repository contains **no real ticket data**.

All data is:
- Local to the developer environment
- Configured using environment variables
- Excluded from version control via `.gitignore`

Only application logic and structure are stored here.

---

## Project Status
This is an active learning and experimentation project that evolves alongside my work in enterprise IT environments.
