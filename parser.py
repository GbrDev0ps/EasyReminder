from datetime import datetime, timedelta
from dateutil import parser as date_parser
import re
import pytz

BR_TZ = pytz.timezone("America/Sao_Paulo")


WEEKDAYS = {
    "segunda": 0,
    "terça": 1, "terca": 1,
    "quarta": 2,
    "quinta": 3,
    "sexta": 4,
    "sábado": 5, "sabado": 5,
    "domingo": 6,
}

def next_weekday(target):
    """Retorna o próximo datetime para o dia da semana desejado."""
    today = datetime.now(BR_TZ)
    days_ahead = target - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return today + timedelta(days=days_ahead)


def parse_relative(text):
    """Parses: 'em X min', 'em X horas', 'daqui X minutos', etc"""
    pad = text.lower().strip()

    regex = r"(em|daqui)\s+(\d+)\s*(minutos|min|hora|horas|dia|dias)"
    m = re.search(regex, pad)

    if not m:
        return None

    qtd = int(m.group(2))
    unidade = m.group(3)

    if "min" in unidade:
        dt = datetime.now(BR_TZ) + timedelta(minutes=qtd)
    elif "hora" in unidade:
        dt = datetime.now(BR_TZ) + timedelta(hours=qtd)
    else:
        dt = datetime.now(BR_TZ) + timedelta(days=qtd)

    # Remove a parte de tempo para sobrar apenas o texto final
    msg = re.sub(regex, "", pad).strip()
    if not msg:
        msg = "Lembrete"

    return msg, dt


def parse_weekday(text):
    """Parses: 'segunda 10h', 'sábado às 14h', etc"""
    pad = text.lower()

    for name, idx in WEEKDAYS.items():
        if name in pad:
            dt = next_weekday(idx)

            # Extrair hora — qualquer formato: “10”, “10h”, “10:30”, “às 10h”
            m = re.search(r"(\d{1,2})(h|:\d{2})?", pad)
            if m:
                hour = int(m.group(1))
                minute = 0

                if m.group(2) and ":" in m.group(2):
                    minute = int(m.group(2)[1:])

                dt = dt.replace(hour=hour, minute=minute, second=0)

            msg = pad
            # Remover partes que são dia / hora
            msg = re.sub(name, "", msg)
            msg = re.sub(r"às?", "", msg)
            msg = re.sub(r"\d{1,2}(h|:\d{2})?", "", msg)
            msg = msg.strip()
            if not msg:
                msg = "Lembrete"

            return msg, dt

    return None


def parse_absolute(text):
    """Parses datas completas e horários detectados automaticamente."""
    try:
        dt = date_parser.parse(text, fuzzy=True, dayfirst=True)

        # Remover tokens que claramente são datas/horas
        tokens = text.split()
        cleaned = []

        for token in tokens:
            try:
                date_parser.parse(token, fuzzy=False)
            except:
                cleaned.append(token)

        msg = " ".join(cleaned).strip()
        if not msg:
            msg = "Lembrete"

        # Tornar timezone-aware
        dt = BR_TZ.localize(dt)
        return msg, dt

    except:
        return None


def parse_reminder(text):
    """
    Parser principal.
    Retorna: (mensagem, datetime) ou None
    """

    # 1) relativo
    rel = parse_relative(text)
    if rel:
        return rel

    # 2) dia da semana
    wd = parse_weekday(text)
    if wd:
        return wd

    # 3) absoluto (data/hora completa)
    absd = parse_absolute(text)
    if absd:
        return absd

    return None
