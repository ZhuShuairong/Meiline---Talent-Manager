import schedule
import time
import subprocess
import datetime

def run_scrape():
    print(f"Running scrape.py at {datetime.datetime.now()}")
    subprocess.run(["python", "scrape.py"])  # Replace with python3 if needed

def check_time_and_schedule():
    current_minute = datetime.datetime.now().minute
    if current_minute in [0, 30]:  # Run at :00 or :30
        run_scrape()

# Schedule the check every minute
schedule.every(1).minutes.do(check_time_and_schedule)

print("Scheduler started. Waiting to run scrape.py at :00 or :30 each hour.")
while True:
    schedule.run_pending()
    time.sleep(60)  # Sleep for 1 minute