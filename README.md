# CSE 412 Final Project — Music Library

Flask frontend for the CSE 412 music library project (Phase 3). Currently uses mock data; PostgreSQL integration is planned for a later phase.

## Setup

**Prerequisites:** Python 3.9+

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the development server
python app.py
```

The app runs at `http://localhost:5001` by default (port 5000 is reserved by macOS AirPlay).

To use a different port:

```bash
FLASK_PORT=8080 python app.py
```

## Mock credentials

| Username    | Password      |
|-------------|---------------|
| `jdoe`      | `pass123`     |
| `asmith`    | `music4life`  |
| `mjohnson`  | `vinyl99`     |
| `kwilliams` | `beats2024`   |
| `lbrown`    | `sound_wave`  |

You can also register a new account from the UI (stored in memory only, resets on restart).

---

## Phase 3 TODO checklist

### Fix Phase 2 grader feedback
- [ ] Address grader feedback from Phase 2

### Backend / database
- [x] Replace mock data with a real PostgreSQL connection (`psycopg2`)
- [ ] Add `DATABASE_URL` (or host/port/dbname/user/password) env vars to setup instructions
- [ ] Wire login/register to the `Users` table (parameterized queries, no plaintext passwords)
- [ ] Wire home, release detail, and collection detail pages to live DB queries

### CRUD operations (20 pts — all four required)
- [ ] **Create** — add UI + route to insert a new release (or other record) into the DB
- [ ] **Read** — already scaffolded; confirm it pulls from PostgreSQL, not mock data
- [ ] **Update** — add UI + route to edit an existing record
- [ ] **Delete** — add UI + route to remove a record, with confirmation

### Deliverables
- [ ] Screen-recorded video (≤ 10 min) with voice narration from all team members showing Insert / Update / Delete / Query
- [ ] Upload video to YouTube (public or unlisted) and paste link here
- [ ] Make GitHub repository public and paste link here
- [ ] Prepare Application Manual PDF (`GroupID.pdf`), including:
  - [ ] Overview
  - [ ] Database design summary (ER diagram or schema snapshot from Phase 2)
  - [ ] Technology stack section
  - [ ] Setup instructions (can mirror this README)
  - [ ] Feature list and descriptions
  - [ ] Screenshots of each CRUD operation (UI + resulting DB state)
  - [ ] Authentication details (test credentials)
  - [ ] Team contributions (name, responsibilities, % contribution)
  - [ ] YouTube video link
  - [ ] GitHub link
- [ ] Submit ZIP: PDF report + full source code + database dump/schema
