import queue
import traceback
import proxy_imaplib
import socks
import email
import threading
from datetime import datetime, timedelta, timezone
import time
import var
import imaplib
import codecs
from utils import difference_between_time
import webhook
from database import Database as DB
from var import logger


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def slashescape(err):
    """ codecs error handler. err is UnicodeDecode instance. return
    a tuple with a replacement for the unencodable part of the input
    and a position where encoding should continue"""
    # print err, dir(err), err.start, err.end, err.object[:err.start]
    thebyte = err.object[err.start:err.end]
    repl = u'\\x' + hex(ord(thebyte))[2:]
    return (repl, err.end)


codecs.register_error('slashescape', slashescape)


def check_if_blacklisted(input_string: str):
    for keyword in var.inbox_blacklist:
        if keyword in input_string:
            return True

    return False


def set_read_flag(index):
    try:
        global logger
        data = var.inbox_data
        proxy_user = data['proxy_user'][index]
        proxy_pass = data['proxy_pass'][index]
        imap_user = data['user'][index]
        imap_pass = data['pass'][index]
        uid = data['uid'][index]

        if data['proxy_host'][index] != "":
            proxy_host = data['proxy_host'][index]
            proxy_port = int(data['proxy_port'][index])
            print(index, data['uid'][index], proxy_host, proxy_port,
                  proxy_user, proxy_pass, imap_user, imap_pass)
            imap = proxy_imaplib.IMAP(proxy_host=proxy_host, proxy_port=proxy_port, proxy_type=socks.PROXY_TYPE_SOCKS5,
                                      proxy_user=proxy_user, proxy_pass=proxy_pass, host=var.imap_server,
                                      port=var.imap_port, timeout=30)
        else:
            imap = imaplib.IMAP4_SSL(var.imap_server)

        imap.login(imap_user, imap_pass)

        imap.select("Inbox")

        imap.uid('STORE', uid, '+FLAGS', '\Seen')
        imap.close()
        imap.logout()
        print("Set read flag")
    except Exception as e:
        logger.error("Error at set_read_flag - {} - {}".format(imap_user, e))


def delete_email(group):
    try:
        var.thread_open += 1
        print("group name ", group.iloc[0]['user'])
        print(len(var.inbox_data))

        proxy_user = group.iloc[0]['proxy_user']
        proxy_pass = group.iloc[0]['proxy_pass']
        imap_user = group.iloc[0]['user']
        imap_pass = group.iloc[0]['pass']

        if group.iloc[0]['proxy_host'] != "":
            proxy_host = group.iloc[0]['proxy_host']
            proxy_port = int(group.iloc[0]['proxy_port'])
            print(proxy_host, proxy_port, proxy_user,
                  proxy_pass, imap_user, imap_pass)
            imap = proxy_imaplib.IMAP(proxy_host=proxy_host, proxy_port=proxy_port, proxy_type=socks.PROXY_TYPE_SOCKS5,
                                      proxy_user=proxy_user, proxy_pass=proxy_pass, host=var.imap_server,
                                      port=var.imap_port, timeout=30)
        else:
            imap = imaplib.IMAP4_SSL(var.imap_server)

        imap.login(imap_user, imap_pass)

        imap.select("Inbox")

        for row_index, row in group.iterrows():
            if var.stop_delete:
                break
            imap.uid('STORE', row['uid'], '+X-GM-LABELS', '\\Trash')
            var.delete_email_count += 1
            var.inbox_data.drop(row_index, inplace=True)
        print(len(var.inbox_data))
        imap.close()
        imap.logout()
        print("Deleted email")
    except Exception as e:
        print("Error at deleting email : {}".format(e))
        logger.error("Error at deleting email - {} - {}".format(imap_user, e))

    finally:
        var.thread_open -= 1


class ImapBase:
    def __init__(self, **kwargs):
        super().__init__()
        self.proxy_host = kwargs["proxy_host"]
        self.proxy_port = kwargs["proxy_port"]
        self.proxy_type = kwargs["proxy_type"]
        self.proxy_user = kwargs["proxy_user"]
        self.proxy_pass = kwargs["proxy_pass"]
        self.imap_host = var.imap_server
        self.imap_port = var.imap_port
        self.imap_user = kwargs["user"]
        self.imap_pass = kwargs["password"]

        self.logger = logger

    def login(self):
        if self.proxy_host != "":
            imap = proxy_imaplib.IMAP(proxy_host=self.proxy_host, proxy_port=self.proxy_port,
                                      proxy_type=self.proxy_type,
                                      proxy_user=self.proxy_user, proxy_pass=self.proxy_pass, host=self.imap_host,
                                      port=self.imap_port, timeout=30)
        else:
            imap = imaplib.IMAP4_SSL(var.imap_server)

        imap.login(self.imap_user, self.imap_pass)

        return imap


class ImapCheckForBlocks(ImapBase):
    def __init__(self, **kwargs):
        self.time_limit = kwargs["time_limit"]
        super().__init__(**kwargs)

    def check_for_block_messages(self):
        try:
            # FROM - Mail Delivery Subsystem mailer-daemon@googlemail.com
            # SUBJECT - Delivery Status Notification (Failure)
            # Message bloqué   or  Message blocked

            imap = self.login()
            imap.select("Inbox", readonly=True)

            date = datetime.today() - timedelta(days=1)

            tmp, data = imap.search(
                None,
                f'(SINCE "{date.strftime("%d-%b-%Y")}" SUBJECT "Delivery Status Notification (Failure)" FROM "mailer-daemon@googlemail.com")')
            for num in data[0].split():
                tmp, data = imap.fetch(num, '(UID RFC822)')
                raw = data[0][0]
                raw_str = raw.decode("utf-8")
                uid = raw_str.split()[2]
                email_message = email.message_from_string(
                    data[0][1].decode('utf-8', 'slashescape'))

                date = email.utils.parsedate_to_datetime(email_message['Date'])
                difference_in_minute = difference_between_time(
                    date, datetime.now(timezone.utc))

                if difference_in_minute < self.time_limit:
                    b = email_message
                    body = ""

                    if b.is_multipart():
                        for part in b.walk():
                            ctype = part.get_content_type()
                            cdispo = str(part.get('Content-Disposition'))

                            # skip any text/plain (txt) attachments
                            if ctype == 'text/plain' and 'attachment' not in cdispo:
                                body = part.get_payload(decode=True)  # decode
                                break
                    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
                    else:
                        body = b.get_payload(decode=True)

                    try:
                        body = body.decode("utf-8", 'slashescape')
                    except:
                        body = body

                    blocked_message_keyword = [
                        "Message bloqué", "Message blocked", "Message rejected"]

                    for item in blocked_message_keyword:
                        if item.lower() in body.lower():
                            return True

            return False

        except Exception as e:
            print(
                "error at Imap_base.check_for_block_messages - {} - {}".format(self.imap_user, e))
            self.logger.error(
                "Error at Imap_base.check_for_block_messages - {} - {}".format(self.imap_user, e))
            return False


class ImapFollowUpCheck(ImapBase, threading.Thread):
    followup_required = list()
    thread_open = int()
    email_to_be_sent = int()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setDaemon(True)

        self.campaign_time: datetime = kwargs['campaign_time']
        self.target_info = kwargs['target_info']
        self.kwargs = kwargs

    def run(self):
        try:
            logger.info(f"Starting ImapFollowUpCheck: {self.imap_user}")

            ImapFollowUpCheck.thread_open += 1

            imap = self.login()
            imap.select("Inbox", readonly=True)

            date = self.campaign_time - timedelta(days=1)

            target_that_replied = []

            for item in self.target_info:
                logger.info(f"Looking for ImapFollowUpCheck: {item['target_email']}")

                tmp, data = imap.search(
                    None,
                    f'(SINCE "{date.strftime("%d-%b-%Y")}"'
                    f' FROM "{item["target_email"]}")')

                if not len(data[0].split()) > 0:
                    target_that_replied.append(item)
                    ImapFollowUpCheck.email_to_be_sent += 1

            if len(target_that_replied) > 0:
                self.kwargs['target_info'] = target_that_replied
                ImapFollowUpCheck.followup_required.append(self.kwargs)
                logger.info(f"ImapFollowUpCheck: {self.imap_user} "
                            f"Added to FollowUp list ")
            else:
                logger.info(f"ImapFollowUpCheck: {self.imap_user} "
                            f"MSG: No Followup needed ")

            logger.info(f"Finishing ImapFollowUpCheck: {self.imap_user}")

        except Exception as e:
            logger.error(f"Error at ImapFollowUpCheck: {e}\n{traceback.format_exc()}")

        finally:
            ImapFollowUpCheck.thread_open -= 1


class IMAP_(threading.Thread):
    def __init__(self, threadID, name, proxy_host, proxy_port, proxy_type, proxy_user, proxy_pass, imap_user, imap_pass,
                 FIRSTFROMNAME, LASTFROMNAME, targets, responses_webhook_enabled):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.setDaemon(True)
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_type = proxy_type
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        self.imap_host = var.imap_server
        self.imap_port = var.imap_port
        self.imap_user = imap_user
        self.imap_pass = imap_pass
        self.FIRSTFROMNAME = FIRSTFROMNAME
        self.LASTFROMNAME = LASTFROMNAME
        self.logger = logger
        self.targets = targets
        self.responses_webhook_enabled = responses_webhook_enabled

    def run(self):
        global email_failed, total_email_downloaded
        try:
            var.thread_open += 1
            if self.proxy_host != "":
                imap = proxy_imaplib.IMAP(proxy_host=self.proxy_host, proxy_port=self.proxy_port,
                                          proxy_type=self.proxy_type,
                                          proxy_user=self.proxy_user, proxy_pass=self.proxy_pass, host=self.imap_host,
                                          port=self.imap_port, timeout=30)
            else:
                imap = imaplib.IMAP4_SSL(var.imap_server)

            imap.login(self.imap_user, self.imap_pass)
            # print(self.folder, self.category)
            imap.select("Inbox", readonly=True)

            objDate = datetime.strptime(var.date, '%m/%d/%Y')
            offset_naive_date = objDate
            offset_aware_date = utc_to_local(offset_naive_date)

            for item in ['SEEN', 'UNSEEN']:
                # if self.category:
                #     tmp, data = imap.search(None,
                #             '({} SINCE "{}" X-GM-RAW "Category:{}")'.format(
                #                 item, objDate.strftime('%d-%b-%Y'), self.category))
                # else:
                #     tmp, data = imap.search(None, '({} SINCE "{}")'.format(item, objDate.strftime('%d-%b-%Y')))

                tmp, data = imap.search(None, '({} SINCE "{}")'.format(
                    item, objDate.strftime('%d-%b-%Y')))

                for num in data[0].split():
                    if var.stop_download:
                        break
                    tmp, data = imap.fetch(num, '(UID RFC822)')
                    raw = data[0][0]
                    raw_str = raw.decode("utf-8")
                    uid = raw_str.split()[2]
                    email_message = email.message_from_string(
                        data[0][1].decode('utf-8', 'slashescape'))
                    # print(email_message.items())
                    b = email_message
                    body = ""

                    if b.is_multipart():
                        for part in b.walk():
                            ctype = part.get_content_type()
                            cdispo = str(part.get('Content-Disposition'))

                            # skip any text/plain (txt) attachments
                            if (ctype == 'text/plain' or ctype == 'text/html') and 'attachment' not in cdispo:
                                body = part.get_payload(decode=True)  # decode
                                break
                    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
                    else:
                        body = b.get_payload(decode=True)

                    try:
                        body = body.decode("utf-8", 'ignore')
                    except:
                        # print(body)
                        body = body

                    subject = email.header.make_header(
                        email.header.decode_header(email_message['Subject']))

                    subject = str(subject)

                    from_name = str(email.header.make_header(email.header.decode_header(
                        email.utils.parseaddr(email_message['From'])[0]))
                    )
                    from_mail = str(email.header.make_header(email.header.decode_header(
                        email.utils.parseaddr(email_message['From'])[1]))
                    )

                    if not check_if_blacklisted(from_mail):
                        to_name = str(email.header.make_header(email.header.decode_header(
                            email.utils.parseaddr(email_message['To'])[0]))
                        )
                        to_mail = str(email.header.make_header(email.header.decode_header(
                            email.utils.parseaddr(email_message['To'])[1]))
                        )
                        mail_date = email.utils.parsedate_to_datetime(
                            email_message['Date'])

                        t_dict = {
                            'uid': uid,
                            'to': "{} {}".format(to_name, to_mail),
                            'TONAME': to_name,
                            'to_mail': to_mail,
                            'message-id': email.utils.parseaddr(email_message['Message-ID'])[1],
                            'from': "{} {}".format(from_name, from_mail),
                            'from_name': from_name,
                            'from_mail': from_mail,
                            'date': utc_to_local(mail_date),
                            'subject': subject,
                            'user': self.imap_user,
                            'pass': self.imap_pass,
                            'body': body,
                            'proxy_host': self.proxy_host,
                            'proxy_port': self.proxy_port,
                            'proxy_user': self.proxy_user,
                            'proxy_pass': self.proxy_pass,
                            'FIRSTFROMNAME': self.FIRSTFROMNAME,
                            'LASTFROMNAME': self.LASTFROMNAME,
                            'flag': item,
                            'Webhook_flag': False  # means not fired yet

                        }

                        # print(from_name, from_mail, to_name, to_mail, subject, body)
                        print("utc - ", utc_to_local(mail_date),
                              "| Non utc - ", mail_date)

                        try:
                            if mail_date.tzinfo:
                                print("Date is offset aware.")

                                if offset_aware_date <= mail_date:
                                    t_dict['date'] = utc_to_local(mail_date)
                                    var.email_q.put(t_dict.copy())
                                    var.total_email_downloaded += 1
                                else:
                                    print("From previous date.")
                            else:
                                print("Date is offset naive.")

                                if offset_naive_date <= mail_date:
                                    t_dict['date'] = utc_to_local(mail_date)
                                    var.email_q.put(t_dict.copy())
                                    var.total_email_downloaded += 1
                                else:
                                    print("From previous date offset naive.")

                        except Exception as e:
                            self.logger.error(
                                f"Error on Imap download {self.imap_user} : {e}")

                        if self.responses_webhook_enabled and t_dict['from_mail'] in self.targets:
                            t_dict["date"] = str(t_dict["date"])
                            webhook.inbox_q.put(t_dict.copy())

            imap.close()
            imap.logout()
        except Exception as e:
            var.email_failed += 1
            print("error at Imap - {} - {}".format(self.name, e))
            self.logger.error(
                "Error at downloading email - {} - {}".format(self.imap_user, e))
        finally:
            var.acc_finished += 1
            var.thread_open -= 1


def main(group):
    global logger
    var.email_failed = 0
    var.total_email_downloaded = 0
    responses_webhook_enabled = var.responses_webhook_enabled

    # folder = ""
    # sub_category = ""

    # if "Inbox" in category:
    #     folder, sub_category = category.split("->")[0], category.split("->")[-1]
    # else:
    #     folder = category

    # print(folder, sub_category)
    targets = set()

    if responses_webhook_enabled:
        webhook.inbox_q = queue.Queue()
        db = DB()
        targets = set(db.get_cached_targets() + var.target['EMAIL'].tolist())

        responses_webhook = webhook.SendWebhook_Inbox(0)
        responses_webhook.start()

    for index, item in group.iterrows():
        try:
            if var.stop_download:
                break

            proxy_type = socks.PROXY_TYPE_SOCKS5
            proxy_user = item["PROXY_USER"]
            proxy_pass = item["PROXY_PASS"]
            imap_user = item["EMAIL"]
            imap_pass = item["EMAIL_PASS"]
            name = item["EMAIL"]
            FIRSTFROMNAME = item["FIRSTFROMNAME"]
            LASTFROMNAME = item["LASTFROMNAME"]

            if item["PROXY:PORT"] != " ":
                proxy_host = item["PROXY:PORT"].split(':')[0]
                proxy_port = int(item["PROXY:PORT"].split(':')[1])
            else:
                proxy_host = ""
                proxy_port = ""

            while var.thread_open >= var.limit_of_thread and var.stop_download == False:
                time.sleep(1)

            print(index, name, proxy_host, proxy_port,
                  proxy_type, proxy_user, proxy_pass, imap_user,
                  imap_pass, FIRSTFROMNAME, LASTFROMNAME)

            IMAP_(index, name, proxy_host, proxy_port,
                  proxy_type, proxy_user, proxy_pass, imap_user,
                  imap_pass, FIRSTFROMNAME, LASTFROMNAME, targets, responses_webhook_enabled).start()

        except Exception as e:
            print("Error at Imap thread open - {} - {}".format(name, e))
            logger.error("Error at Imap thread open - {} - {}".format(name, e))

    while var.thread_open != 0 and not var.stop_download:
        time.sleep(1)

    if responses_webhook_enabled:
        while not webhook.inbox_q.empty():
            time.sleep(1)

        time.sleep(5)
        responses_webhook.quit()

    var.download_email_status = False
    # alert(text='Total Emails Downloaded : {}\nAccounts Failed : {}\ncheck app.log'.\
    #             format(var.total_email_downloaded, var.email_failed), title='Alert', button='OK')
    print("Downloading finished")
