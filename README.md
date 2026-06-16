# Web Scraper Bot

A Python-based web scraper that monitors a notice board webpage and sends email notifications whenever a new notice is published.

The project is designed to run automatically using GitHub Actions, eliminating the need to keep a personal computer running 24/7.

---

## Features

* Monitors a notice board webpage at regular intervals.
* Detects newly published notices.
* Sends email notifications automatically.
* Stores the latest processed notice to prevent duplicate notifications.
* Supports GitHub Actions scheduled execution.
* Uses environment variables for secure credential management.

---

## Project Structure

```text
.
├── main.py
├── notice.json
├── requirements.txt
├── .env
└── .github
    └── workflows
        └── scraper.yml
```

### Files

| File                            | Description                                                                             |
| ------------------------------- | --------------------------------------------------------------------------------------  |
| `main.py`                       | Main scraper logic (customize the data format to your own scenario)                     |
| `notice.json`                   | Stores the latest processed notice                            scenario                          |
| `requirements.txt`              | Python dependencies                                                                     |
| `.env`                          | Local environment variables (not committed)                                             |
| `.github/workflows/scraper.yml` | GitHub Actions workflow                                                                 |

---

## Requirements

* Python 3.10+
* Gmail account
* Google App Password
* GitHub account (for scheduled execution)

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
SITE_URL=https://example.com/notices

SENDER_EMAIL=your_email@gmail.com
RECEIVER_EMAIL=receiver@gmail.com

GMAIL_APP_PASSWORD=your_app_password
```

### Variables

| Variable             | Description                              |
| -------------------- | ---------------------------------------- |
| `SITE_URL`           | Notice board URL                         |
| `SENDER_EMAIL`       | Gmail account used to send notifications |
| `RECEIVER_EMAIL`     | Email that receives notifications        |
| `GMAIL_APP_PASSWORD` | Google App Password                      |

---

## Gmail Setup

1. Enable Two-Factor Authentication on your Google account.
2. Open Google App Passwords.
3. Generate a new App Password.
4. Store the generated password in:

```env
GMAIL_APP_PASSWORD=
```

Do not use your normal Gmail password.

---

## Running Locally

```bash
python main.py
```

The scraper will:

1. Fetch the notice board.
2. Extract the latest notice.
3. Compare it with the stored notice.
4. Send an email if a new notice is detected.
5. Update `notices.json`.

---

## GitHub Actions Setup

Add the following repository secrets:

| Secret               | Value               |
| -------------------- | ------------------- |
| `SITE_URL`           | Notice board URL    |
| `SENDER_EMAIL`       | Sender Gmail        |
| `RECEIVER_EMAIL`     | Receiver email      |
| `GMAIL_APP_PASSWORD` | Google App Password |

Repository:

```text
Settings
└── Secrets and Variables
    └── Actions
```

---

## Example Workflow

```yaml
name: Notice Scraper

on:
  schedule:
    - cron: "*/10 * * * *"
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - run: pip install -r requirements.txt

      - run: python main.py
```

This workflow executes every 10 minutes.

---

## How New Notices Are Detected

The scraper stores the most recent notice in:

```json
{
    "date": "02-04-2026",
    "notice": "example title",
    "link": "additional link"
}

customize it with your own needs
```

Each run compares the latest notice from the website with the stored data.

If they differ:

1. Email notification is sent.
2. Stored data is updated.

---

## Security Notes

* Never commit `.env`.
* Never expose Gmail App Passwords.
* Store credentials using GitHub Secrets in production.

Add the following to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
```

---

## License

This project is provided for educational and personal use.
