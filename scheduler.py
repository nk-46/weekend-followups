from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
import time
from avoid_weekend_followups import main, rotate_logs  # Import the main function from avoid_weekend_followups.py

# Define the timezone
IST = timezone("Asia/Kolkata")

# Initialize BackgroundScheduler
scheduler = BackgroundScheduler()

# Schedule main function for Saturdays at 5:00 AM IST
scheduler.add_job(
    main,
    trigger=CronTrigger(day_of_week="sat", hour=5, minute=0, timezone=IST),
    kwargs={"action": "set_true"}
)

# Schedule main function for Mondays at 5:00 AM IST
scheduler.add_job(
    main,
    trigger=CronTrigger(day_of_week="mon", hour=5, minute=0, timezone=IST),
    kwargs={"action": "set_false"}
)

# Schedule log rotation on the 1st of every month at midnight IST
scheduler.add_job(
    rotate_logs,
    trigger=CronTrigger(day=1, hour=0, minute=0, timezone=IST)
)

# Start the scheduler
if __name__ == "__main__":
    print("Scheduler is running...")
    scheduler.start()

    try:
        while True:
            time.sleep(60)  # Keep the script running
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # Gracefully shut down the scheduler
        print("Scheduler stopped.")
