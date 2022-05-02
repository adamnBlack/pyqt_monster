import traceback
from json import load, dumps
import pandas as pd
import queue
from queue import LifoQueue
from win32event import CreateMutex
from win32api import CloseHandle, GetLastError
from winerror import ERROR_ALREADY_EXISTS
from pyautogui import alert
from apscheduler.schedulers.background import BackgroundScheduler
from logger import logger

# pd.set_option('display.max_colwidth',1000)
import sys, os


def override_where():
    """ overrides certifi.core.where to return actual location of cacert.pem"""
    # change this to match the location of cacert.pem
    return os.path.abspath(os.path.join(os.getcwd(), "database", "cacert.pem"))


# is the program compiled?
if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where

    # delay importing until after where() has been replaced
    import requests
    import requests.utils
    import requests.adapters

    # replace these variables in case these modules were
    # imported before we replaced certifi.core.where
    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()
else:
    import requests


class SingleInstance:
    """ Limits application to single instance """

    def __init__(self):
        self.mutexname = "testmutex_{D0E858DF-985E-4907-B7FB-8D732C3FC3B9}"
        self.mutex = CreateMutex(None, False, self.mutexname)
        self.lasterror = GetLastError()

    def already_running(self):
        return self.lasterror == ERROR_ALREADY_EXISTS

    def __del__(self):
        if self.mutex:
            CloseHandle(self.mutex)

try:
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)


    # icon path
    mail_unread_icon = resource_path("icons/email.ico")
    mail_read_icon = resource_path("icons/mail.ico")

    # webhook_fired = resource_path("icons/webhook_fired.png")
    # webhook_not_fired = resource_path("icons/webhook_not_fired.png")

    # delete_icon = resource_path("icons/bin.svg")
    # deleted_icon = resource_path("icons/delete.svg")
    # icon path

except Exception as e:
    print(e)

version = '2.2r'
base_dir = "database"
followup_report_file_path = "followup_report.csv"

# Create and configure logger
# logging.basicConfig(filename=base_dir + "/app.log",
#                     format='%(asctime)s %(message)s',
#                     filemode='a')
#

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

# admin password = hkHK#j4@jh#@
# email='orders@gmonster.net'

scheduler = BackgroundScheduler(logger=logger)
scheduler.start()

db_file_loading_config = {
    "group_a": True,
    "group_b": True,
    "target": True
}

add_custom_hostname = False

email_failed = 0
total_email_downloaded = 0
# in seconds
waiting_period_for_followup = 600

sign_up_label = ""
sign_in_label = ""
signed_in = False

check_for_blocks = False
email_tracking_state = False

rid_list = []

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
remove_email_from_target = False

limit_of_thread = 100

imap_server = 'imap.gmail.com'
imap_port = 993
smtp_server = "smtp.gmail.com"
smtp_port = 587
# smtp_port = 465

button_style = """QPushButton {
    color: rgb(255, 255, 255);
    border: 0px solid #555;
    border-radius: 3px;
    border-style: Solid;
    padding: 5px 28px;
    }
"""

date = "8/24/2020"
num_emails_per_address = 0
delay_between_emails = ""
limit_of_thread = 100
login_email = ""
tracking = {}

webhook_link = ""
api = "https://enzim.pythonanywhere.com/"
# api = "http://127.0.0.1:5000/"

gmail_provider = "https://gmonster.co/product/gmail-accounts/"
proxy_provider = "https://gmonster.co/product/gmonster-proxies/"

responses_webhook_enabled = False
inbox_blacklist = []

try:
    with open('{}/config.json'.format(base_dir)) as json_file:
        data = load(json_file)
    config = data['config']
    date = config['date']
    if config['compose_email_subject']:
        compose_email_subject = config['compose_email_subject']
    if config['compose_email_body']:
        compose_email_body = config['compose_email_body']
    if config['compose_email_body_html']:
        compose_email_body_html = config['compose_email_body_html']
    num_emails_per_address = config['num_emails_per_address']
    delay_between_emails = config['delay_between_emails']
    limit_of_thread = config['limit_of_thread']
    login_email = config['login_email']
    tracking = config['tracking']
    webhook_link = config['webhook_link']
    check_for_blocks = config['check_for_blocks']
    remove_email_from_target = config['remove_email_from_target']
    add_custom_hostname = config['custom_hostname']
    enable_webhook_status = config['enable_webhook']
    email_tracking_state = config['enable_email_tracking']
    campaign_group = config['campaign_group']
    body_type = config['body_type']
    target_blacklist = config['target_blacklist']
    inbox_blacklist = config['inbox_blacklist']
    responses_webhook_enabled = config['responses_webhook_enabled']
    followup_enabled = config['followup_enabled']
    followup_days = config['followup_days']
    followup_subject = config['followup_subject']
    followup_body = config['followup_body']
except Exception as e:
    print("Exception occurred at config loading : {}".format(e))

delay_start = int(delay_between_emails.split("-")[0].strip())
delay_end = int(delay_between_emails.split("-")[1].strip())


def email_tracking_link():
    return f"https://www.google-analytics.com/collect?v=1&tid={tracking['analytics_account']}&cid=[**RID**]&aip=1&t=event&ec=email&ea=open&dp=%2Femail%2F{tracking['campaign_name']}&dt=Email"


delete_email_count = 0
stop_delete = False
group_a = pd.DataFrame()
group_b = pd.DataFrame()
target = pd.DataFrame()
db_path = "database/group.db"

if __name__ == "__main__":
    # do this at beginning of your application
    myapp = SingleInstance()

    # check is another instance of same program running
    if myapp.already_running():
        alert(text="Another instance of this program is already running")
        print("Another instance of this program is already running")
        sys.exit(1)

    is_testing_environment = 0
    try:
        if os.getenv('fa414ce5-05d1-45e2-ba53-df760ad35fa0'):
            is_testing_environment = int(os.getenv('fa414ce5-05d1-45e2-ba53-df760ad35fa0'))
    except:
        pass

    if is_testing_environment:
        import main
    else:
        import dialog



# pyinstaller --onedir --icon=icons/icon.ico --name=GMonster --noconsole --noconfirm var.py
# pyi-makespec --onefile --icon=icons/icon.ico --name=GMonster --noconsole var.py
# pyinstaller --onefile --icon=icons/icon.ico --name=GMonster --noconsole --add-data="icons/icon.ico;imag" --add-data="icons/mail.ico;imag" --add-data="icons/email.ico;imag" var.py
# pyinstaller --onefile --icon=icons/icon.ico --name=GMonster --upx-dir=E:\Upwork\2020\upx-3.96-win64 GMonster.spec
# pyinstaller GMonster.spec
# a.datas += Tree('E:\\Upwork\\2020\\gmail_app\\gmail_app\\icons', prefix='icons\\')
