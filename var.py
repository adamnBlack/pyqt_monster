import traceback
import uuid
from json import load, dumps
from pathlib import Path
import pandas as pd
import queue
from queue import LifoQueue
from win32event import CreateMutex
from win32api import CloseHandle, GetLastError
from winerror import ERROR_ALREADY_EXISTS
from pyautogui import alert
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

import var
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


gmonster_desktop_id = ''
version = '2.2r'
base_dir = "database"
followup_report_file_path = "followup_report.csv"
update_temp_path = "temp"
update_bat_file_path = os.path.join(os.getcwd(), base_dir, 'updater.bat')

try:
    with open(update_bat_file_path, "w") as file:
        file.write(
            r"""
@echo off

rem Wait for a period of time (e.g., 20 seconds)
timeout /t 20

rem Replace the original executable with the updated one
set "tempExePath=.\temp\GMonster.exe"  rem Replace with the actual path of the updated executable
set "originalExePath=.\GMonster.exe"  rem Replace with the actual path of the original executable
copy /y "%tempExePath%" "%originalExePath%"

rem Execute the updated version of the application
start "" "%originalExePath%"

set "tempExePath=.\temp\WUM.exe"  rem Replace with the actual path of the updated executable
set "originalExePath=.\WUM.exe"  rem Replace with the actual path of the original executable
copy /y "%tempExePath%" "%originalExePath%"
            
            """
        )
except:
    logger.error(f"Error at updater.bat file creating: {traceback.format_exc()}")


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
jobstores = {
    'default': SQLAlchemyJobStore(url=f'sqlite:///{base_dir}/jobs.sqlite')
}

logger.info("Logger Started")
scheduler = BackgroundScheduler(logger=logger)
# scheduler = BackgroundScheduler(logger=logger, jobstores=jobstores)
# scheduler.add_jobstore('sqlalchemy', url=f'sqlite:///{base_dir}/jobs.sqlite')
scheduler.start()


def exit_gracefully(signum, frame):
    global scheduler
    logger.info('shutdown scheduler gracefully')
    scheduler.shutdown()


db_file_loading_config = {
    "group_a": True,
    "group_b": True,
    "target": True
}


class AirtableConfig:
    base_id = ''
    api_key = ''
    table_name = ''
    use_desktop_id = False
    mark_sent_airtable = False
    continuous_loading = False
    continuous_loading_time_period = 24

    def __init__(self):
        pass


wum_exe_path = "WUM.exe"
CONFUSABLES_CHARACTER = [" ", " ", " ", " "]
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

airtable_base_id = 'appaCmKFn3MWDzjsF'
airtable_api_key = 'keyajjzgPaHo8VjWA'

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

# scheduler campaign
campaign_scheduler_cache_path = os.path.join(os.path.join(os.getcwd(), base_dir, "campaign_scheduler"))

try:
    if not os.path.exists(campaign_scheduler_cache_path):
        os.mkdir(campaign_scheduler_cache_path)
except Exception as e:
    logger.error(f"Error while creating campaign_scheduler folder - {e}")

responses_webhook_enabled = False
auto_fire_responses_webhook = False

# in hour
auto_fire_responses_webhook_interval = 1
# auto_fire_responses_webhook_interval = 6 * (2/360)
inbox_blacklist = []
inbox_whitelist = []
gmonster_desktop_id = ''
id_file_name = "gmonster_id"
id_file_path = os.path.join(os.getcwd(), base_dir, id_file_name)

hostname_list = []
inbox_whitelist_checkbox = False
space_encoding_checkbox = False

test_email = ''

try:
    if os.path.exists(id_file_path):
        with open(id_file_path, "r", encoding="utf-8") as file:
            gmonster_desktop_id = file.read().strip()
    else:
        gmonster_desktop_id = str(uuid.uuid4())

        with open(id_file_path, "w", encoding="utf-8") as file:
            file.write(gmonster_desktop_id)

except Exception as e:
    logger.info("Exception occurred at id file loading : {}".format(e))

config_file_path = '{}/gmonster_config.json'.format(base_dir)
try:
    with open(config_file_path) as json_file:
        data = load(json_file)
    config = data['config']

    # this is a section where you add new config variable

    if 'inbox_whitelist' not in config:
        config['inbox_whitelist'] = var.inbox_whitelist

    if 'inbox_whitelist_checkbox' not in config:
        config['inbox_whitelist_checkbox'] = inbox_whitelist_checkbox

    if 'space_encoding_checkbox' not in config:
        config['space_encoding_checkbox'] = space_encoding_checkbox

    if 'test_email' not in config:
        config['test_email'] = test_email

    # ends here

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
    inbox_whitelist = config['inbox_whitelist']
    responses_webhook_enabled = config['responses_webhook_enabled']
    auto_fire_responses_webhook = config["auto_fire_responses_webhook"]
    followup_enabled = config['followup_enabled']
    followup_days = config['followup_days']
    followup_subject = config['followup_subject']
    followup_body = config['followup_body']
    mail_server = config['mail_server']
    hostname_list = config['hostname_list']
    inbox_whitelist_checkbox = config['inbox_whitelist_checkbox']
    space_encoding_checkbox = config['space_encoding_checkbox']
    test_email = config['test_email']
    AirtableConfig.base_id = config['airtable']['base_id']
    AirtableConfig.api_key = config['airtable']['api_key']
    AirtableConfig.table_name = config['airtable']['table_name']
    AirtableConfig.use_desktop_id = config['airtable']['use_desktop_id']
    AirtableConfig.mark_sent_airtable = config['airtable']['mark_sent_airtable']
    AirtableConfig.continuous_loading = config['airtable']['continuous_loading']
    AirtableConfig.continuous_loading_time_period = config['airtable']['continuous_loading_time_period']
except Exception as e:
    logger.info("Exception occurred at config loading : {}".format(e))
    sys.exit()

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
        logger.info("Another instance of this program is already running")
        sys.exit(1)

    is_testing_environment = 0
    try:
        if os.getenv('fa414ce5-05d1-45e2-ba53-df760ad35fa0'):
            is_testing_environment = int(os.getenv('fa414ce5-05d1-45e2-ba53-df760ad35fa0'))
    except:
        pass

    logger.info("gmonster_desktop_id - {}".format(gmonster_desktop_id))

    from utils import update_config_json

    update_config_json()

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

# https://plainenglish.io/blog/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184