from datetime import datetime, timedelta
from dateutil import parser as date_parser

def parse_reminder(text):
    text = text.lower().strip()

    # --- 1. Caso: tempo relativo ---
    if "em " in text:
        try:
            msg, time_part = text.split("em ", 1)
            msg = msg.strip()

            parts = time_part.split()
            qtd = int(parts[0])
            unidade = parts[1]

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
        except:
            return None

    # --- 2. Caso: tempo absoluto ---
    try:
        dt = date_parser.parse(text, fuzzy=True, dayfirst=True)

        # remove partes que são datas detectadas
        tokens = text.split()
        cleaned = []

        for token in tokens:
            try:
                date_parser.parse(token, fuzzy=False)
                # token é parte da data → não guardar
            except:
                cleaned.append(token)

        msg = " ".join(cleaned).strip()
        if msg == "":
            msg = "Lembrete"

        return msg, dt.isoformat()

    except:
        return None
