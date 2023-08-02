import os

import psycopg2
import sched
import time
from datetime import datetime, timedelta
import threading

from dotenv import load_dotenv

load_dotenv()


def delete_old_bookings():
    # Replace the following with your PostgreSQL database credentials
    db_config = {
        'host': os.environ.get("DB_HOST"),
        'database': os.environ.get("DB_NAME"),
        'user': os.environ.get("DB_USER"),
        'password': os.environ.get("DB_PASSWORD")
    }

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_config)
    conn.autocommit = True
    cursor = conn.cursor()

    # Calculate the timestamp 10 minutes ago from the current time
    ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)

    try:
        # Delete rows older than ten minutes
        update_query = """
            UPDATE booking_table 
            SET booking_id = NULL 
            FROM booking_booking
            WHERE booking_table.booking_id = booking_booking.id
                AND booking_booking.created_at < %s
                AND booking_booking.paid = false
       """
        delete_query = "DELETE FROM booking_booking WHERE created_at < %s AND paid = false"
        cursor.execute(update_query, (ten_minutes_ago,))
        cursor.execute(delete_query, (ten_minutes_ago,))
        deleted_rows = cursor.rowcount

        print(f"{deleted_rows} row(s) deleted successfully.")

    except (Exception, psycopg2.Error) as error:
        print("Error while deleting rows:", error)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def run_scheduler():
    # Create a new scheduler
    scheduler = sched.scheduler(time.time, time.sleep)

    # Define the function to be executed every minute
    def delete_bookings():
        delete_old_bookings()
        # Schedule the next execution after 1 minute
        scheduler.enter(30, 1, delete_bookings, ())

    # Schedule the first execution after 1 minute
    scheduler.enter(30, 1, delete_bookings, ())

    # Run the scheduler
    scheduler.run()

if __name__ == "__main__":
    # Create a daemon thread to run the scheduler in the background
    background_thread = threading.Thread(target=run_scheduler, daemon=True)
    background_thread.start()

    try:
        # Keep the main thread running to allow the daemon to continue
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the daemon.")
