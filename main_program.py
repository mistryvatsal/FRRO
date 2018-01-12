#Flow of the program
#while loop --> scheduling for 7 am --> function 'update_database; --> function 'thread_row'
# --> scheduling for 8 am --> function 'check_date_match' --> if condition match --> .py file 'message_send' to send message and mail

import _thread    #threading
from datetime import datetime,timedelta    #checking date time of the system
import json
import schedule   #scheduling
import gspread                              #google spreadsheet api
from oauth2client.service_account import ServiceAccountCredentials    #authentiction
import message_send                     #python file for further mailing and messaging


global start_from

start_from=0


def thread_row(sheet,db_row,json_data,file):   #this thread is going to work continously for each student unless the task gets over

    def check_date_match(db_row):
        if(db_row['single visa']==1):    #if the visa is for the whole course .. then this should executed
            for i in range(1,5):         # for frro 1 to frro 4 ; checking if the todays date matches with any
                day_1=datetime.strptime(db_row['frro %d'%(i)+'(rc/rp)_start'],'%Y-%m-%d')+timedelta(days=1)     #timedelta adds days to the given date  ... Hence we save all the notifications date in variable
                day_2=datetime.strptime(db_row['frro %d'%(i)+'(rc/rp)_start'],'%Y-%m-%d')+timedelta(days=2)
                day_3=datetime.strptime(db_row['frro %d'%(i)+'(rc/rp)_start'],'%Y-%m-%d')+timedelta(days=3)
                day_9=datetime.strptime(db_row['frro %d'%(i)+'(rc/rp)_start'],'%Y-%m-%d')+timedelta(days=9)
                day_10=datetime.strptime(db_row['frro %d'%(i)+'(rc/rp)_start'],'%Y-%m-%d')+timedelta(days=10)
                day_11=datetime.strptime(db_row['frro %d'%(i)+'(rc/rp)_start'],'%Y-%m-%d')+timedelta(days=11)

                try:
                    if(datetime.now().date()==day_1 or  datetime.now().date()==day_2 or  datetime.now().date()==day_3 or  datetime.now().date()==day_9 or  datetime.now().date()==day_10 or  datetime.now().date()==day_11):      #column 12
                        message_send.send_message(db_row['contact Number'],db_row['email'])
                except: pass

        # if(db_row['single_visa']==0):    # if the visa is not for the whole course and needs renewel in between
        #
        #     day_1=datetime.strptime(db_row['visa issue date'],'%Y-%m-%d')+timedelta(days=1)

    if(  datetime.now().date() < (datetime.strptime(db_row['frro 4(rc/rp) start'],'%Y-%m-%d'))+timedelta(days=14)   ):
            schedule.every().day.at("08:00").do(lambda:check_date_match(db_row))           #checking the date every date at 9:00

    else:
        del json_data[ db_row['name of student'] ]     #the task of the student is completed hence to remove the name from the json file
        f=open('data.json','w')
        f.write(json.dumps(json_data))


def update_database():    #taking data from the sheets at regular intervals 7:00 am
    try:
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret_key.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open('FRRO TRIAL').sheet1
        db=sheet.get_all_records()       #taking all the records

        file=open('data.json','r')
        json_data=json.load(file)
        file.close()

        for i in range(start_from,len(db)):      #for all the records .. making a thread of each row i.e. for each person.
            if(db[i]['name of student'] not in json_data.keys()):     #checking if the name present in data.json
                json_data[  db[i]['name of student']  ]="started"    #if name not present ; then add the name and start the thread of it
                f=open('data.json','w')
                f.write(json.dumps(json_data))
                f.close()
                _thread.start_new_thread(thread_row,(sheet,db[i],json_data,file))  #thread created for each student

    except:
        schedule.every(1).minute.do(update_database)
schedule.every().day.at("07:00").do(update_database)    #checks every day and updates the datebase

while True:
    schedule.run_pending()











