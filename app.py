from backend import create_app
from backend.worker import celery_init_app
from backend.tasks import send_email, daily_reminder
from celery.schedules import crontab

app =create_app()
celery_app = celery_init_app(app)
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=7, minute =0, day_of_month=1),
        send_email.s("admin@email.com", "Test_Subject_Email")
    )
    sender.add_periodic_task(
        crontab(hour=19, minute=30,), daily_reminder.s("Daily Ad Reminder")
    )

if __name__ == "__main__":
    app.run(host= "127.0.0.1", port=5000, debug=True)
