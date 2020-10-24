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

logger=var.logging.getLogger()
logger.setLevel(var.logging.DEBUG)
sent_q = queue.Queue()

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
        msg["Subject"] = var.email_in_view['subject']
        msg['From'] = formataddr((str(Header("{} {}".format(var.email_in_view['FIRSTFROMNAME'], var.email_in_view['LASTFROMNAME']) , 'utf-8')), var.email_in_view['user']))
        msg["To"] = var.email_in_view['from_mail']
        msg['Date'] = formatdate(localtime=True)
        body =  var.email_in_view['body']
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

        server.sendmail(var.email_in_view['user'], var.email_in_view['from_mail'], msg.as_string())

        server.quit()
        server.close()
        print("done")
        return True

    except Exception as e:
        print("Error at reply : {}".format(e))
        logger.error("Error at replying - {} - {}".format(var.email_in_view['user'], e))
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
        global logger
        self.logger=logger
        self.d_start = d_start
        self.d_end = d_end

    def run(self):
        try:
            global sent_q
            last_recipient = ''
            var.thread_open_campaign += 1
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

            t_part = []
            for path in var.files:
                part = MIMEBase('application', "octet-stream")
                with open(path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename="{}"'.format(Path(path).name))
                t_part.append(part)
            print("Length - {}".format(len(self.target)))
            for index, item in self.target.iterrows():
                if var.stop_send_campaign == True:
                    break
                msg = MIMEMultipart("alternative")
                msg["Subject"] = utils.format_email(var.compose_email_subject, self.FIRSTFROMNAME, self.LASTFROMNAME, item['1'], item['2'], item['3'], item['TONAME'])
                msg['From'] = formataddr((str(Header("{} {}".format(self.FIRSTFROMNAME, self.LASTFROMNAME), 'utf-8')), self.user))
                msg["To"] = item['EMAIL']
                last_recipient = item['EMAIL']
                msg['Date'] = formatdate(localtime=True)
                body =  utils.format_email(var.compose_email_body, self.FIRSTFROMNAME, self.LASTFROMNAME, item['1'], item['2'], item['3'], item['TONAME'])
                msg.attach(MIMEText(body, "plain"))
                for part in t_part:
                    msg.attach(part)
                server.sendmail(self.user, item['EMAIL'], msg.as_string())
                t_dict = {
                    "TARGET": item['EMAIL'],
                    "FROMEMAIL": self.user,
                    "STATUS": "sent"
                }
                var.send_report.put(t_dict.copy())
                sent_q.put(item['EMAIL'])
                var.send_campaign_email_count+=1
                time.sleep(random.randint(self.d_start, self.d_end))
            server.quit()
            server.close()
        except Exception as e:
            print("error at SMTP - {} - {}".format(self.name, e))
            self.logger.error("Error at Sending - {} - {}".format(self.name, e))
            t_dict = {
                    "TARGET": last_recipient,
                    "FROMEMAIL": self.user,
                    "STATUS": str(e)
                }
            var.send_report.put(t_dict.copy())
        finally:
            var.thread_open_campaign-=1

def main(group, d_start, d_end):
    global sent_q
    sent_q = queue.Queue()
    target_len = len(var.target)
    group_len = len(group)
    var.send_campaign_run_status = True
    var.send_report = queue.Queue()

    while var.send_campaign_email_count < target_len and group['flag'].sum() < group_len:
        var.target = var.target.sort_values(by=['flag'], ascending=False)
        temp = var.target.flag.ne('0').idxmax()
        end = 0
        print(temp)
        for index, item in group.loc[group['flag'] == 0].iterrows():
            if var.stop_send_campaign == True or end >= target_len-1:
                break
            if item["PROXY:PORT"] != " ":
                proxy_host = item["PROXY:PORT"].split(':')[0]
                proxy_port = int(item["PROXY:PORT"].split(':')[1])
            else:
                proxy_host = ""
                proxy_port = ""
            proxy_user = item["PROXY_USER"]
            proxy_pass = item["PROXY_PASS"]
            user = item["EMAIL"]
            passwd = item["EMAIL_PASS"]
            name = item["EMAIL"]
            FIRSTFROMNAME = item["FIRSTFROMNAME"]
            LASTFROMNAME = item['LASTFROMNAME']
            start = temp
            end = start + var.num_emails_per_address - 1
            temp = end + 1
            while var.thread_open_campaign >= var.limit_of_thread and var.stop_send_campaign == False:
                time.sleep(1)
            group.loc[index, ['flag']] = 1
            print(index, name, proxy_host, proxy_port, proxy_user, proxy_pass, user, passwd, FIRSTFROMNAME, LASTFROMNAME, start, end, d_start, d_end)
            SMTP_(index, name, proxy_host, proxy_port, proxy_user, proxy_pass, user, passwd, FIRSTFROMNAME, LASTFROMNAME, var.target.loc[start:end],  d_start, d_end).start()

        while var.thread_open_campaign!=0 and var.stop_send_campaign == False:
            time.sleep(1)

        while not sent_q.empty():
            email = sent_q.get()
            var.target.loc[var.target['EMAIL'] == email]['flag'] = 1
        # print(var.group_a.head(5))
        # print(group.head(5))


    var.send_campaign_run_status = False

    print("sending finished")
    try:
        field_names = ['TARGET','FROMEMAIL','STATUS']
        with open(var.base_dir+"/report.csv", 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = field_names)
            writer.writeheader()
            while not var.send_report.empty():
                writer.writerow(var.send_report.get())
    except Exception as e:
        print('Error while saving report - {}'.format(e))
