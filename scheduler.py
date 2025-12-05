from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from db import delete_reminder

scheduler = AsyncIOScheduler()
scheduler.start()

def schedule_reminder(reminder_id, user_id, text, remind_at, app):
    remind_datetime = datetime.fromisoformat(remind_at)

    scheduler.add_job(
        send_notification,
        "date",
        run_date=remind_datetime,
        args=[reminder_id, user_id, text, app]
    )

async def send_notification(reminder_id, user_id, text, app):
    await app.bot.send_message(
        chat_id=user_id,
        text=f"🔔 Lembrete:\n{text}"
    )
    delete_reminder(reminder_id)
