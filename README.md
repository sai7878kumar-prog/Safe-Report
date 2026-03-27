# SafeReport

SafeReport is a simulation-based smart harassment reporting system built with Flask.

## Features

- Simulated social media chat interface
- Harassment detection with severity classification (Low/Medium/High)
- Smart suggestions based on severity
- Escalation workflow simulation for high-risk chats
- SQLite report storage with timestamps
- Admin panel with severity filter

## Project Structure

```text
safe_report/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── analyzer.py
│   ├── models.py
│   ├── templates/
│   │   ├── chat.html
│   │   ├── result.html
│   │   └── admin.html
│   └── static/
├── database.db
├── run.py
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python run.py
```

4. Open:

- `http://127.0.0.1:5000/chat`
- `http://127.0.0.1:5000/admin`

## Notes

- `database.db` is created automatically when app starts.
- Detection uses keyword-based NLP logic in `app/analyzer.py`.
