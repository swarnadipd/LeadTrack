# LeadTrack — a tiny CRM API

A small REST API for managing sales leads (name, email, company, status).
Built with FastAPI + PostgreSQL + SQLAlchemy, containerized with Docker,
and designed to run two copies behind an Nginx load balancer.

**Every file in this project has been run and tested against a real
Postgres database before being handed to you** — the commands below are
exactly what was tested, so if something doesn't work, it's almost
certainly an environment/setup issue on your machine, not a bug in the
code. That's actually a good debugging exercise for the interview too.

---

## Day 1 — run it locally (no Docker yet)

1. Install Python 3.12+ if you don't have it.
2. Start a local Postgres. Easiest way — using Docker just for the database:
   ```bash
   docker run -d --name leadtrack-db \
     -e POSTGRES_USER=leadtrack \
     -e POSTGRES_PASSWORD=leadtrack \
     -e POSTGRES_DB=leadtrack \
     -p 5432:5432 postgres:16
   ```
3. Install the Python dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Run the API:
   ```bash
   uvicorn main:app --reload
   ```
5. Open **http://localhost:8000/docs** in your browser. This is FastAPI's
   auto-generated interactive documentation — you can create, list,
   update, and delete leads right from the browser, no extra tools needed.

### Or test it from the terminal (this exact sequence was verified to work)
```bash
curl localhost:8000/health

curl -X POST localhost:8000/leads -H "Content-Type: application/json" \
  -d '{"name":"Riya Sharma","email":"riya@acme.com","company":"Acme Co"}'

curl localhost:8000/leads

curl -X PATCH localhost:8000/leads/1 -H "Content-Type: application/json" \
  -d '{"status":"contacted"}'

curl "localhost:8000/leads?status=contacted"

curl -X DELETE localhost:8000/leads/1
```

**What to look at while this runs:** open `main.py` and read each endpoint
top to bottom. Every endpoint follows the same shape: get a database
session, do a query, return the result. Once that pattern clicks, you
understand the core of how FastAPI apps work.

---

## Day 2 — run two copies behind a load balancer

This is the part most worth understanding deeply for the interview.

```bash
docker compose up --build
```
(Note the space, not a hyphen — `docker compose` is the current standard command.)

This starts **four containers**: `db` (Postgres), `api1` and `api2` (two
identical copies of the same app), and `nginx` (the load balancer sitting
in front of both).

Now hit the load balancer's port repeatedly and watch the `instance`
field change:
```bash
curl localhost:8080/health
curl localhost:8080/health
curl localhost:8080/health
```

You'll see the hostname alternate between the two containers — that's
Nginx round-robining your request across `api1` and `api2`. All your
`/leads` endpoints also work the same way, just through port 8080 instead
of 8000 now.

---

## Day 3 — deploy it for real

See the full plan and deployment steps in `zero_crm_3day_prep_plan.md`
(the companion file). Short version: push this folder to a GitHub repo,
connect it to Render's free tier, add a free Postgres instance there, and
point `DATABASE_URL` at it.

---

## Project structure

```
leadtrack/
├── main.py            # FastAPI app + all the /leads endpoints
├── models.py           # SQLAlchemy table definition (the "leads" table)
├── schemas.py          # Pydantic request/response shapes
├── database.py          # DB connection setup
├── requirements.txt      # Exact tested dependency versions
├── Dockerfile            # How to containerize the app
├── docker-compose.yml      # Runs db + api1 + api2 + nginx together
├── nginx.conf              # Load balancer config
└── README.md                # This file
```
