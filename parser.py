from datetime import datetime, timedelta
from dateutil import parser

def parse_reminder(text):
    try:
        # Caso 1: relativo → "em 10 minutos"
        if "em " in text:
            msg, time_part = text.split("em ", 1)
            msg = msg.strip()

            qtd, unidade = time_part.split(" ", 1)
            qtd = int(qtd)

            if "min" in unidade:
                delta = timedelta(minutes=qtd)
            elif "hora" in unidade:
                delta = timedelta(hours=qtd)
            elif "dia" in unidade:
                delta = timedelta(days=qtd)
            else:
                return None

            remind_at = datetime.now() + delta
            return msg, remind_at.isoformat()

        # Caso 2: data/hora absoluta
        dt = parser.parse(text, fuzzy=True)
        msg = text.split(str(dt.date()))[0].strip()
        return msg, dt.isoformat()

    except:
        return None
