from datetime import datetime

def schedule_reminder(reminder_id, user_id, text, remind_at, application):

    if isinstance(remind_at, str):
        remind_at = datetime.fromisoformat(remind_at)

    async def send_reminder(context):
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🔔 Lembrete:\n{text}"
        )

    application.job_queue.run_at(
        send_reminder,
        when=remind_at,
        name=str(reminder_id)
    )
