from bs4 import BeautifulSoup
import requests
from pprint import pprint
from Google import Create_Service


google_sheets_url = 'https://docs.google.com/spreadsheets/d/1u7PbhfRWa_Scnxvv-qozHqp7_xnitB4-c3K33_fitlk/edit#gid=0'
CLIENT_SECRET_FILE = 'secret.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']
service_sheets = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES_SHEETS)


url = 'https://app.redeemer.com/content/misc/year4archive'
urls = []

result = requests.get(url)
soup = BeautifulSoup(result.text, 'html.parser')
a_tags = soup.find_all('a')

for a in a_tags:
    urls.append(a.get('href'))


pages = []
titles = []
for url in urls: 

    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    ps = soup.find_all('p')
    hs = soup.find_all('h2')
    prs = []
    h2s = []
    for h in hs:
        h2s.append(h.get_text())
    for p in ps:
        prs.append(p.get_text())
    pages.append(h2s)
    pages.append(prs)
   
     
    
print(pages)
spreadsheet_id = '1y70aURa3VmEnAVF3i8vPpKRhj1z_pkNsgWeRRmMe6fA'

#create new worksheet
google_worksheet = service_sheets.spreadsheets().batchUpdate(
    spreadsheetId = spreadsheet_id,
    body={
        'requests': [
            {
                    'addSheet': {}
            }
            ]
            
        }
    ).execute()
    
pprint(google_worksheet)
    
    # insert column headers
service_sheets.spreadsheets().values().update(
        spreadsheetId = spreadsheet_id,
        valueInputOption = 'USER_ENTERED',
        range='{0}!A1'.format(google_worksheet['replies'][0]['addSheet']['properties']['title']),
        body={
            'majorDimension': 'ROWS',
            'values': pages,
        }
    ).execute()


 

