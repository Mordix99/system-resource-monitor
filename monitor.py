import shutil
import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()

webhook_url = os.getenv("DISCORD_WEBHOOK_URL")


def load_json_file(file_path="config.json"):
    with open(file_path, "r") as file:
        return json.load(file)


def check_disk_usage(path="C:\\"):
    usage = shutil.disk_usage(path)
    percent_used = (usage.used / usage.total) * 100
    return percent_used


def send_to_discord(webhook_url, message):
    payload = {
        "content": message
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")



def main():
    if not webhook_url:
        print("Discord webhook URL is not set. Please check your .env file.")
        return

    config = load_json_file()
    threshold = config.get("disk_threshold_percent", 80)

    disk_usage = check_disk_usage("C:\\")
    print(f"Current disk usage: {disk_usage:.2f}%")

    if disk_usage > threshold:
        message = f"Warning: Disk usage has exceeded the threshold! Current usage: {disk_usage:.2f}%"
        send_to_discord(webhook_url, message)
    else:
        print("Disk usage is within the safe limit.")

if __name__ == "__main__":
    main()