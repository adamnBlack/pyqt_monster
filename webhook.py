import threading
import requests
from json import loads, dumps
import time
import var
import queue
import os, sys

logger = var.logging
logger.getLogger("requests").setLevel(var.logging.WARNING)


def override_where():
    """ overrides certifi.core.where to return actual location of cacert.pem"""
    # change this to match the location of cacert.pem
    return os.path.abspath(f"database/cacert.pem")


# is the program compiled?
if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where

    # delay importing until after where() has been replaced
    import requests.utils
    import requests.adapters

    # replace these variables in case these modules were
    # imported before we replaced certifi.core.where
    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()


class SendWebhook(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.threadID = None
        self.name = "SendReport"
        self.setDaemon(True)
        self.close = False

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        self.api_link = var.webhook_link
        self.logger = var.logging
        self.logger.getLogger("requests").setLevel(var.logging.WARNING)

    def run(self):
        print("Webhook Started...")

        while not self.close:
            dict_list = []

            while not var.webhook_q.empty():
                try:
                    dict_list.append(var.webhook_q.get().copy())
                except Exception as e:
                    print(f"Error at SendWebhook part 1 : {e}")
                    self.logger.error(f"Error at SendWebhook part 1 : {e}")

            if len(dict_list) > 0:
                dict_obj = {
                    "data": dict_list,
                    "data_len": len(dict_list)
                }

                try:
                    data = dumps(dict_obj).encode("utf-8")
                    data = loads(data)

                    result = requests.post(
                        self.api_link, json=data, headers=self.headers, timeout=10)

                    self.logger.info(
                        f"POSTed {dict_obj['data_len']} data to webhook")

                except Exception as e:
                    print(f"Error at SendWebhook part 2 : {e}")
                    self.logger.error(f"Error at SendWebhook part 2 : {e}")

            time.sleep(1)
        print("Webhook Finished.")

    def __repr__(self):
        return f"Thread: {self.name}"

    def __str__(self):
        pass

    def quit(self):
        self.close = True


class SendWebhook_Inbox(threading.Thread):
    def __init__(self, total_length):
        threading.Thread.__init__(self)
        self.threadID = None
        self.name = "SendReport_Inbox"
        self.setDaemon(True)
        self.close = False

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        self.api_link = var.webhook_link
        self.logger = var.logging
        self.logger.getLogger("requests").setLevel(var.logging.WARNING)
        self.total_length = total_length

    def run(self):
        global inbox_q
        print("Inbox Webhook Thread Started...")
        count = 0
        while not self.close:

            while not inbox_q.empty():
                try:
                    temp = inbox_q.get().copy()
                except Exception as e:
                    print(f"Error at SendWebhook Inbox part 1 : {e}")
                    self.logger.error(
                        f"Error at SendWebhook Inbox part 1 : {e}")

                try:
                    dict_obj = {
                        "data": temp,
                        "type": "Inbox_Data"
                    }
                    data = dumps(dict_obj).encode("utf-8")
                    data = loads(data)

                    result = requests.post(
                        self.api_link, json=data, headers=self.headers, timeout=10)

                    count += 1

                    var.command_q.put(
                        f'GUI.label_email_status.setText("Total email sent - {count}/{self.total_length}")')

                except Exception as e:
                    print(f"Error at SendWebhook Inbox part 2 : {e}")
                    self.logger.error(
                        f"Error at SendWebhook Inbox part 2 : {e}")

            time.sleep(1)
        print("Webhook Inbox Thread Finished.")

    def __repr__(self):
        return f"Thread: {self.name}"

    def __str__(self):
        pass

    def quit(self):
        self.close = True


inbox_q = queue.Queue()


def start_inbox_stream():
    global inbox_q, logger
    try:
        print("Inbox Webhook Func started...")

        temp_df = var.inbox_data.copy()

        temp_df = temp_df[temp_df['checkbox_status'] == 1]

        total_email_count = len(temp_df)

        webhook = SendWebhook_Inbox(total_email_count)
        webhook.start()

        temp_df = temp_df.to_dict('records').copy()

        for item in temp_df:
            temp = item.copy()
            temp["date"] = str(temp["date"])
            inbox_q.put(temp.copy())

        while not inbox_q.empty():
            time.sleep(1)

        time.sleep(5)
        webhook.quit()
        var.command_q.put("GUI.label_email_status.setText('Email Webhook Firing Done.')")
        print("Inbox Webhook Func Finished.")

    except Exception as e:
        logger.error(
            f"Error at SendWebhook Inbox func : {e}")

        print(f"Error at SendWebhook Inbox func : {e}")
