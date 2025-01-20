import schedule
import time
from apscheduler.schedulers.background import BackgroundScheduler
from avoid_weekend_followups import main, rotate_logs  # Import the main function from your_main_script.py

# Schedule the main function
schedule.every().saturday.at("05:00" , "Asia/Kolkata").do(main, action="set_true")  # Runs main() at 5:00 AM on Saturdays
schedule.every().monday.at("05:00" , "Asia/Kolkata").do(main, action="set_false")    # Runs main() at 5:00 AM on Mondays

# Start the scheduler
if __name__ == "__main__":
    # Schedule log rotation on the 1st of every month at midnight
    scheduler = BackgroundScheduler()
    scheduler.add_job(rotate_logs, 'cron', day=1, hour=0, minute=0)  # First day of every month at midnight
    scheduler.start()

# Keep the script running
    try:
        print("Scheduler is running in the background. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)  # Keeps the script alive
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # Shut down the scheduler gracefully
        print("Scheduler stopped.")
        
    print("Scheduler is running...")
    while True:
        schedule.run_pending()  # Check if a scheduled job needs to run
        time.sleep(60)          # Wait for a minute before checking again
