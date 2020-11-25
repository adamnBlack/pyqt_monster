import re
import var
import random
import json

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