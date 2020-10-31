from pyautogui import alert, password, confirm
import proxy_imaplib
import socks
import email
import threading
from datetime import datetime
import time
import var
import imaplib

email_failed = 0
total_email_downloaded = 0
logger=var.logging.getLogger()
logger.setLevel(var.logging.DEBUG)

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
            print(index, data['uid'][index], proxy_host, proxy_port, proxy_user, proxy_pass, imap_user, imap_pass)
            imap = proxy_imaplib.IMAP(proxy_host=proxy_host, proxy_port=proxy_port, proxy_type=socks.PROXY_TYPE_SOCKS5,
                        proxy_user=proxy_user, proxy_pass=proxy_pass, host=var.imap_server, port=var.imap_port, timeout=30)
        else:
            imap = imaplib.IMAP4_SSL(var.imap_server)

        imap.login(imap_user, imap_pass)

        imap.select('Inbox')

        imap.uid('STORE', uid, '+FLAGS','\Seen')
        imap.close()
        imap.logout()
        print("Done")
    except Exception as e:
        print("Error at deleting email : {}".format(e))
        logger.error("Error at set_read_flag - {} - {}".format(imap_user, e))

def delete_email(group):
    try:
        var.thread_open += 1
        global logger
        print("group name ",group.iloc[0]['user'])

        proxy_user = group.iloc[0]['proxy_user']
        proxy_pass = group.iloc[0]['proxy_pass']
        imap_user = group.iloc[0]['user']
        imap_pass = group.iloc[0]['pass']


        if group.iloc[0]['proxy_host'] != "":
            proxy_host = group.iloc[0]['proxy_host']
            proxy_port = int(group.iloc[0]['proxy_port'])
            print(proxy_host, proxy_port, proxy_user, proxy_pass, imap_user, imap_pass)
            imap = proxy_imaplib.IMAP(proxy_host=proxy_host, proxy_port=proxy_port, proxy_type=socks.PROXY_TYPE_SOCKS5,
                        proxy_user=proxy_user, proxy_pass=proxy_pass, host=var.imap_server, port=var.imap_port, timeout=30)
        else:
            imap = imaplib.IMAP4_SSL(var.imap_server)

        imap.login(imap_user, imap_pass)

        imap.select('Inbox')

        for row_index, row in group.iterrows():
            if var.stop_delete == True:
                break
            imap.uid('STORE', row['uid'], '+X-GM-LABELS', '\\Trash')
            var.delete_email_count += 1
            var.inbox_data.drop(row_index)
        imap.close()
        imap.logout()
    except Exception as e:
        print("Error at deleting email : {}".format(e))
        logger.error("Error at deleting email - {} - {}".format(imap_user, e))
    finally:
        var.thread_open -= 1

class IMAP_(threading.Thread):
    def __init__(self, threadID, name, proxy_host, proxy_port, proxy_type, proxy_user, proxy_pass, imap_user, imap_pass, FIRSTFROMNAME, LASTFROMNAME):
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
        global logger
        self.logger = logger

    def run(self):
        global email_failed, total_email_downloaded
        try:
            var.thread_open+=1
            if self.proxy_host != "":
                imap = proxy_imaplib.IMAP(proxy_host=self.proxy_host, proxy_port=self.proxy_port, proxy_type=self.proxy_type,
                    proxy_user=self.proxy_user, proxy_pass=self.proxy_pass, host=self.imap_host, port=self.imap_port, timeout=30)
            else:
                imap = imaplib.IMAP4_SSL(var.imap_server)

            imap.login(self.imap_user, self.imap_pass)

            imap.select('Inbox', readonly=True)

            objDate = datetime.strptime(var.date, '%m/%d/%Y')

            for item in ['SEEN', 'UNSEEN']:

                tmp, data = imap.search(None, '({} SINCE "{}")'.format(item, objDate.strftime('%d-%b-%Y')))

                for num in data[0].split():
                    if var.stop_download == True:
                        break
                    tmp, data = imap.fetch(num, '(UID RFC822)')
                    raw = data[0][0]
                    raw_str = raw.decode("utf-8")
                    uid = raw_str.split()[2]
                    email_message = email.message_from_string(data[0][1].decode())
                    # print(email_message.items())
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
                    body = body.decode("utf-8")
                    t_dict = {
                        'uid': uid,
                        'to': email_message['To'],
                        'TONAME': email.utils.parseaddr(email_message['To'])[0],
                        'to_mail': email.utils.parseaddr(email_message['To'])[1],
                        'message-id': email.utils.parseaddr(email_message['Message-ID'])[1],
                        'from': email_message['From'],
                        'from_name': email.utils.parseaddr(email_message['From'])[0],
                        'from_mail': email.utils.parseaddr(email_message['From'])[1],
                        'date': email.utils.parsedate_to_datetime(email_message['Date']),
                        'subject': email_message['Subject'],
                        'user': self.imap_user,
                        'pass': self.imap_pass,
                        'body': body,
                        'proxy_host': self.proxy_host,
                        'proxy_port': self.proxy_port,
                        'proxy_user': self.proxy_user,
                        'proxy_pass': self.proxy_pass,
                        'FIRSTFROMNAME': self.FIRSTFROMNAME,
                        'LASTFROMNAME': self.LASTFROMNAME,
                        'flag': item
                        }
                    # print(t_dict)
                    var.email_q.put(t_dict.copy())
                    total_email_downloaded += 1
                var.total_email+=1

            imap.close()
            imap.logout()
        except Exception as e:
            email_failed += 1
            print("error at Imap - {} - {}".format(self.name, e))
            self.logger.error("Error at downloading email - {} - {}".format(self.imap_user, e))
        finally:
            var.acc_finished+=1
            var.thread_open-=1


def main(group):
    global email_failed, total_email_downloaded
    email_failed = 0
    total_email_downloaded = 0
    for index, item in group.iterrows():
        if var.stop_download == True:
            break

        if item["PROXY:PORT"] != " ":
            proxy_host = item["PROXY:PORT"].split(':')[0]
            proxy_port = int(item["PROXY:PORT"].split(':')[1])
        else:
            proxy_host = ""
            proxy_port = ""

        proxy_type = socks.PROXY_TYPE_SOCKS5
        proxy_user = item["PROXY_USER"]
        proxy_pass = item["PROXY_PASS"]
        imap_user = item["EMAIL"]
        imap_pass = item["EMAIL_PASS"]
        name = item["EMAIL"]
        FIRSTFROMNAME = item["FIRSTFROMNAME"]
        LASTFROMNAME = item["LASTFROMNAME"]

        while var.thread_open >= var.limit_of_thread and var.stop_download == False:
            time.sleep(1)
        print(index, name, proxy_host, proxy_port, proxy_type, proxy_user, proxy_pass, imap_user, imap_pass, FIRSTFROMNAME, LASTFROMNAME)
        IMAP_(index, name, proxy_host, proxy_port, proxy_type, proxy_user, proxy_pass, imap_user, imap_pass, FIRSTFROMNAME, LASTFROMNAME).start()

    while var.thread_open!=0 and var.stop_download == False:
        time.sleep(1)
    alert(text='Total Email Downloaded : {}\nEmail Failed : {}\ncheck app.log'.\
                format(total_email_downloaded, email_failed), title='Alert', button='OK')
    print("Downloading finished")