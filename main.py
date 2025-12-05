import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from db import init_db, save_reminder, list_reminders, delete_reminder
from scheduler import schedule_reminder
from parser import parse_reminder

TOKEN = os.getenv("TOKEN")

async def start(update, context):
    await update.message.reply_text(
        "Olá! Eu sou seu bot de lembretes.\n\n"
        "Use:\n"
        "/lembrar <texto> em <tempo>\n"
        "/lembrar <texto> dia/hora\n"
        "/listar\n"
        "/cancelar <id>"
    )

async def lembrar(update, context):
    user_id = update.message.from_user.id
    text = " ".join(context.args)

    parsed = parse_reminder(text)
    if parsed is None:
        await update.message.reply_text("Não entendi a data/hora. Tente outro formato.")
        return

    reminder_text, remind_at = parsed
    reminder_id = save_reminder(user_id, reminder_text, remind_at)

    schedule_reminder(reminder_id, user_id, reminder_text, remind_at, context.application)

    await update.message.reply_text(
        f"⏰ Lembrete criado!\nID: {reminder_id}\nQuando: {remind_at}\nTexto: {reminder_text}"
    )

async def listar(update, context):
    user_id = update.message.from_user.id
    reminders = list_reminders(user_id)

    if not reminders:
        await update.message.reply_text("Você não tem lembretes.")
        return

    msg = "📋 *Seus lembretes:*\n\n"
    for r in reminders:
        msg += f"ID: {r[0]} — {r[2]} — {r[3]}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def cancelar(update, context):
    if not context.args:
        await update.message.reply_text("Use: /cancelar <id>")
        return

    reminder_id = context.args[0]
    if delete_reminder(reminder_id):
        await update.message.reply_text("❌ Lembrete cancelado!")
    else:
        await update.message.reply_text("ID não encontrado.")

def main():
    init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lembrar", lembrar))
    app.add_handler(CommandHandler("listar", listar))
    app.add_handler(CommandHandler("cancelar", cancelar))

    app.run_polling()

if __name__ == "__main__":
    main()
