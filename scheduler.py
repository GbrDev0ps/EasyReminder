from datetime import datetime

def schedule_reminder(reminder_id, user_id, text, remind_at, application):
    # Converte string para datetime se necessário
    if isinstance(remind_at, str):
        remind_at = datetime.fromisoformat(remind_at)

    async def send_reminder(context):
        await context.bot.send_message(chat_id=user_id, text=f"🔔 Lembrete:\n{text}")

    # Calcula quanto tempo falta
    now = datetime.now()
    delay_seconds = (remind_at - now).total_seconds()

    if delay_seconds <= 0:
        # Se a hora já passou, dispara instantaneamente
        delay_seconds = 1

    # Agenda o lembrete em X segundos
    application.job_queue.run_once(
        send_reminder,
        when=delay_seconds,
        name=str(reminder_id)
