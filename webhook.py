import threading
import requests
from json import loads, dumps
import time
import var


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
        while self.close != True:
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
        print(f"Thread: {self.name}")

    def __str__(self):
        pass

    def quit(self):
        self.close = True
