from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from json import load, dumps
from pyautogui import alert, password, confirm
import os
import sys
import pandas as pd
import queue
from collections import deque
from queue import LifoQueue
import logging
from threading import Thread
from database import engine, Group_A, Group_B, Targets, Base
from sqlalchemy.orm import sessionmaker
import main


# pd.set_option('display.max_colwidth',1000)

version = '1.4r'
base_dir = "database"

# admin password = hkHK#j4@jh#@
# email='orders@gmonster.net'

email_failed = 0
total_email_downloaded = 0

sign_up_label = ""
sign_in_label = ""
signed_in = False

#Create and configure logger
logging.basicConfig(filename=base_dir+"/app.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logging.getLogger("requests").setLevel(logging.WARNING)

compose_email_subject = "Just a friendly outreach about [3]"
compose_email_body = '''{Hey|Hi|Hello} [TONAME],

I'm reaching out to you because i {noticed|came across|found|visited} you website {the other day|yesterday} and thought you'd be interested in a {collaboration|partnership}.

{Hope you don't mind my outreach!|Looking forward to your reply!}

Regards,
[FIRSTFROMNAME]'''
compose_email_body_html = """\
<html>
    <body>
        <p>{Hey|Hi|Hello} [TONAME],<br>
        I'm reaching out to you because i {noticed|came across|found|visited} you website {the other day|yesterday} and thought you'd be interested in a {collaboration|partnership}.<br>
        {Hope you don't mind my outreach!|Looking forward to your reply!}<br>
        <a href="http://www.realpython.com">Real Python</a> 
        has many great tutorials.
        </p>
    </body>
</html>
"""
body_type = "Normal"

try:
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    # icon path
    mail_unread_icon = resource_path("icons/email.ico")
    mail_read_icon = resource_path("icons/mail.ico")
    # delete_icon = resource_path("icons/bin.svg")
    # deleted_icon = resource_path("icons/delete.svg")
    # icon path

except Exception as e:
    print(e)


files = []

inbox_data = pd.DataFrame()

email_in_view = {}

email_q = LifoQueue()
total_email = 0
row_pos = 0
thread_open = 0
acc_finished = 0
total_acc = 0
stop_download = False

thread_open_campaign = 0
stop_send_campaign = False
send_campaign_email_count = 0
send_campaign_run_status = False
download_email_status = False
send_report = queue.Queue()


limit_of_thread = 100

imap_server = 'imap.gmail.com'
imap_port = 993
smtp_server = "smtp.gmail.com"
smtp_port = 587

button_style = """QPushButton {
    color: rgb(255, 255, 255);
    border: 0px solid #555;
    border-radius: 3px;
    border-style: Solid;
    padding: 5px 28px;
    }
"""

# button_style = """QPushButton {
#     color: rgb(255, 255, 255);
#     border: 1px solid #555;
#     border-radius: 3px;
#     border-style: Solid;
#     background: qradialgradient(
#         cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
#         radius: 1.35, stop: 0 #e5e5e5, stop: 1 #4B7DAD
#         );
#     padding: 5px 28px;
#     }

# QPushButton:hover {
#     background: qradialgradient(
#         cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
#         radius: 1.35, stop: 0 #e5e5e5, stop: 1 #79d70f
#     }

# QPushButton:pressed {
#     border-style: inset;
#     background: qradialgradient(
#         cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,
#         radius: 1.35, stop: 0 #e5e5e5, stop: 1 #79d70f
#         );
#     }"""

num_emails_per_address = 0
delay_between_emails = ""
date = "8/24/2020"
limit_of_thread = 100
login_email = ""

api = "https://enzim.pythonanywhere.com/"
# api = "http://127.0.0.1:5000/"

gmail_provider = "https://gmonster.co/product/gmail-accounts/"
proxy_provider = "https://gmonster.co/product/gmonster-proxies/"

try:
    with open('{}/config.json'.format(base_dir)) as json_file:
        data = load(json_file)
    config = data['config']
    date = config['date']
    num_emails_per_address = config['num_emails_per_address']
    delay_between_emails = config['delay_between_emails']
    limit_of_thread = config['limit_of_thread']
    login_email = config['login_email']
except Exception as e:
    print("Exeception occured at config loading : {}".format(e))

# import dialog

delete_email_count = 0
stop_delete = False
group_a = pd.DataFrame()
group_b = pd.DataFrame()
target = pd.DataFrame()
db_path = "database/group.db"

def get_session():
    Session = sessionmaker(bind = engine)
    session = Session()

    return session

def db_update_row(row):
    global Group_A, Group_B, Targets
    try:
        session = get_session()

        if main.GUI.radioButton_db_groupa.isChecked():
            objects = session.query(Group_A).get(row['ID'])
            objects.FIRSTFROMNAME = row["FIRSTFROMNAME"]
            objects.LASTFROMNAME = row["LASTFROMNAME"]
            objects.EMAIL = row["EMAIL"]
            objects.EMAIL_PASS = row["EMAIL_PASS"]
            objects.PROXY_PORT = row["PROXY:PORT"]
            objects.PROXY_USER = row["PROXY_USER"]
            objects.PROXY_PASS = row["PROXY_PASS"]
        
        elif main.GUI.radioButton_db_groupb.isChecked():
            print(type(row["FIRSTFROMNAME"]))
            objects = session.query(Group_B).get(int(row['ID']))
            objects.FIRSTFROMNAME = row["FIRSTFROMNAME"]
            objects.LASTFROMNAME = row["LASTFROMNAME"]
            objects.EMAIL = row["EMAIL"]
            objects.EMAIL_PASS = row["EMAIL_PASS"]
            objects.PROXY_PORT = row["PROXY:PORT"]
            objects.PROXY_USER = row["PROXY_USER"]
            objects.PROXY_PASS = row["PROXY_PASS"]
        
        else:
            objects = session.query(Targets).get(row['ID'])
            objects.one = row["one"]
            objects.two = row["two"]
            objects.three = row["three"]
            objects.TONAME = row["TONAME"]
            objects.EMAIL = row["EMAIL"]
        
        session.commit()
        print("db updated")
        return True
    
    except Exception as e:
        session.rollback()
        print(f"Error at var.db_update_row : {e}")
        return False

def db_remove_row(id):
    global Group_A, Group_B, Targets
    try:
        session = get_session()

        if main.GUI.radioButton_db_groupa.isChecked():
            objects = session.query(Group_A).get(id)
        elif main.GUI.radioButton_db_groupb.isChecked():
            objects = session.query(Group_B).get(id)
        else:
            objects = session.query(Targets).get(id)
        
        if objects:
            session.delete(objects)
            session.commit()
            print("db updated")
            return True
        else:
            return False
    
    except Exception as e:
        session.rollback()
        print(f"Error at var.db_remove_row : {e}")
        return False

def db_insert_row():
    global Group_A, Group_B, Targets
    try:
        session = get_session()

        if main.GUI.radioButton_db_groupa.isChecked():
            objects = Group_A( 
                            FIRSTFROMNAME = "",
                            LASTFROMNAME = "",
                            EMAIL = "",
                            EMAIL_PASS = "",
                            PROXY_PORT = "",
                            PROXY_USER = "",
                            PROXY_PASS = ""
                    )
        elif main.GUI.radioButton_db_groupb.isChecked():
            objects = Group_B( 
                            FIRSTFROMNAME = "",
                            LASTFROMNAME = "",
                            EMAIL = "",
                            EMAIL_PASS = "",
                            PROXY_PORT = "",
                            PROXY_USER = "",
                            PROXY_PASS = ""
                    )
        else:
            objects = Targets( 
                            one = "",
                            two = "",
                            three = "",
                            TONAME = "",
                            EMAIL = ""
                    )
        
        session.add(objects)
        session.commit()
        print("db updated")
        return True, objects.id
    
    except Exception as e:
        session.rollback()
        print(f"Error at var.db_insert_rows : {e}")
        return False, None


def file_to_db():
    global Group_A, Group_B, Targets
    session = get_session()
    
    group_header = ['FIRSTFROMNAME', 'LASTFROMNAME', 'EMAIL', 'EMAIL_PASS', 'PROXY:PORT', 'PROXY_USER', 'PROXY_PASS']
    target_header = ['1', '2', '3', 'TONAME', 'EMAIL']
    group_a = pd.read_csv(base_dir+'/group_a.csv')
    group_b = pd.read_csv(base_dir+'/group_b.csv')
    target = pd.read_csv(base_dir+'/target.csv')
    
    if list(group_a.keys()) == group_header and list(group_b.keys()) == group_header and list(target.keys()) == target_header:
        group_a.fillna(" ", inplace=True)
        group_a = group_a.astype(str)
        group_a = group_a.loc[group_a['PROXY:PORT'] != " "]

        if len(group_a) > 0:
            objects = [ Group_A( 
                        FIRSTFROMNAME = row['FIRSTFROMNAME'],
                        LASTFROMNAME = row['LASTFROMNAME'],
                        EMAIL = row['EMAIL'],
                        EMAIL_PASS = row['EMAIL_PASS'],
                        PROXY_PORT = row['PROXY:PORT'],
                        PROXY_USER = row['PROXY_USER'],
                        PROXY_PASS = row['PROXY_PASS']
                        
                        ) for index, row in group_a.iterrows() ]

            session.add_all(objects)
        else:
            objects = Group_A(
                        id=1, 
                        FIRSTFROMNAME = "",
                        LASTFROMNAME = "",
                        EMAIL = "",
                        EMAIL_PASS = "",
                        PROXY_PORT = "",
                        PROXY_USER = "",
                        PROXY_PASS = ""
                        )
            session.add(objects)

        group_b.fillna(" ", inplace=True)
        group_b = group_b.astype(str)
        group_b = group_b.loc[group_b['PROXY:PORT'] != " "]
        
        if len(group_b) > 0:
            objects = [ Group_B( 
                        FIRSTFROMNAME = row['FIRSTFROMNAME'],
                        LASTFROMNAME = row['LASTFROMNAME'],
                        EMAIL = row['EMAIL'],
                        EMAIL_PASS = row['EMAIL_PASS'],
                        PROXY_PORT = row['PROXY:PORT'],
                        PROXY_USER = row['PROXY_USER'],
                        PROXY_PASS = row['PROXY_PASS']
                        
                        ) for index, row in group_b.iterrows() ]

            session.add_all(objects)
        else:
            objects = Group_B( 
                        id=1,
                        FIRSTFROMNAME = "",
                        LASTFROMNAME = "",
                        EMAIL = "",
                        EMAIL_PASS = "",
                        PROXY_PORT = "",
                        PROXY_USER = "",
                        PROXY_PASS = ""
                        )
            session.add(objects) 

        target.fillna(" ", inplace=True)
        target = target.astype(str)
        target = target.loc[target['EMAIL'] != " "]

        if len(target) > 0:
            objects = [ Targets( 
                        one = row['1'],
                        two = row['2'],
                        three = row['3'],
                        TONAME = row['TONAME'],
                        EMAIL = row['EMAIL']
                
                        ) for index, row in target.iterrows() ]

            session.add_all(objects)

        else:
            objects = Targets( 
                        id=1,
                        one = "",
                        two = "",
                        three = "",
                        TONAME = "",
                        EMAIL = ""
                        )
            session.add(objects) 
        
        session.commit()

    else:
        alert(text="Headers not matching!!!", title='Alert', button='OK')

def pandas_to_db():
    try:
        global group_a, group_b, target
        objects = [ Group_A( 
                        FIRSTFROMNAME = row['FIRSTFROMNAME'],
                        LASTFROMNAME = row['LASTFROMNAME'],
                        EMAIL = row['EMAIL'],
                        EMAIL_PASS = row['EMAIL_PASS'],
                        PROXY_PORT = row['PROXY:PORT'],
                        PROXY_USER = row['PROXY_USER'],
                        PROXY_PASS = row['PROXY_PASS']
                        
                        ) for index, row in group_a.iterrows() ]

        session.add_all(objects)

        objects = [ Group_B( 
                        FIRSTFROMNAME = row['FIRSTFROMNAME'],
                        LASTFROMNAME = row['LASTFROMNAME'],
                        EMAIL = row['EMAIL'],
                        EMAIL_PASS = row['EMAIL_PASS'],
                        PROXY_PORT = row['PROXY:PORT'],
                        PROXY_USER = row['PROXY_USER'],
                        PROXY_PASS = row['PROXY_PASS']
                        
                        ) for index, row in group_b.iterrows() ]

        session.add_all(objects)

        objects = [ Targets( 
                        one = row['1'],
                        two = row['2'],
                        three = row['3'],
                        TONAME = row['TONAME'],
                        EMAIL = row['EMAIL']
                
                        ) for index, row in target.iterrows() ]

        session.add_all(objects)
        print("Pandas to DB done!")
    except Exception as e:
        print(f"Error at var.pandas_to_db : {e}")


def db_to_pandas():
    global group_a, group_b, target, Group_A, Group_B, Targets
    session = get_session()
    
    results = session.query(Group_A).all()

    group_a_list = [ {
                'ID': item.id,
                'FIRSTFROMNAME': item.FIRSTFROMNAME,
                'LASTFROMNAME': item.LASTFROMNAME,
                'EMAIL': item.EMAIL,
                'EMAIL_PASS': item.EMAIL_PASS,
                'PROXY:PORT': item.PROXY_PORT,
                'PROXY_USER': item.PROXY_USER,
                'PROXY_PASS': item.PROXY_PASS
                }.copy() for item in results ]

    group_a = pd.DataFrame(group_a_list)

    results = session.query(Group_B).all()

    group_b_list = [ {
                'ID': item.id,
                'FIRSTFROMNAME': item.FIRSTFROMNAME,
                'LASTFROMNAME': item.LASTFROMNAME,
                'EMAIL': item.EMAIL,
                'EMAIL_PASS': item.EMAIL_PASS,
                'PROXY:PORT': item.PROXY_PORT,
                'PROXY_USER': item.PROXY_USER,
                'PROXY_PASS': item.PROXY_PASS
                }.copy() for item in results ]

    group_b = pd.DataFrame(group_b_list)


    results = session.query(Targets).all()

    targets_list = [ {
                'ID': item.id,
                '1': item.one,
                '2': item.two,
                '3': item.three,
                'TONAME': item.TONAME,
                'EMAIL': item.EMAIL
                }.copy() for item in results ]

    target = pd.DataFrame(targets_list)
    print(group_a.head(5))
    print(group_b.head(5))
    print(target.head(5))

def clear_table():
    global session, Group_A, Group_B, Targets
    try:
        session = get_session()
        
        session.query(Group_A).delete()
        session.query(Group_B).delete()
        session.query(Targets).delete()
        session.commit()
    except Exception as e:
        print("Exeception occured at clear db table : {}".format(e))
        alert(text="Exeception occured at clear db table : {}".format(e), title='Alert', button='OK')

def load_db():
    global group_a, group_b, target
    try:
        clear_table()
        file_to_db()
        db_to_pandas()
        alert(text="Database Loaded Successfully", title='Alert', button='OK')
    except Exception as e:
        session.rollback()
        print("Exeception occured at db loading : {}".format(e))
        alert(text="Exeception occured at db loading : {}".format(e), title='Alert', button='OK')

def startup_load_db(parent=None):
    global group_a, group_b, target
    try:
        session = get_session()
        if session.query(Group_A).first() == None and session.query(Group_B).first() == None:
            file_to_db()

        db_to_pandas()

    except Exception as e:
        session.rollback()
        print("Exeception occured at startup_db loading : {}".format(e))
        alert(text="Exeception occured at startup_db loading : {}".format(e), title='Alert', button='OK')

# Thread(target=startup_load_db, daemon=True, args=("dialog",)).start()
# startup_load_db()

# pyinstaller --onedir --icon=icons/icon.ico --name=GMonster --noconsole --noconfirm var.py
# pyi-makespec --onefile --icon=icons/icon.ico --name=GMonster --noconsole var.py
# pyinstaller --onefile --icon=icons/icon.ico --name=GMonster --noconsole --add-data="icons/icon.ico;imag" --add-data="icons/mail.ico;imag" --add-data="icons/email.ico;imag" var.py
# pyinstaller --onefile --icon=icons/icon.ico --name=GMonster --upx-dir=E:\Upwork\2020\upx-3.96-win64 GMonster.spec
# pyinstaller --onefile --name=GMonster GMonster.spec
# a.datas += Tree('E:\\Upwork\\2020\\gmail_app\\gmail_app\\icons', prefix='icons\\')