import logging
import os
from telegram.ext import Application, CommandHandler
from db import init_db, save_reminder, list_reminders, delete_reminder
from scheduler import schedule_reminder
from parser import parse_reminder

TOKEN = os.getenv("TOKEN")   # Configure isso no Railway!

async def start(update, context):
    await update.message.reply_text(
        "Olá! 👋 Eu sou seu bot de lembretes.\n\n"
        "Use /ajuda para ver como criar lembretes."
    )

# --------------------
# /AJUDA INTELIGENTE
# --------------------
async def ajuda(update, context):
    msg = (
        "📘 *Como usar o bot de lembretes*\n\n"
        "Você pode criar lembretes usando vários formatos:\n\n"

        "🕒 *Tempo relativo*\n"
        "`/lembrar tomar água em 10 minutos`\n"
        "`/lembrar alongar em 2 horas`\n"
        "`/lembrar pagar conta em 3 dias`\n\n"

        "📅 *Dia da semana*\n"
        "`/lembrar academia segunda 19h`\n"
        "`/lembrar mercado sábado às 14h`\n\n"

        "📆 *Data específica*\n"
        "`/lembrar pagar boleto dia 20 às 15h`\n"
        "`/lembrar médico 20/12 09:30`\n"
        "`/lembrar reunião amanhã 8h`\n"
        "`/lembrar estudo hoje 18h`\n\n"

        "⏳ *Horário direto*\n"
        "`/lembrar café 15h`\n\n"

        "📋 *Outros comandos:*\n"
        "• `/listar` — mostra todos os seus lembretes\n"
        "• `/cancelar <id>` — apaga um lembrete\n"
        "• `/ajuda` — mostra esta mensagem\n\n"

        "🔔 *Dica:* O bot entende datas e horários automaticamente!"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

# --------------------
# CRIAR LEMBRETE
# --------------------
async def lembrar(update, context):
    user_id = update.message.from_user.id
    text = " ".join(context.args)

    parsed = parse_reminder(text)
    if parsed is None:
        await update.message.reply_text(
            "⚠ Não consegui entender a data/hora.\n"
            "Use /ajuda para ver formatos aceitos."
        )
        return

    reminder_text, remind_at = parsed
    reminder_id = save_reminder(user_id, reminder_text, remind_at)

    schedule_reminder(
        reminder_id,
        user_id,
        reminder_text,
        remind_at,
        context.application
    )

    await update.message.reply_text(
        f"⏰ *Lembrete criado!*\n"
        f"ID: `{reminder_id}`\n"
        f"Quando: `{remind_at}`\n"
        f"Texto: _{reminder_text}_",
        parse_mode="Markdown"
    )

# --------------------
# LISTAR LEMBRETES
# --------------------
async def listar(update, context):
    user_id = update.message.from_user.id
    reminders = list_reminders(user_id)

    if not reminders:
        await update.message.reply_text("Você não tem lembretes.")
        return

    msg = "📋 *Seus lembretes:*\n\n"
    for r in reminders:
        msg += f"ID `{r[0]}` — `{r[3]}` — _{r[2]}_\n"

    await update.message.reply_text(msg, parse_mode="Markdown")

# --------------------
# CANCELAR LEMBRETE
# --------------------
async def cancelar(update, context):
    if not context.args:
        await update.message.reply_text("Use: /cancelar <id>")
        return

    reminder_id = context.args[0]
    if delete_reminder(reminder_id):
        await update.message.reply_text("❌ Lembrete cancelado!")
    else:
        await update.message.reply_text("ID não encontrado.")

# --------------------
# MAIN
# --------------------
def main():
    init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(CommandHandler("lembrar", lembrar))
    app.add_handler(CommandHandler("listar", listar))
    app.add_handler(CommandHandler("cancelar", cancelar))

    print("🤖 Bot online com JobQueue ativa!")
    app.run_polling()

if __name__ == "__main__":
    main()
