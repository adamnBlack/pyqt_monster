from proxy_smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import socks
import threading
import var
import time
import utils
import smtplib
import csv
import queue
import random
from pyautogui import alert, password, confirm
from datetime import datetime
from imap import ImapCheckForBlocks
from webhook import SendWebhook
from main import GUI

email_failed = 0

logger = var.logging
logger.getLogger("requests").setLevel(var.logging.WARNING)

sent_q = queue.Queue()


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

        server.ehlo()
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
                                            send['LASTFROMNAME'], target['1'], target['2'], target['3'], target['TONAME'])
        msg['From'] = formataddr((str(Header("{} {}".format(
            send['FIRSTFROMNAME'], send['LASTFROMNAME']), 'utf-8')), send['EMAIL']))
        msg["To"] = send_to
        msg['Date'] = formatdate(localtime=True)

        if var.body_type == "Html":
            body = utils.format_email(
                var.compose_email_body_html, send['FIRSTFROMNAME'], send['LASTFROMNAME'], target['1'], target['2'], target['3'], target['TONAME'], source="body")
            msg.attach(MIMEText(body, "html"))
        else:
            body = utils.format_email(
                var.compose_email_body, send['FIRSTFROMNAME'], send['LASTFROMNAME'], target['1'], target['2'], target['3'], target['TONAME'])
            msg.attach(MIMEText(body, "plain"))

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
                                 proxy_host=var.email_in_view['proxy_host'], proxy_port=int(var.email_in_view['proxy_port']), proxy_type=socks.PROXY_TYPE_SOCKS5,
                                 proxy_user=var.email_in_view['proxy_user'], proxy_pass=var.email_in_view["proxy_pass"])
        else:
            server = smtplib.SMTP(var.smtp_server, var.smtp_port)
            server.set_debuglevel(0)
            # server.set_debuglevel(1)

        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(var.email_in_view['user'], var.email_in_view['pass'])
        print(var.email_in_view['from_mail'])
        msg["Subject"] = "Fwd: " + var.email_in_view['original_subject']
        msg['From'] = formataddr((str(Header("{} {}".format(
            var.email_in_view['FIRSTFROMNAME'], var.email_in_view['LASTFROMNAME']), 'utf-8')), var.email_in_view['user']))
        msg["To"] = forward_to
        msg['Date'] = formatdate(localtime=True)

        body = "---------- Forwarded message ---------\nFrom: {}\nDate: {}\nSubject: {}\nTo: <{}>\n\n{}".\
            format(var.email_in_view['from'], formatdate(localtime=True),
                   var.email_in_view['original_subject'], var.email_in_view['to_mail'],
                   var.email_in_view['original_body'])

        part1 = MIMEText(body, "plain")
        msg.attach(part1)

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
                                 proxy_host=var.email_in_view['proxy_host'], proxy_port=int(var.email_in_view['proxy_port']), proxy_type=socks.PROXY_TYPE_SOCKS5,
                                 proxy_user=var.email_in_view['proxy_user'], proxy_pass=var.email_in_view["proxy_pass"])
        else:
            server = smtplib.SMTP(var.smtp_server, var.smtp_port)
            server.set_debuglevel(0)
            # server.set_debuglevel(1)

        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(var.email_in_view['user'], var.email_in_view['pass'])

        msg_id = var.email_in_view['message-id']
        f_f_name = var.email_in_view['FIRSTFROMNAME']
        l_f_name = var.email_in_view['LASTFROMNAME']
        toname = var.email_in_view['from_name']
        msg["Subject"] = utils.format_email(
            var.email_in_view['subject'], f_f_name, l_f_name, "", "", "", toname)
        msg['From'] = formataddr((str(Header("{} {}".format(
            var.email_in_view['FIRSTFROMNAME'], var.email_in_view['LASTFROMNAME']), 'utf-8')), var.email_in_view['user']))
        msg["To"] = var.email_in_view['from_mail']
        msg['Date'] = formatdate(localtime=True)

        body = utils.format_email(
            var.email_in_view['body'], f_f_name, l_f_name, "", "", "", toname, source="body")

        if var.body_type == "Html":
            part1 = MIMEText(body, "html")
        else:
            part1 = MIMEText(body, "plain")

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
    def __init__(self, threadID, name, proxy_host, proxy_port, proxy_user, proxy_pass, user, passwd, FIRSTFROMNAME, LASTFROMNAME, target, d_start, d_end):
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
        print("Length - {} {}".format(len(self.target), self.user))
        global logger
        self.logger = logger
        self.d_start = d_start
        self.d_end = d_end

    def login(self):
        if self.proxy_host != "":
            server = SMTP(timeout=30)
            server.connect_proxy(host=var.smtp_server, port=var.smtp_port,
                                 proxy_host=self.proxy_host, proxy_port=int(self.proxy_port), proxy_type=socks.PROXY_TYPE_SOCKS5,
                                 proxy_user=self.proxy_user, proxy_pass=self.proxy_pass)
            # server.set_debuglevel(1)
        else:
            server = smtplib.SMTP(var.smtp_server, var.smtp_port)
            server.set_debuglevel(0)

        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.user, self.passwd)

        return server

    def run(self):
        try:
            global sent_q, email_failed
            last_recipient = ''
            var.thread_open_campaign += 1

            server = self.login()
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
                if var.stop_send_campaign == True:
                    break

                count += 1

                msg = MIMEMultipart("alternative")
                msg["Subject"] = utils.format_email(
                    var.compose_email_subject, self.FIRSTFROMNAME, self.LASTFROMNAME, item['1'], item['2'], item['3'], item['TONAME'])
                msg['From'] = formataddr((str(Header("{} {}".format(
                    self.FIRSTFROMNAME, self.LASTFROMNAME), 'utf-8')), self.user))
                msg["To"] = item['EMAIL']
                last_recipient = item['EMAIL']
                msg['Date'] = formatdate(localtime=True)

                if var.body_type == "Html":
                    body = utils.format_email(var.compose_email_body_html, self.FIRSTFROMNAME,
                                              self.LASTFROMNAME, item['1'], item['2'], item['3'], item['TONAME'], source="body")
                    msg.attach(MIMEText(body, "html"))
                else:
                    body = utils.format_email(var.compose_email_body, self.FIRSTFROMNAME, self.LASTFROMNAME,
                                              item['1'], item['2'], item['3'], item['TONAME'], source="body")
                    msg.attach(MIMEText(body, "plain"))

                for part in t_part:
                    msg.attach(part)

                time.sleep(random.randint(self.d_start, self.d_end))

                if count == 1:
                    first_time = datetime.now()

                try:
                    server.sendmail(self.user, item['EMAIL'], msg.as_string())
                except:
                    print("Reconnecting smtp - {}".format(self.name))
                    server = self.login()
                    server.sendmail(self.user, item['EMAIL'], msg.as_string())

                if count % 5 == 0 and var.check_for_blocks == True:
                    last_time = datetime.now()
                    elapsed_time = utils.difference_between_time(
                        first_time, last_time)

                    imap_object = ImapCheckForBlocks(time_limit=elapsed_time, proxy_host=self.proxy_host,
                                                     proxy_port=self.proxy_port, proxy_type=socks.PROXY_TYPE_SOCKS5,
                                                     proxy_user=self.proxy_user, proxy_pass=self.proxy_pass,
                                                     imap_user=self.user, imap_pass=self.passwd)

                    if imap_object.check_for_block_messages():
                        print(f"Found block messages : {self.name}")
                        self.logger.error(
                            f"Found block messages : {self.name} {str(datetime.now())}")
                        break
                    else:
                        print(f"Found no block messages : {self.name}")
                        self.logger.error(
                            f"Found no block messages : {self.name} {str(datetime.now())}")

                t_dict = {
                    "TARGET": item['EMAIL'],
                    "FROMEMAIL": self.user,
                    "STATUS": "sent"
                }
                var.send_report.put(t_dict.copy())

                if var.enable_webhook_status:
                    t_dict = {
                        "target": item['EMAIL'],
                        "sender": self.user,
                        "time": datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S"),
                        "subject": msg["Subject"],
                        "body": body
                    }
                    var.webhook_q.put(t_dict.copy())

                sent_q.put((item['EMAIL'], index))
                var.send_campaign_email_count += 1

            server.quit()
            server.close()
        except Exception as e:
            email_failed += 1
            print("error at SMTP - {} - {}".format(self.name, e))
            self.logger.error(
                "Error at Sending - {} - {}".format(self.name, e))
            t_dict = {
                "TARGET": last_recipient,
                "FROMEMAIL": self.user,
                "STATUS": str(e)
            }
            var.send_report.put(t_dict.copy())
        finally:
            server = None
            var.thread_open_campaign -= 1


def main(group, d_start, d_end):
    global sent_q, email_failed, logger

    var.rid_list = []

    email_failed = 0
    sent_q = queue.Queue()
    target = var.target.copy()
    target = target[target['EMAIL'] != ""]

    target.insert(6, 'flag', '')
    target['flag'] = 0

    group.insert(8, 'flag', '')
    group['flag'] = 0

    target_len = len(target)
    group_len = len(group)
    # var.send_report = queue.Queue()
    # var.webhook_q = queue.Queue()

    with var.send_report.mutex:
        var.send_report.queue.clear()

    with var.webhook_q.mutex:
        var.webhook_q.queue.clear()

    if var.enable_webhook_status:
        webhook = SendWebhook()
        webhook.start()

    while var.send_campaign_email_count < target_len and group['flag'].sum() < group_len:
        target = target[target['flag'] == 0]

        target = target.reset_index(drop=True)

        e_target_len = len(target)
        temp = 0
        end = 0

        for index, item in group.loc[group['flag'] == 0].iterrows():
            try:

                if var.stop_send_campaign == True or end >= e_target_len-1:
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

                print(index, name, target.loc[start:end].copy(), start, end, len(
                    target.loc[start:end]), d_start, d_end)

                SMTP_(index, name, proxy_host, proxy_port, proxy_user,
                      proxy_pass, user, passwd, FIRSTFROMNAME, LASTFROMNAME, target.loc[start:end].copy(),  d_start, d_end).start()

                while var.thread_open_campaign >= var.limit_of_thread and var.stop_send_campaign == False:
                    time.sleep(1)
            except Exception as e:
                print("Error at smtp thread opening - {} - {}".format(user, e))
                logger.error(
                    "Error at smtp thread opening - {} - {}".format(user, e))

        while var.thread_open_campaign != 0 and var.stop_send_campaign == False:
            time.sleep(1)

        while not sent_q.empty():
            temp = sent_q.get()
            email, index = temp[0], temp[1]
            target.at[index, 'flag'] = 1

    while var.thread_open_campaign != 0 and var.stop_send_campaign == False:
        time.sleep(1)

    # wait for webhook queue to be emptied
    if var.enable_webhook_status:
        time.sleep(2)

        while not var.webhook_q.empty():
            time.sleep(1)

        webhook.quit()

    try:
        field_names = ['TARGET', 'FROMEMAIL', 'STATUS']
        with open(var.base_dir+"/report.csv", 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            while not var.send_report.empty():
                writer.writerow(var.send_report.get())
    except Exception as e:
        print('Error while saving report - {}'.format(e))

    var.email_failed = email_failed
    var.send_campaign_run_status = False

    print("sending finished")
    # alert(text='Total Emails Sent : {}\nAccounts Failed : {}\ncheck app.log and report.csv'.\
    #             format(var.send_campaign_email_count, email_failed), title='Alert', button='OK')
