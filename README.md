# System Resource Monitor

[![CI Pipeline](https://github.com/Mordix99/system-resource-monitor/actions/workflows/ci.yml/badge.svg)](https://github.com/Mordix99/system-resource-monitor/actions/workflows/ci.yml)

Lightweight tool to monitor system resources (disk and RAM) in real time and send alert notifications via Discord Webhook embeds.

## Features

- Real-time disk (`shutil`) and RAM (`psutil`) resource monitoring.
- Alert notifications formatted as Discord Rich Embeds.
- Configurable thresholds and check intervals via `config.json`.
- Secure credential management using environment variables (`.env`).
- Containerized application ready to deploy (`python:3.11-slim`).
- Automated CI/CD pipeline running code linting (`ruff`) and test container builds.

## Technologies

- Python 3.11
- Libraries: `psutil`, `requests`, `python-dotenv`
- Docker
- GitHub Actions

## Configuration

1. Configure `config.json`:
```json
{
  "disk_threshold": 80.0,
  "ram_threshold": 85.0,
  "check_interval_seconds": 60,
  "disk_path": "/"
}
```

2. Create `.env` file with Discord webhook URL:
```env
DISCORD_WEBHOOK_URL=(https://discord.com/api/webhooks/)...
```

3. Start locally:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python monitor.py
```

4. Run in Docker:
```bash
docker build -t system-monitor:latest .
docker run -d --name resource-monitor --env-file .env system-monitor:latest
```