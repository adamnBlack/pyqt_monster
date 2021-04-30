import dialog
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

# import main


# pd.set_option('display.max_colwidth',1000)

version = '2.1r'
base_dir = "database"

# admin password = hkHK#j4@jh#@
# email='orders@gmonster.net'

email_failed = 0
total_email_downloaded = 0

sign_up_label = ""
sign_in_label = ""
signed_in = False

check_for_blocks = False
email_tracking_state = False

rid_list = []


# Create and configure logger
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
command_q = queue.Queue()
webhook_q = queue.Queue()
enable_webhook_status = False


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
tracking = {}

webhook_link = ""
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
    tracking = config['tracking']
    webhook_link = config['webhook_link']
except Exception as e:
    print("Exeception occured at config loading : {}".format(e))


def email_tracking_link():
    return f"https://www.google-analytics.com/collect?v=1&tid={tracking['analytics_account']}&cid=[**RID**]&aip=1&t=event&ec=email&ea=open&dp=%2Femail%2F{tracking['campaign_name']}&dt=Email"


delete_email_count = 0
stop_delete = False
group_a = pd.DataFrame()
group_b = pd.DataFrame()
target = pd.DataFrame()
db_path = "database/group.db"


# pyinstaller --onedir --icon=icons/icon.ico --name=GMonster --noconsole --noconfirm var.py
# pyi-makespec --onefile --icon=icons/icon.ico --name=GMonster --noconsole var.py
# pyinstaller --onefile --icon=icons/icon.ico --name=GMonster --noconsole --add-data="icons/icon.ico;imag" --add-data="icons/mail.ico;imag" --add-data="icons/email.ico;imag" var.py
# pyinstaller --onefile --icon=icons/icon.ico --name=GMonster --upx-dir=E:\Upwork\2020\upx-3.96-win64 GMonster.spec
# pyinstaller GMonster.spec
# a.datas += Tree('E:\\Upwork\\2020\\gmail_app\\gmail_app\\icons', prefix='icons\\')
