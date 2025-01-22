from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.job import Job
from pytz import timezone
import time
import os
from flask import Flask
from avoid_weekend_followups import main, rotate_logs  # Import the main function from avoid_weekend_followups.py

# Define the timezone
IST = timezone("Asia/Kolkata")

#Initialize Flask
app = Flask(__name__)

# Initialize BackgroundScheduler
scheduler = BackgroundScheduler()


# Schedule main function for Saturdays at 5:00 AM IST
scheduler.add_job(
    main,
    id="set_true_job",  # Unique job ID
    trigger=CronTrigger(day_of_week="wed", hour=17, minute=25, timezone=IST),
    kwargs={"action": "set_true"}
)

# Schedule main function for Mondays at 5:00 AM IST
scheduler.add_job(
    main,
    id="set_false_job",  # Unique job ID
    trigger=CronTrigger(day_of_week="wed", hour=17, minute=35, timezone=IST),
    kwargs={"action": "set_false"}
)

# Schedule log rotation on the 1st of every month at midnight IST
scheduler.add_job(
    rotate_logs,
    id="log_rotation_job",  # Unique job ID
    trigger=CronTrigger(day=22, hour=17, minute=40, timezone=IST)
)

# Function to check the status of jobs
def monitor_jobs():
    print("Checking job statuses...")
    for job in scheduler.get_jobs():
        if not job.next_run_time:
            print(f"Job {job.id} is not scheduled. Restarting...")
            # Restart the job based on its ID
            if job.id == "set_true_job":
                scheduler.add_job(
                    main,
                    id="set_true_job",
                    trigger=CronTrigger(day_of_week="wed", hour=17, minute=25, timezone=IST),
                    kwargs={"action": "set_true"}
                )
            elif job.id == "set_false_job":
                scheduler.add_job(
                    main,
                    id="set_false_job",
                    trigger=CronTrigger(day_of_week="wed", hour=17, minute=35, timezone=IST),
                    kwargs={"action": "set_false"}
                )
            elif job.id == "log_rotation_job":
                scheduler.add_job(
                    rotate_logs,
                    id="log_rotation_job",
                    trigger=CronTrigger(day=22, hour=17, minute=40, timezone=IST)
                )
            print(f"Job {job.id} restarted.")
        else:
            print(f"Job {job.id} is scheduled to run at {job.next_run_time}.")

# Start the scheduler
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

    # Initialize BackgroundScheduler
    scheduler = BackgroundScheduler()
    print("Scheduler is running...")
    scheduler.start()

    while True:
        monitor_jobs()  # Check job statuses every iteration
        time.sleep(60)  # Keep the script running and check every minute