from datetime import datetime
import pytz

def schedule_reminder(reminder_id, user_id, text, remind_at, application):

    # Converter string para datetime, se vier do SQLite
    if isinstance(remind_at, str):
        remind_at = datetime.fromisoformat(remind_at)

    # Telegram requer timezone-aware
    if remind_at.tzinfo is None:
        remind_at = remind_at.replace(tzinfo=pytz.UTC)

    async def send_reminder(context):
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🔔 Lembrete:\n{text}"
        )

    # Agenda usando run_once
    application.job_queue.run_once(
        send_reminder,
        when=remind_at,
        name=str(reminder_id)
    )
