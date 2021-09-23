import re
import var
import random
import json
from pyautogui import alert, password, confirm
import uuid


def difference_between_time(first_time, last_time):
    difference = last_time - first_time
    seconds_in_day = 24 * 60 * 60
    minutes, seconds = divmod(
        difference.days * seconds_in_day + difference.seconds, 60)
    elapsed_time = round(minutes + (seconds/60), 2)
    return elapsed_time


def prepare_html(body):
    # print(body)
    mails = re.findall('[\w\.-]+@[\w\.-]+\.\w+', body)
    urls = re.findall('https?://[^\s<>"]+|www\.[^\s<>"]+', body)
    for item in urls:
        try:
            a_tag = '<a href="{}">{}</a>'.format(item, item)
            if "<{}>".format(item) in body:
                body = body.replace("<{}>".format(item), a_tag)
            else:
                body = body.replace(" {}".format(item), " " + a_tag)
                body = body.replace("\n{}".format(item), "\n" + a_tag)
        except:
            pass

    for item in mails:
        try:
            a_tag = ' <a href="mailto:{}">{}</a>'.format(item, item)
            body = body.replace(" {}".format(item), a_tag)

        except:
            pass
    body = body.replace("\n", '<br>')
    # print(body)
    html = """<!doctype html>

            <html lang="en">
            <head>
            <meta charset="utf-8">

            <title>The HTML5 Herald</title>
            <meta name="description" content="The HTML5 Herald">
            <meta name="author" content="SitePoint">


            </head>

            <body>
            <p>{}</p>
            
            </body>
            </html>""".format(body)

    return html


def update_config_json():
    try:
        data = {
            "config":
            {
                "date": var.date,
                "num_emails_per_address": var.num_emails_per_address,
                "delay_between_emails": var.delay_between_emails,
                "limit_of_thread": var.limit_of_thread,
                "compose_email_subject": var.compose_email_subject,
                "compose_email_body": var.compose_email_body,
                "compose_email_body_html": var.compose_email_body_html,
                "login_email": var.login_email,
                "tracking": var.tracking,
                "webhook_link": var.webhook_link,
                "check_for_blocks": var.check_for_blocks,
                "target_blacklist": var.target_blacklist
            }
        }
        with open(var.base_dir+'/config.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print("config updated")
    except Exception as e:
        print("Exeception occured at update_config_json : {}".format(e))
        alert(text="Exeception occured at update_config_json : {}".format(e),
              title='Alert', button='OK')


def format_email(text, FIRSTFROMNAME, LASTFROMNAME, one, two, three, four, five, six, TONAME, source=None):
    text = text.replace('[FIRSTFROMNAME]', str(FIRSTFROMNAME))
    text = text.replace('[LASTFROMNAME]', str(LASTFROMNAME))
    text = text.replace('[1]', str(one))
    text = text.replace('[2]', str(two))
    text = text.replace('[3]', str(three))
    text = text.replace('[4]', str(four))
    text = text.replace('[5]', str(five))
    text = text.replace('[6]', str(six))
    text = text.replace('[TONAME]', str(TONAME))

    if var.body_type == "Html" and var.email_tracking_state == True and source != None:
        text = text.split("</body>")
        text[0] = text[0] + f"<img src='{var.email_tracking_link()}'></body>"
        text = "".join(text)
        rid = uuid.uuid4()
        # print(rid)
        text = text.replace('[**RID**]', str(rid))
        # print(text)

    result = re.findall(r'\{.*?\}', text)

    for item in result:
        temp = item[1:-1]
        temp = random.choice(temp.split("|"))
        text = text.replace(item, temp)

    if var.body_type == "Html":
        text = text.replace('[LINEBREAK]', "<br>")  # replace linebreaks with
    else:
        text = text.replace('[LINEBREAK]', "\n")

    return text


if __name__ == "__main__":
    print(__name__)
    print(format_email(var.compose_email_body, 'a', 'b', 'c', 'd', 'e'))
    print(format_email(var.compose_email_subject, 'a', 'b', 'c', 'd', 'e'))
