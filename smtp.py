import os
import pandas as pd
from followup_smtp import FollowUpSend
from proxy_smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from email.mime.text import MIMEText
from email.utils import formatdate
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import socks
import threading
import time
import utils
import smtplib
import csv
import random
import json
import uuid
from pyairtable import Table
from pyairtable.formulas import match
from pyautogui import alert, password, confirm
from datetime import datetime, timedelta
from imap import ImapCheckForBlocks, ImapFollowUpCheck
from webhook import SendWebhook, CampaignReportWebhook
from main import GUI
from database import Database as DB
from database import db_to_pandas
from collections import defaultdict
from bs4 import BeautifulSoup
import traceback
import queue
import var
from var import logger

# defaultdict accept a function. Whatever that
# functions return is default value for non-existent keys
success_sent = defaultdict(lambda: False)
logger = logger
email_failed = 0
sent_q = queue.Queue()


def contains_non_ascii_characters(str):
    return not all(ord(c) < 128 for c in str)


def html_to_text(body):
    soup = BeautifulSoup(body, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return str(text)


def test(send_to):
    try:
        if GUI.radioButton_campaign_group_a.isChecked():
            send = var.group_a.iloc[0].to_dict()
        else:
            send = var.group_b.iloc[0].to_dict()

        target = var.target.iloc[0].to_dict()
        compose_email_subject = GUI.lineEdit_subject.text().strip()
        compose_email_body = GUI.textBrowser_compose.toPlainText().strip()
        msg = MIMEMultipart("alternative")
        if send["PROXY:PORT"] != " ":
            proxy_host = send["PROXY:PORT"].split(':')[0]
            proxy_port = int(send["PROXY:PORT"].split(':')[1])
        else:
            proxy_host = ""
            proxy_port = ""
        if proxy_host != "":
            server = SMTP(timeout=30)
            server.connect_proxy(host=var.smtp_server, port=var.smtp_port,
                                 proxy_host=proxy_host, proxy_port=proxy_port, proxy_type=socks.PROXY_TYPE_SOCKS5,
                                 proxy_user=send['PROXY_USER'], proxy_pass=send["PROXY_PASS"])
        else:
            server = smtplib.SMTP(var.smtp_server, var.smtp_port)
            server.set_debuglevel(0)

        server.starttls()
        server.ehlo()
        server.login(send['EMAIL'], send['EMAIL_PASS'])
        t_part = []
        for path in var.files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(Path(path).name))
            t_part.append(part)

        msg["Subject"] = utils.format_email(compose_email_subject, send['FIRSTFROMNAME'],
                                            send['LASTFROMNAME'], target['1'], target['2'], target['3'], target['4'],
                                            target['5'], target['6'], target['TONAME'])
        msg['From'] = formataddr((str(Header("{} {}".format(
            send['FIRSTFROMNAME'], send['LASTFROMNAME']), 'utf-8')), send['EMAIL']))
        msg["To"] = send_to
        msg['Date'] = formatdate(localtime=True)

        if var.body_type == "Html":
            body = utils.format_email(
                var.compose_email_body_html, send['FIRSTFROMNAME'], send['LASTFROMNAME'],
                target['1'], target['2'], target['3'], target['4'], target['5'], target['6'], target['TONAME'],
                source="body")
            msg.attach(MIMEText(body, "html"))
            msg.attach(MIMEText(html_to_text(body), "plain"))

        else:
            body = utils.format_email(
                var.compose_email_body, send['FIRSTFROMNAME'], send['LASTFROMNAME'],
                target['1'], target['2'], target['3'], target['4'], target['5'], target['6'], target['TONAME'])
            msg.attach(MIMEText(body, "plain"))

            html_body = "<html><body><p>" + \
                        body.replace("\n", "<br>") + "</p></body></html>"

            msg.attach(MIMEText(html_body, "html"))

        for part in t_part:
            msg.attach(part)

        server.sendmail(send['EMAIL'], send_to, msg.as_string())
        server.quit()
        server.close()
        print("done")
        return True

    except Exception as e:
        print("Error at test send : {}".format(e))
        logger.error("Error at test send - {} - {}".format(send['EMAIL'], e))
        return False


def forward(forward_to):
    try:
        msg = MIMEMultipart("alternative")
        if var.email_in_view['proxy_host'] != "":
            server = SMTP(timeout=30)
            server.connect_proxy(host=var.smtp_server, port=var.smtp_port,
                                 proxy_host=var.email_in_view['proxy_host'],
                                 proxy_port=int(var.email_in_view['proxy_port']), proxy_type=socks.PROXY_TYPE_SOCKS5,
                                 proxy_user=var.email_in_view['proxy_user'], proxy_pass=var.email_in_view["proxy_pass"])
        else:
            server = smtplib.SMTP(var.smtp_server, var.smtp_port)
            server.set_debuglevel(0)
            # server.set_debuglevel(1)

        server.starttls()
        server.ehlo()
        server.login(var.email_in_view['user'], var.email_in_view['pass'])
        print(var.email_in_view['from_mail'])
        msg["Subject"] = "Fwd: " + var.email_in_view['original_subject']
        msg['From'] = formataddr((str(Header("{} {}".format(
            var.email_in_view['FIRSTFROMNAME'], var.email_in_view['LASTFROMNAME']), 'utf-8')),
                                  var.email_in_view['user']))
        msg["To"] = forward_to
        msg['Date'] = formatdate(localtime=True)

        body = "---------- Forwarded message ---------\nFrom: {}\nDate: {}\nSubject: {}\nTo: <{}>\n\n{}". \
            format(var.email_in_view['from'], formatdate(localtime=True),
                   var.email_in_view['original_subject'], var.email_in_view['to_mail'],
                   var.email_in_view['original_body'])

        part1 = MIMEText(body, "plain")
        msg.attach(part1)

        html_body = "<html><body><p>" + \
                    body.replace("\n", "<br>") + "</p></body></html>"

        msg.attach(MIMEText(html_body, "html"))

        server.sendmail(var.email_in_view['user'], forward_to, msg.as_string())

        server.quit()
        server.close()
        print("done")
        return True

    except Exception as e:
        print("Error at forward : {}".format(e))
        logger.error(
            "Error at forward - {} - {}".format(var.email_in_view['user'], e))
        return False


def reply():
    try:
        msg = MIMEMultipart("alternative")
        if var.email_in_view['proxy_host'] != "":
            server = SMTP(timeout=30)
            server.connect_proxy(host=var.smtp_server, port=var.smtp_port,
                                 proxy_host=var.email_in_view['proxy_host'],
                                 proxy_port=int(var.email_in_view['proxy_port']), proxy_type=socks.PROXY_TYPE_SOCKS5,
                                 proxy_user=var.email_in_view['proxy_user'], proxy_pass=var.email_in_view["proxy_pass"])
        else:
            server = smtplib.SMTP(var.smtp_server, var.smtp_port)
            server.set_debuglevel(0)
            # server.set_debuglevel(1)

        server.starttls()
        server.ehlo()
        server.login(var.email_in_view['user'], var.email_in_view['pass'])

        msg_id = var.email_in_view['message-id']
        f_f_name = var.email_in_view['FIRSTFROMNAME']
        l_f_name = var.email_in_view['LASTFROMNAME']
        toname = var.email_in_view['from_name']
        msg["Subject"] = utils.format_email(
            var.email_in_view['subject'], f_f_name, l_f_name, "", "", "", "", "", "", toname)
        msg['From'] = formataddr((str(Header("{} {}".format(
            var.email_in_view['FIRSTFROMNAME'], var.email_in_view['LASTFROMNAME']), 'utf-8')),
                                  var.email_in_view['user']))
        msg["To"] = var.email_in_view['from_mail']
        msg['Date'] = formatdate(localtime=True)

        body = utils.format_email(
            var.email_in_view['body'], f_f_name, l_f_name, "", "", "", "", "", "", toname, source="body")

        if var.body_type == "Html":
            part1 = MIMEText(body, "html")
            msg.attach(MIMEText(html_to_text(body), "plain"))
        else:
            part1 = MIMEText(body, "plain")
            html_body = "<html><body><p>" + \
                        body.replace("\n", "<br>") + "</p></body></html>"

            msg.attach(MIMEText(html_body, "html"))

        msg.add_header("In-Reply-To", msg_id)
        msg.add_header("References", msg_id)
        msg.attach(part1)

        for path in var.files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(Path(path).name))
            msg.attach(part)

        server.sendmail(
            var.email_in_view['user'], var.email_in_view['from_mail'], msg.as_string())

        server.quit()
        server.close()
        print("done")
        return True

    except Exception as e:
        print("Error at reply : {}".format(e))
        logger.error(
            "Error at replying - {} - {}".format(var.email_in_view['user'], e))
        return False


class SMTP_(threading.Thread):
    followup_queue = queue.Queue()

    def __init__(self, threadID, name, proxy_host, proxy_port, proxy_user,
                 proxy_pass, user, passwd, FIRSTFROMNAME, LASTFROMNAME, target, d_start, d_end, campaign_id,
                 cached_targets,
                 followup_enabled):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.setDaemon(True)
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        self.user = user
        self.passwd = passwd
        self.FIRSTFROMNAME = FIRSTFROMNAME
        self.LASTFROMNAME = LASTFROMNAME
        self.target = target
        self.logger = logger

        logger.info("Length - {} {}".format(len(self.target), self.user))
        self.d_start = d_start
        self.d_end = d_end
        self.campaign_id = campaign_id
        self.local_hostname = None
        self.cached_targets = cached_targets
        self.followup_enabled = followup_enabled

    def login(self):
        try:

            if var.add_custom_hostname:
                self.local_hostname = f"{self.FIRSTFROMNAME}-pc"

            if self.proxy_host != "":
                server = SMTP(
                    timeout=30, local_hostname=self.local_hostname)
                server.connect_proxy(host=var.smtp_server, port=var.smtp_port,
                                     proxy_host=self.proxy_host, proxy_port=int(self.proxy_port),
                                     proxy_type=socks.PROXY_TYPE_SOCKS5,
                                     proxy_user=self.proxy_user, proxy_pass=self.proxy_pass)
                # server.set_debuglevel(1)
            else:
                server = smtplib.SMTP(var.smtp_server, var.smtp_port)
                server.set_debuglevel(0)

            server.starttls()
            server.ehlo()
            server.login(self.user, self.passwd)

            return server

        except Exception as e:
            print(
                f"Error at SMTP_.login {self.name} : {e.__class__.__name__} : {str(e)}")

            if var.enable_webhook_status:
                t_dict = {
                    "sender": self.user,
                    "sender_name": f"{self.FIRSTFROMNAME} {self.LASTFROMNAME}",
                    "time": datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S"),
                    "error_details": f"{e.__class__.__name__} : {str(e)}"
                }
                var.webhook_q.put(t_dict.copy())

            raise  # this is for re raising the exception

    def sleep(self):
        duration = random.randint(self.d_start, self.d_end)
        count = 0

        while not var.stop_send_campaign:
            time.sleep(1)
            count += 1
            if count >= duration:
                break

    def run(self):
        try:
            global sent_q, email_failed, success_sent, remove_target_q

            last_recipient = ''
            var.thread_open_campaign += 1

            t_part = []

            for path in var.files:
                part = MIMEBase('application', "octet-stream")
                with open(path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename="{}"'.format(Path(path).name))
                t_part.append(part)

            count = 0

            for index, item in self.target.iterrows():
                self.sleep()

                if var.stop_send_campaign:
                    break

                if not success_sent[item['EMAIL']]:
                    server = self.login()

                    msg = MIMEMultipart("alternative")

                    msg["Subject"] = utils.format_email(var.compose_email_subject, self.FIRSTFROMNAME,
                                                        self.LASTFROMNAME, item['1'], item['2'], item['3'],
                                                        item['4'], item['5'], item['6'], item['TONAME'])
                    msg['From'] = formataddr((str(Header("{} {}".format(
                        self.FIRSTFROMNAME, self.LASTFROMNAME), 'utf-8')), self.user))
                    msg["To"] = item['EMAIL']
                    last_recipient = item['EMAIL']
                    msg['Date'] = formatdate(localtime=True)

                    if var.body_type == "Html":
                        body = utils.format_email(var.compose_email_body_html, self.FIRSTFROMNAME, self.LASTFROMNAME,
                                                  item['1'], item['2'], item['3'], item['4'], item['5'], item['6'],
                                                  item['TONAME'], source="body")

                        # if contains_non_ascii_characters(body):
                        msg.attach(
                            MIMEText(body.encode('utf-8'), "html", 'utf-8'))
                        msg.attach(MIMEText(html_to_text(
                            body).encode('utf-8'), "plain", 'utf-8'))

                        # else:

                        # msg.attach(MIMEText(body, "html"))
                        # msg.attach(MIMEText(html_to_text(body), "plain"))

                    else:
                        body = utils.format_email(var.compose_email_body, self.FIRSTFROMNAME, self.LASTFROMNAME,
                                                  item['1'], item['2'], item['3'], item['4'], item['5'], item['6'],
                                                  item['TONAME'], source="body")

                        html_body = "<html><body><p>" + \
                                    body.replace("\n", "<br>") + "</p></body></html>"

                        # if contains_non_ascii_characters(body):
                        msg.attach(
                            MIMEText(body.encode('utf-8'), "plain", "utf-8"))
                        msg.attach(
                            MIMEText(html_body.encode('utf-8'), "html", "utf-8"))

                        # else:

                        # msg.attach(MIMEText(body, "plain"))
                        # msg.attach(MIMEText(html_body, "html"))

                    for part in t_part:
                        msg.attach(part)

                    if count == 1:
                        first_time = datetime.now()

                    if var.stop_send_campaign:
                        break

                    for counter in range(0, 3):
                        try:
                            server.sendmail(
                                self.user, item['EMAIL'], msg.as_string())
                            break
                        except:
                            if counter == 2:
                                raise
                            time.sleep(random.randint(10, 100))
                            print("Reconnecting smtp - {}".format(self.name))
                            try:
                                server = self.login()
                            except:
                                pass
                            # server.sendmail(
                            #     self.user, item['EMAIL'], msg.as_string())

                    success_sent[item['EMAIL']] = True

                    self.cached_targets.targets_q.put(item['EMAIL'])

                    self.logger.info(f"Sent - {self.user} {item['EMAIL']}")

                    sent_q.put((item['EMAIL'], index))
                    var.send_campaign_email_count += 1
                    count += 1

                    t_dict = {
                        "TARGET": item['EMAIL'],
                        "FROMEMAIL": self.user,
                        "STATUS": "sent",
                        "CAMPAIGN": self.campaign_id,
                        "DATE": str(datetime.today().date())
                    }
                    var.send_report.put(t_dict.copy())

                    if self.followup_enabled:
                        target_info = item.to_dict()
                        target_info['target_email'] = target_info.pop('EMAIL')
                        target_info['email_subject'] = msg["Subject"]
                        SMTP_.followup_queue.put({
                            "group_email": self.user,
                            "group_info": {
                                "proxy_host": self.proxy_host,
                                "proxy_port": self.proxy_port,
                                "proxy_user": self.proxy_user,
                                "proxy_pass": self.proxy_pass,
                                "user": self.user,
                                "password": self.passwd,
                                "proxy_type": socks.PROXY_TYPE_SOCKS5,
                                "FIRSTFROMNAME": self.FIRSTFROMNAME,
                                "LASTFROMNAME": self.LASTFROMNAME
                            },
                            "target_email": item['EMAIL'],
                            "target_info": target_info,
                            "campaign_id": self.campaign_id
                        })

                    if var.enable_webhook_status:
                        t_dict = {
                            "target": item['EMAIL'],
                            "sender": self.user,
                            "sender_name": f"{self.FIRSTFROMNAME} {self.LASTFROMNAME}",
                            "time": datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S"),
                            "subject": msg["Subject"],
                            "body": body
                        }
                        var.webhook_q.put(t_dict.copy())

                    var.command_q.put("self.update_compose_progressbar()")

                    if var.remove_email_from_target:
                        # target = DB()
                        # result = target.remove(table="targets", id=item['ID'])
                        remove_target_q.put(item['ID'])

                    if var.AirtableConfig.mark_sent_airtable:
                        MarkTargetSentAirtable.airtable_target_q.put(item['EMAIL'])

                    if count % 5 == 0 and var.check_for_blocks:
                        last_time = datetime.now()
                        elapsed_time = utils.difference_between_time(
                            first_time, last_time)

                        imap_object = ImapCheckForBlocks(time_limit=elapsed_time, proxy_host=self.proxy_host,
                                                         proxy_port=self.proxy_port, proxy_type=socks.PROXY_TYPE_SOCKS5,
                                                         proxy_user=self.proxy_user, proxy_pass=self.proxy_pass,
                                                         user=self.user, password=self.passwd)

                        if imap_object.check_for_block_messages():
                            self.logger.error(
                                f"Found block messages : {self.name} {str(datetime.now())}")
                            break
                        else:
                            self.logger.error(f"Found no block messages : {self.name}")
                            # self.logger.error(
                            #     f"Found no block messages : {self.name} {str(datetime.now())}")

                        # this is where you might want to anything that you want every campaign threads to do

                    server.quit()

        except Exception as e:
            email_failed += 1

            self.logger.error(
                "Error at Sending - {} - {}".format(self.name, traceback.format_exc()))

            t_dict = {
                "TARGET": last_recipient,
                "FROMEMAIL": self.user,
                "STATUS": str(e),
                "CAMPAIGN": self.campaign_id,
                "DATE": str(datetime.today().date())
            }
            var.send_report.put(t_dict.copy())

        finally:
            server = None
            var.thread_open_campaign -= 1


class MarkTargetSentAirtable(threading.Thread):
    airtable_target_q = queue.Queue()

    def __init__(self):
        super().__init__()

        self.threadID = "MarkTargetAsSent01"
        self.name = "MarkTargetAsSent"
        self.setDaemon(True)

        self._close = False
        self.config = var.AirtableConfig
        self.table = Table(self.config.api_key, self.config.base_id, self.config.table_name)

    def run(self):
        logger.info(f"Starting {self.__class__.__name__}...")

        list_of_email = []
        while not self.close:
            try:
                if not MarkTargetSentAirtable.airtable_target_q.empty():
                    email = MarkTargetSentAirtable.airtable_target_q.get()
                    list_of_email.append(email)
                else:
                    if len(list_of_email) > 0:
                        if var.AirtableConfig.use_desktop_id:
                            formula = self.formulas_with_desktop_id(list_of_email)
                        else:
                            formula = self.formulas_normal(list_of_email)

                        list_of_email = []
                        try:
                            results = self.table.all(formula=formula)
                        except Exception as e:
                            logger.error(f"Error at {self.__class__.__name__} : " +
                                         f"formula - {formula} | {traceback.format_exc()}")

                            raise

                        update_dict_list = []
                        if len(results) > 0:
                            for item in results:
                                item['fields']['has_sent_email'] = 1
                                update_dict_list.append(item)

                            self.table.batch_update(update_dict_list)

            except Exception as e:
                logger.error(f"Error at {self.__class__.__name__} : {traceback.format_exc()}")

            time.sleep(1)

        logger.info(f"Completed {self.__class__.__name__}...")

    def formulas_with_desktop_id(self, list_of_email):
        logger.info(f"formulas_with_desktop_id {self.__class__.__name__}...")

        formula = "AND(OR(" + ",".join([f"{{EMAIL}}='{item}'" for item in list_of_email]) + \
                  f", {{desktop_app_id}}='{var.gmonster_desktop_id}', {{has_sent_email}}=0))"

        return formula

    def formulas_normal(self, list_of_email):
        logger.info(f"formulas_normal {self.__class__.__name__}...")

        formula = "AND(OR(" + ",".join([f"{{EMAIL}}='{item}'" for item in list_of_email]) + \
                  f", {{has_sent_email}}=0))"

        return formula

    @property
    def close(self) -> bool:
        return self._close

    @close.setter
    def close(self, value: bool):
        self._close = value


remove_target_q = queue.Queue()


class RemoveTarget(threading.Thread):
    def __init__(self):
        super().__init__()

        self.threadID = "RemoveTarget01"
        self.name = "RemoveTarget"
        self.setDaemon(True)

        self.close = False
        self.target = DB()

    def run(self):
        global remove_target_q

        while not self.close:
            try:
                if not remove_target_q.empty():
                    _id = remove_target_q.get()
                    result = self.target.remove(table="targets", id=_id)

            except Exception as e:
                logger.error(f"Error at remove_target_from_database : {traceback.format_exc()}")

            time.sleep(1)

        print("Remove target thread class terminating")

    def stop(self):
        self.close = True


class AddCachedTargets(threading.Thread):
    def __init__(self):
        super().__init__()

        self.threadID = "AddCachedTargets"
        self.name = "AddCachedTargets"
        self.setDaemon(True)

        self._close = False
        self.db = DB()
        self.targets_q = queue.Queue()

    def run(self) -> None:
        while not self._close:
            try:
                if not self.targets_q.empty():
                    email = self.targets_q.get()
                    self.db.add_to_cached_targets(email)

            except Exception as e:
                logger.error(f"Error at AddCachedTargets : {traceback.format_exc()}")

            time.sleep(1)

        print("AddCachedTargets thread class terminating")

    @property
    def close(self):
        return self._close

    @close.setter
    def close(self, value):
        self._close = value


class AddFollowUps:
    def __init__(self, followup_queue: queue.Queue, campaign_time: datetime):
        self.db: DB() = DB()
        self.followup_queue = followup_queue
        self.campaign_time = campaign_time

    def send(self) -> None:
        logger.info(f"{self.__class__.__name__} starting...")

        followups = []
        while not self.followup_queue.empty():
            followup = self.followup_queue.get()
            followup['campaign_time'] = self.campaign_time
            followups.append(followup.copy())

        result = self.db.add_follow_up(followups)

        if result:
            logger.info(f"{self.__class__.__name__} successful")
        else:
            logger.info(f"{self.__class__.__name__} unsuccessful")


def main(group, d_start, d_end, group_selected):
    global sent_q, email_failed, success_sent, remove_target_q
    try:
        success_sent.clear()

        var.command_q.put("self.compose_config_visibility(on=False)")
        var.command_q.put("self.update_compose_progressbar()")

        email_failed = 0
        sent_q = queue.Queue()
        target = var.target.copy()

        # it removes the rows that doesn't any email address
        target = target[target['EMAIL'] != ""]

        target.insert(9, 'flag', '')
        target['flag'] = 0

        group.insert(8, 'flag', '')
        group['flag'] = 0

        target_len = len(target)
        group_len = len(group)

        campaign_id = str(uuid.uuid4())

        logger.error(f"\n Starting Send Campaign : "
                     + f"\n Target Removal - {var.remove_email_from_target}"
                     + f"\n Group Selected: {group_selected}"
                     + f"\n Webhook Enabled: {var.enable_webhook_status}"
                     + f"\n Email Block Check: {var.check_for_blocks}"
                     + f"\n Emails Per Account: {var.num_emails_per_address}"
                     + f"\n Len of Group: {group_len}"
                     + f"\n Len of Targets: {target_len}"
                     + f"\n Delay: {d_start} - {d_end}"
                     + f"\n Campaign ID: {campaign_id}"
                     + f"\n Add Custom Hostname: {var.add_custom_hostname}")

        with var.send_report.mutex:
            var.send_report.queue.clear()

        with var.webhook_q.mutex:
            var.webhook_q.queue.clear()

        if var.enable_webhook_status:
            webhook = SendWebhook()
            webhook.start()

        remove_target_q = queue.Queue()

        if var.remove_email_from_target:
            remove_target = RemoveTarget()
            remove_target.start()

        MarkTargetSentAirtable.airtable_target_q = queue.Queue()

        if var.AirtableConfig.mark_sent_airtable:
            mark_target_sent_airtable = MarkTargetSentAirtable()
            mark_target_sent_airtable.start()

        add_cached_targets = AddCachedTargets()
        add_cached_targets.start()

        followup_enabled = var.followup_enabled
        campaign_time = datetime.utcnow()

        with SMTP_.followup_queue.mutex:
            SMTP_.followup_queue.queue.clear()

        while var.send_campaign_email_count < target_len and group['flag'].sum() < group_len:
            target = target[target['flag'] == 0]

            target = target.reset_index(drop=True)

            e_target_len = len(target)

            temp = 0
            end = 0

            if var.stop_send_campaign:
                break

            for index, item in group.loc[group['flag'] == 0].iterrows():
                try:

                    if var.stop_send_campaign or temp > e_target_len - 1:
                        break

                    proxy_user = item["PROXY_USER"]
                    proxy_pass = item["PROXY_PASS"]
                    user = item["EMAIL"]
                    passwd = item["EMAIL_PASS"]
                    name = item["EMAIL"]
                    FIRSTFROMNAME = item["FIRSTFROMNAME"]
                    LASTFROMNAME = item['LASTFROMNAME']

                    if item["PROXY:PORT"] != " ":
                        proxy_host = item["PROXY:PORT"].split(':')[0]
                        proxy_port = int(item["PROXY:PORT"].split(':')[1])
                    else:
                        proxy_host = ""
                        proxy_port = ""

                    start = temp
                    end = start + var.num_emails_per_address - 1
                    temp = end + 1

                    group.at[index, 'flag'] = 1

                    logger.error(f"\nStarting Thread : Name - {name}"
                                 f"\nTargets Count - {len(target.loc[start:end])}")
                    # + f"\nTargets - {json.dumps(target.loc[start:end].to_dict())}")

                    SMTP_(index, name, proxy_host, proxy_port, proxy_user,
                          proxy_pass, user, passwd, FIRSTFROMNAME, LASTFROMNAME,
                          target.loc[start:end].copy(), d_start, d_end, campaign_id, add_cached_targets,
                          followup_enabled).start()

                    while var.thread_open_campaign >= var.limit_of_thread and not var.stop_send_campaign:
                        time.sleep(1)
                except:
                    logger.error(f"Error at smtp thread opening {campaign_id} - {user} - {traceback.format_exc()}")

            while var.thread_open_campaign != 0 and not var.stop_send_campaign:
                time.sleep(1)

            while not sent_q.empty():
                temp = sent_q.get()
                email, index = temp[0], temp[1]
                target.at[index, 'flag'] = 1

        # while var.thread_open_campaign != 0 and var.stop_send_campaign == False:
        #     time.sleep(1)

        # wait for all thread to be closed
        while var.thread_open_campaign != 0:
            time.sleep(1)

        # wait for webhook queue to be emptied
        if var.enable_webhook_status:
            time.sleep(2)

            while not var.webhook_q.empty():
                time.sleep(1)

            webhook.quit()

        try:
            field_names = ['TARGET', 'FROMEMAIL', 'STATUS', 'CAMPAIGN', "DATE"]
            with open(var.base_dir + "/report.csv", 'a', newline='', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writeheader()
                while not var.send_report.empty():
                    temp_dict = var.send_report.get()
                    writer.writerow(temp_dict)
        except Exception as e:
            logger.error('Error while saving report - {}'.format(e))

        if var.remove_email_from_target:
            logger.info("removing email from target...")

            while not remove_target_q.empty():
                time.sleep(1)

            remove_target.stop()
            db_to_pandas(group_a=False, group_b=False, target=True)
            var.command_q.put("self.update_db_table()")

        if var.AirtableConfig.mark_sent_airtable:
            logger.info("Marking target as sent...")

            while not MarkTargetSentAirtable.airtable_target_q.empty():
                time.sleep(1)

            mark_target_sent_airtable.close = True

        while not add_cached_targets.targets_q.empty():
            time.sleep(1)

        add_cached_targets.close = True

        if followup_enabled and not var.stop_send_campaign:
            add_follow_ups = AddFollowUps(SMTP_.followup_queue, campaign_time)
            add_follow_ups.send()

            next_run_time = datetime.now() + timedelta(days=var.followup_days)
            var.scheduler.add_job(follow_up, 'date',
                                  args=(campaign_id,),
                                  next_run_time=next_run_time)
            logger.info(f"FollowUp scheduled: {next_run_time} {campaign_id}")

        var.email_failed = email_failed

        if var.enable_webhook_status:
            campaign_report_webhook = CampaignReportWebhook({
                                                                'total_emails_sent': var.send_campaign_email_count,
                                                                'accounts_failed': email_failed,
                                                                'targets_remaining': len(var.target),
                                                                'group': group_selected,
                                                                'registered_mail': var.login_email
                                                            }.copy())

            campaign_report_webhook.start()

        alert(text='Total Emails Sent : {}\nAccounts Failed : {}\nTargets Remaining : {}\ncheck app.log and report.csv'.
              format(var.send_campaign_email_count, email_failed, len(var.target)), title='Alert', button='OK')

    except Exception as e:
        logger.error(f"Error at smtp.main: {traceback.format_exc()}")

    finally:
        var.command_q.put("GUI.pushButton_send.setEnabled(True)")

        var.command_q.put("self.update_compose_progressbar()")
        var.command_q.put("GUI.progressBar_compose.setValue(0)")
        var.command_q.put("self.send_button_visibility(on=True)")
        var.command_q.put("self.compose_config_visibility(on=True)")
        var.send_campaign_run_status = False

        logger.info(f"Sending Finished {campaign_id}")


def follow_up(campaign_id: str):
    try:
        logger.info(f"Starting Followup process, Campaign ID - {campaign_id}")

        while var.send_campaign_run_status:
            time.sleep(var.waiting_period_for_followup)
            logger.info(f"Waiting to start Followup process because campaign is running"
                        f", Campaign ID - {campaign_id}")

        logger.info(f"Starting Followup process again, Campaign ID - {campaign_id}")

        var.command_q.put("GUI.progressBar_compose.setValue(0)")
        var.command_q.put("self.send_button_visibility(on=False)")
        var.command_q.put("self.compose_config_visibility(on=False)")
        var.command_q.put("GUI.label_compose_status.setText('Follow Up: 0/2')")

        ImapFollowUpCheck.followup_required = []
        ImapFollowUpCheck.thread_open = 0
        ImapFollowUpCheck.email_to_be_sent = 0
        FollowUpSend.thread_open = 0

        db: DB = DB()
        followups = db.get_all_followup(campaign_id)

        if len(followups) > 0:
            followups_df = pd.DataFrame(followups)

            followup_group_df = followups_df.groupby('group_email')

            ImapFollowUpCheck.total_follow_up_checks = len(followup_group_df)

            for group_name, df_group in followup_group_df:
                groups_dict = df_group.to_dict('records')[0]
                groups_dict.update(groups_dict['group_info'])
                groups_dict.pop('group_info')
                groups_dict['target_info'] = []

                for row_index, row in df_group.iterrows():
                    groups_dict['target_info'] = groups_dict['target_info'] + [row['target_info'].copy()]

                imap_followup_check_thread = ImapFollowUpCheck(**groups_dict)
                imap_followup_check_thread.start()

                time.sleep(5)
                while ImapFollowUpCheck.thread_open >= var.limit_of_thread:
                    time.sleep(1)

            while ImapFollowUpCheck.thread_open != 0:
                time.sleep(1)

            var.command_q.put("GUI.label_compose_status.setText('Follow Up: 1/2')")

            followup_required = ImapFollowUpCheck.followup_required
            FollowUpSend.email_to_be_sent = ImapFollowUpCheck.email_to_be_sent

            if len(followup_required) > 0:
                logger.info(f"follow_up, Campaign Id - {campaign_id}: "
                            f"{FollowUpSend.email_to_be_sent} email to be sent")

                for item in followup_required:
                    item: dict
                    item['smtp_server'] = var.smtp_server
                    item['smtp_port'] = var.smtp_port
                    item['delay_start'] = var.delay_start
                    item['delay_end'] = var.delay_end
                    item['attachment_files'] = var.files
                    item['campaign_id'] = campaign_id

                    follow_up_send = FollowUpSend(**item)
                    follow_up_send.start()

                    time.sleep(5)
                    while FollowUpSend.thread_open >= var.limit_of_thread:
                        time.sleep(1)

                while FollowUpSend.thread_open != 0:
                    time.sleep(1)

                try:
                    field_names = ['TARGET', 'FROMEMAIL', 'STATUS', 'CAMPAIGN', "DATE"]
                    with open(os.path.join(os.getcwd(), var.base_dir, var.followup_report_file_path),
                              'a', newline='', encoding="utf-8") as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        while not FollowUpSend.send_report.empty():
                            report = FollowUpSend.send_report.get()
                            writer.writerow(report)

                        logger.info(f"Saving followup report, Campaign Id - {campaign_id}")

                except Exception as e:
                    logger.error(f'Error at follow_up, Campaign Id - {campaign_id} - {e}\n{traceback.format_exc()}')

            else:
                logger.info(f"No Followups required. Campaign Id - {campaign_id}")

        else:
            logger.info(f"No Followups entry found. Campaign Id - {campaign_id}")

        var.command_q.put("GUI.label_compose_status.setText('Follow Up: 2/2 Done')")

    except Exception as e:
        logger.error(f"Error at follow_up, Campaign Id - {campaign_id}:"
                     f" {e}\n{traceback.format_exc()}")

    finally:
        var.command_q.put("self.send_button_visibility(on=True)")
        var.command_q.put("self.compose_config_visibility(on=True)")
        logger.info(f"Finishing Followup process, Campaign Id - {campaign_id}")
