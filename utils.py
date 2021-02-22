import re
import var
import random
import json
from pyautogui import alert, password, confirm

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
        data =  {
                    "config":
                    {
                        "date": var.date,
                        "num_emails_per_address": var.num_emails_per_address,
                        "delay_between_emails": var.delay_between_emails,
                        "limit_of_thread": var.limit_of_thread,
                        "compose_email_subject": var.compose_email_subject,
                        "compose_email_body": var.compose_email_body,
                        "login_email": var.login_email
                    }
                }
        with open(var.base_dir+'/config.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print("config updated")
    except Exception as e:
        print("Exeception occured at update_config_json : {}".format(e))
        alert(text="Exeception occured at update_config_json : {}".format(e), 
                                title='Alert', button='OK')

def format_email(text, FIRSTFROMNAME, LASTFROMNAME, one, two, three, TONAME):
    text = text.replace('[FIRSTFROMNAME]', str(FIRSTFROMNAME))
    text = text.replace('[LASTFROMNAME]', str(LASTFROMNAME))
    text = text.replace('[1]', str(one))
    text = text.replace('[2]', str(two))
    text = text.replace('[3]', str(three))
    text = text.replace('[TONAME]', str(TONAME))

    result = re.findall(r'\{.*?\}',text)

    for item in result:
        temp = item[1:-1]
        temp = random.choice(temp.split("|"))
        text = text.replace(item, temp)

    return text


if __name__ == "__main__":
    print(__name__)
    print(format_email(var.compose_email_body, 'a', 'b', 'c', 'd', 'e'))
    print(format_email(var.compose_email_subject, 'a', 'b', 'c', 'd', 'e'))