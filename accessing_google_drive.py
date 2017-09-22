__author__ = 'Bhagat'
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from encoder import *
from emailer import email as mail
from smtplib import SMTPRecipientsRefused

def update():
    scope = ['http://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
    client = gspread.authorize(creds)

    sheet = client.open('Security-camera (Responses)').sheet1
    leng=0
    action = 0
    while True:
        result = sheet.get_all_records()
        if leng!=len(result):
            action = result[len(result)-1]['Action: ']
            password = result[len(result)-1]['Activation-Key: '].lower()
            email = result[len(result)-1]['Email: ']
            done = result[len(result)-1]['Done:']

            if password==decode('mwj%w|xfhfxit%xu') and done=='Not Done':
                file = open('armed.txt','w')
                file.write(action)
                file.close()
                sheet.update_cell(len(result)+1,5,'Done')
                if email!='':
                    try:
                        if action=='turn off':
                            mail('Your action has been completed\nThe security camera has been turned off','ACTION COMPLETED',email_send=email)
                        else:
                            mail('Your action has been completed\nThe security camera has been '+action+'ed','ACTION COMPLETED',email_send=email)
                    except SMTPRecipientsRefused:
                        pass
            elif done!='Done':
                sheet.update_cell(len(result)+1,5,'Incorrect Key')
        leng=len(result)
        if action=='turn off':
            break
