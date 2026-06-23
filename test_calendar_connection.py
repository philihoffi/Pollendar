"""
Test-Skript für die Google Calendar API Verbindung.

Verwendung:
  python test_calendar_connection.py

Setzt voraus, dass .env mit CALENDAR_ID und CREDENTIALS_PATH gefüllt ist
und credentials/service_account.json existiert.
"""

import logging
import os
import sys
from datetime import datetime, timedelta

from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
)

load_dotenv()

CALENDAR_ID = os.getenv('CALENDAR_ID', '')
CREDENTIALS_PATH = os.path.join(PROJECT_ROOT, 'credentials', 'service_account.json')

if not CALENDAR_ID:
    print('❌ CALENDAR_ID ist in .env nicht gesetzt.')
    sys.exit(1)

if not os.path.isfile(CREDENTIALS_PATH):
    print(f'❌ Datei nicht gefunden: {CREDENTIALS_PATH}')
    print('   Lege die service_account.json im Ordner credentials/ ab.')
    sys.exit(1)

from src.calendar_client import GoogleCalendarClient
from src.utils.helpers import TZ


def main():
    print('🔌 Teste Verbindung zu Google Calendar ...')
    print(f'   Kalender-ID: {CALENDAR_ID}')
    print(f'   Credentials: {CREDENTIALS_PATH}')
    print()

    client = GoogleCalendarClient(CALENDAR_ID, CREDENTIALS_PATH)

    # ── 1. Events auflisten ──────────────────────────────────
    print('📋 1. Vorhandene Events abrufen (heute + 7 Tage) ...')
    try:
        today = datetime.now(TZ).date()
        events = client.list_events(today, today + timedelta(days=7))
        print(f'   ✅ Erfolg: {len(events)} Event(s) gefunden.')
        for ev in events:
            print(f'      - {ev["title"]} (ID: {ev["id"]})')
    except Exception as e:
        print(f'   ❌ Fehler: {e}')
        sys.exit(1)

    print()

    # ── 2. Test-Event anlegen ────────────────────────────────
    print('✏️  2. Test-Event anlegen ...')
    test_title = f'🔧 Test-Event ({datetime.now(TZ).strftime("%H:%M:%S")})'
    start_dt = datetime.now(TZ).replace(microsecond=0) + timedelta(hours=1)
    end_dt = start_dt + timedelta(hours=1)

    try:
        full_id = client.add_event(test_title, start_dt, end_dt)
        short_id = full_id[:8]
        print(f'   ✅ Erfolg: Event-ID = {full_id}')
        print(f'      Kurz-ID  = {short_id}')
        print(f'      Titel    = {test_title}')
        print(f'      Start    = {start_dt.strftime("%d.%m.%Y %H:%M")}')
        print(f'      Ende     = {end_dt.strftime("%d.%m.%Y %H:%M")}')
    except Exception as e:
        print(f'   ❌ Fehler: {e}')
        sys.exit(1)

    print()

    # ── 3. Event per Kurz-ID suchen ──────────────────────────
    print(f'🔍 3. Event per Kurz-ID "{short_id}" suchen ...')
    try:
        found_full = client._search_by_short_id(short_id)
        if found_full:
            print(f'   ✅ Erfolg: Volle ID = {found_full}')
        else:
            print(f'   ❌ Fehler: Event nicht gefunden.')
            sys.exit(1)
    except Exception as e:
        print(f'   ❌ Fehler: {e}')
        sys.exit(1)

    print()

    # ── 4. Event löschen ─────────────────────────────────────
    print('🗑️  4. Test-Event löschen ...')
    try:
        deleted_title = client.delete_event(short_id)
        print(f'   ✅ Erfolg: "{deleted_title}" gelöscht.')
    except Exception as e:
        print(f'   ❌ Fehler: {e}')
        sys.exit(1)

    print()
    print('✅ Alle Tests bestanden – Google Calendar Verbindung funktioniert.')


if __name__ == '__main__':
    main()