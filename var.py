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

# import main


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
# compose_email_subject = ""
# compose_email_body = ""

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
email_scraper = "https://gmonster.co/product/targeted-email-leads/"
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

import dialog

delete_email_count = 0
stop_delete = False
group_a = pd.DataFrame()
group_b = pd.DataFrame()
target = pd.DataFrame()
def load_db(parent=None):
    global group_a, group_b, target
    try:
        group_a = pd.read_csv(base_dir+'/group_a.csv')
        group_a.fillna(" ", inplace=True)
        group_a = group_a.astype(str)
        group_a.insert(0,'flag', '')
        group_a['flag'] = 0
        group_a = group_a.loc[group_a['PROXY:PORT'] != " "]
        print(group_a.head(5))
        group_b = pd.read_csv(base_dir+'/group_b.csv')
        group_b.fillna(" ", inplace=True)
        group_b = group_b.astype(str)
        group_b.insert(0,'flag', '')
        group_b['flag'] = 0
        group_b = group_b.loc[group_b['PROXY:PORT'] != " "]
        print(group_b.head(5))
        target = pd.read_csv(base_dir+'/target.csv')
        target.fillna(" ", inplace=True)
        target = target.astype(str)
        target.insert(0,'flag', '')
        target['flag'] = 0
        target = target.loc[target['EMAIL'] != " "]
        print(target.head(5))
        if parent=="var":
            # from main import GUI
            # GUI.label_email_status.setText("Database Loaded")
            print("Database loaded")
        elif parent=='dialog':
            print("DB loaded")
        else:
            alert(text='Database Loaded', title='Alert', button='OK')
    except Exception as e:
        print("Exeception occured at db loading : {}".format(e))
        alert(text="Exeception occured at db loading : {}".format(e), title='Alert', button='OK')

# Thread(target=load_db, daemon=True, args=("dialog",)).start()

# pyinstaller --onedir --icon=icons/icon.ico --name=GMonster --noconsole --noconfirm var.py
# pyi-makespec --onefile --icon=icons/icon.ico --name=GMonster --noconsole var.py
# pyinstaller --onefile --icon=icons/icon.ico --name=GMonster --noconsole --add-data="icons/icon.ico;imag" --add-data="icons/mail.ico;imag" --add-data="icons/email.ico;imag" var.py
# pyinstaller --onefile --icon=icons/icon.ico --name=GMonster --upx-dir=E:\Upwork\2020\upx-3.96-win64 GMonster.spec
# pyinstaller --onefile --name=GMonster GMonster.spec
# a.datas += Tree('E:\\Upwork\\2020\\gmail_app\\gmail_app\\icons', prefix='icons\\')