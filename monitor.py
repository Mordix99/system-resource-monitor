import shutil
import json
import os
from dotenv import load_dotenv
import requests
import psutil
from datetime import datetime, timezone
import time

load_dotenv()

webhook_url = os.getenv("DISCORD_WEBHOOK_URL")


def load_json_file(file_path="config.json"):
    with open(file_path, "r") as file:
        return json.load(file)


def check_disk_usage(path="C:\\"):
    usage = shutil.disk_usage(path)
    percent_used = (usage.used / usage.total) * 100
    return percent_used


def send_discord_embed(webhook_url, title, description, color=15158332, fields=None):
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fields": fields or []
    }

    payload = {
        "embeds": [embed]
    }

    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Embed message sent successfully")
    else:
        print("Embed message failed to send")

def check_ram_usage():
    memory = psutil.virtual_memory()
    percent_used = memory.percent
    return percent_used

def main():
    if not webhook_url:
        print("Discord webhook URL is not set. Please check your .env file.")
        return

    config = load_json_file()
    disk_threshold = config.get("disk_threshold_percent", 80)
    ram_threshold = config.get("ram_threshold_percent", 85)
    interval = config.get("check_interval_seconds", 60)

    print(F"Starting monitor... checking every {interval} seconds. Disk threshold: {disk_threshold}%, RAM threshold: {ram_threshold}%")

    try:
        while True:
            disk_usage = check_disk_usage("C:\\")
            ram_usage = check_ram_usage()


            alerts = []
            fields = []


            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Disk Usage: {disk_usage:.2f}%, RAM Usage: {ram_usage:.2f}%")

            if disk_usage > disk_threshold:
                alerts.append("Disk space")
                fields.append({"name": "💾 Disk C:", "value": f"{disk_usage:.2f}% (Limit: {disk_threshold}%)", "inline": True})

            if ram_usage > ram_threshold:
                alerts.append("RAM memory")
                fields.append({"name": "🧠 RAM", "value": f"{ram_usage:.2f}% (Limit: {ram_threshold}%)", "inline": True})

            if alerts:
                title = "🚨 Resource Alert: " + ", ".join(alerts)
                description = "One or more resources exceeded the threshold limit!"
                send_discord_embed(webhook_url, title, description, color=15158332, fields=fields)
            else:
                print("All systems safe.")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")

if __name__ == "__main__":
    main()