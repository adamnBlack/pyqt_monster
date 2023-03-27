import smtplib
import traceback
from proxy_smtplib import SMTP
from var import logger
import var


class SmtpBase:
    def __init__(self, **kwargs):
        super().__init__()

        self.proxy_host = kwargs["proxy_host"]
        self.proxy_port = kwargs["proxy_port"]
        self.proxy_user = kwargs["proxy_user"]
        self.proxy_pass = kwargs["proxy_pass"]
        self.proxy_type = kwargs["proxy_type"]
        self.user = kwargs["user"]
        self.passwd = kwargs["password"]
        self.first_from_name = kwargs["FIRSTFROMNAME"]
        self.last_from_name = kwargs["LASTFROMNAME"]
        self.smtp_server = kwargs['smtp_server']
        self.smtp_port = kwargs['smtp_port']
        self.local_hostname = None

    def _login(self):
        try:
            if var.add_custom_hostname:
                self.local_hostname = f"{self.first_from_name}-pc"

            if self.proxy_host != "":
                server = SMTP(
                    timeout=30, local_hostname=self.local_hostname
                )
                server.connect_proxy(host=self.smtp_server, port=self.smtp_port,
                                     proxy_host=self.proxy_host, proxy_port=int(self.proxy_port),
                                     proxy_type=self.proxy_type, proxy_user=self.proxy_user,
                                     proxy_pass=self.proxy_pass)

            else:
                server = smtplib.SMTP(var.smtp_server, var.smtp_port)
                # server.set_debuglevel(0)

            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.user, self.passwd)

            return server

        except Exception as e:
            logger.error(f"Error at {self.__class__.__name__}._login: {e}\n{traceback.format_exc()}")

            raise