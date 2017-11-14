from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime


def get_credentials(flags, secrets_abspath):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    CLIENT_SECRET_FILE = secrets_abspath
    APPLICATION_NAME = 'Google Calendar API Python Quickstart'

    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags=flags)
        print('Storing credentials to ' + credential_path)
    return credentials


class GoogleCalendarService:
    def __init__(self, secrets_abspath):
        credentials = get_credentials(flags=None, secrets_abspath=secrets_abspath)
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)

    def get_next(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    def get_events(self, start_date: datetime, end_date: datetime, calendar_id="primary", results=250) -> list:
        start_date = start_date.isoformat() + 'Z'
        end_date = end_date.isoformat() + 'Z'
        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            maxResults=results
        ).execute()
        return events_result.get('items')

    def update_event(self, event_id: str, update: dict, calendar_id='primary') -> dict:
        event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
        event.update(update)
        updated_event = self.service.events().update(calendarId=calendar_id, eventId=event['id'], body=event).execute()
        return updated_event

if __name__ == '__main__':
    cal = GoogleCalendarService()
    cal.get_next()
    print('done')
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=7)
    stuff = cal.get_events(start_date=start, end_date=end)
    print(stuff)
