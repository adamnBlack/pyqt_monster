import re
import var
from var import logger
import random
import json
from pyautogui import alert
import uuid


def random_boolean(percent=50):
    return random.randrange(100) < percent


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def difference_between_time(first_time, last_time):
    difference = last_time - first_time
    seconds_in_day = 24 * 60 * 60
    minutes, seconds = divmod(
        difference.days * seconds_in_day + difference.seconds, 60)
    elapsed_time = round(minutes + (seconds/60), 2)
    return elapsed_time


def prepare_html(body):
    # print(body)
    mails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', body)
    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', body)
    for item in urls:
        try:
            a_tag = f'<a href="{item}">{item}</a>'
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


def update_config_json(alternative_name=None):
    try:
        data = {
            "config":
            {
                "mail_server": var.mail_server,
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
                "remove_email_from_target": var.remove_email_from_target,
                "enable_webhook": var.enable_webhook_status,
                "enable_email_tracking": var.email_tracking_state,
                "custom_hostname": var.add_custom_hostname,
                "campaign_group": var.campaign_group,
                "body_type": var.body_type,
                "target_blacklist": var.target_blacklist,
                "inbox_blacklist": var.inbox_blacklist,
                "inbox_whitelist": var.inbox_whitelist,
                "responses_webhook_enabled": var.responses_webhook_enabled,
                "auto_fire_responses_webhook": var.auto_fire_responses_webhook,
                "auto_fire_responses_webhook_interval": var.auto_fire_responses_webhook_interval,
                "followup_enabled": var.followup_enabled,
                "followup_days": var.followup_days,
                "followup_subject": var.followup_subject,
                "followup_body": var.followup_body,
                "hostname_list": var.hostname_list,
                "inbox_whitelist_checkbox": var.inbox_whitelist_checkbox,
                "space_encoding_checkbox": var.space_encoding_checkbox,
                "test_email": var.test_email,
                "airtable": {
                    "api_key": var.AirtableConfig.api_key,
                    "base_id": var.AirtableConfig.base_id,
                    "table_name": var.AirtableConfig.table_name,
                    "use_desktop_id": var.AirtableConfig.use_desktop_id,
                    "mark_sent_airtable": var.AirtableConfig.mark_sent_airtable,
                    "continuous_loading": var.AirtableConfig.continuous_loading,
                    "continuous_loading_time_period": var.AirtableConfig.continuous_loading_time_period
                }
            }
        }
        if alternative_name:
            with open(var.campaign_scheduler_cache_path+f'/{alternative_name}.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)
            logger.info("Scheduler Campaign config saved")
        else:
            with open(var.config_file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            logger.info("config updated")
    except Exception as e:
        logger.error("Exception occurred at update_config_json : {}".format(e))
        alert(text="Exception occurred at update_config_json : {}".format(e),
              title='Alert', button='OK')


def get_config_json():
    data = {
            "config":
            {
                "mail_server": var.mail_server,
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
                "remove_email_from_target": var.remove_email_from_target,
                "enable_webhook": var.enable_webhook_status,
                "enable_email_tracking": var.email_tracking_state,
                "custom_hostname": var.add_custom_hostname,
                "campaign_group": var.campaign_group,
                "body_type": var.body_type,
                "target_blacklist": var.target_blacklist,
                "inbox_blacklist": var.inbox_blacklist,
                "inbox_whitelist": var.inbox_whitelist,
                "responses_webhook_enabled": var.responses_webhook_enabled,
                "auto_fire_responses_webhook": var.auto_fire_responses_webhook,
                "auto_fire_responses_webhook_interval": var.auto_fire_responses_webhook_interval,
                "followup_enabled": var.followup_enabled,
                "followup_days": var.followup_days,
                "followup_subject": var.followup_subject,
                "followup_body": var.followup_body,
                "hostname_list": var.hostname_list,
                "inbox_whitelist_checkbox": var.inbox_whitelist_checkbox,
                "space_encoding_checkbox": var.space_encoding_checkbox,
                "test_email": var.test_email,
                "airtable": {
                    "api_key": var.AirtableConfig.api_key,
                    "base_id": var.AirtableConfig.base_id,
                    "table_name": var.AirtableConfig.table_name,
                    "use_desktop_id": var.AirtableConfig.use_desktop_id,
                    "mark_sent_airtable": var.AirtableConfig.mark_sent_airtable,
                    "continuous_loading": var.AirtableConfig.continuous_loading,
                    "continuous_loading_time_period": var.AirtableConfig.continuous_loading_time_period
                }
            }
        }
    return data


# def format_email(text, FIRSTFROMNAME, LASTFROMNAME, one, two, three, four, five, six, TONAME, source=None):
#     text = text.replace('[FIRSTFROMNAME]', str(FIRSTFROMNAME))
#     text = text.replace('[LASTFROMNAME]', str(LASTFROMNAME))
#     text = text.replace('[1]', str(one))
#     text = text.replace('[2]', str(two))
#     text = text.replace('[3]', str(three))
#     text = text.replace('[4]', str(four))
#     text = text.replace('[5]', str(five))
#     text = text.replace('[6]', str(six))
#     text = text.replace('[TONAME]', str(TONAME))
#
#     if var.body_type == "Html" and var.email_tracking_state is True and source is not None:
#         text = text.split("</body>")
#         text[0] = text[0] + f"<img src='{var.email_tracking_link()}'></body>"
#         text = "".join(text)
#         rid = uuid.uuid4()
#         text = text.replace('[**RID**]', str(rid))
#
#     result = re.findall(r'\{.*?\}', text)
#
#     for item in result:
#         temp = item[1:-1]
#         temp = random.choice(temp.split("|"))
#         text = text.replace(item, temp)
#
#     if var.body_type == "Html":
#         text = text.replace('[LINEBREAK]', "<br>\n")  # replace linebreaks with
#     else:
#         text = text.replace('[LINEBREAK]', "\n")
#
#     if var.space_encoding_checkbox:
#         if random_boolean():
#             text = text.replace(" ", random.choice(var.CONFUSABLES_CHARACTER))
#
#     return text

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

    if var.body_type == "Html" and var.email_tracking_state is True and source is not None:
        text = text.split("</body>")
        text[0] = text[0] + f"<img src='{var.email_tracking_link()}'></body>"
        text = "".join(text)
        rid = uuid.uuid4()
        text = text.replace('[**RID**]', str(rid))

    # Regex to find nested spintax brackets
    # spintax_bracket = re.compile(r'(?<!\\)((?:\\{2})*)\{([^{}]+)(?<!\\)((?:\\{2})*)\}')
    spintax_bracket = re.compile(r'(?<!\\)((?:\\{2})*)\{([^{}]*)(?<!\\)((?:\\{2})*)\}')

    # Define the regex pattern for non-nested spintax
    non_nested_spintax_pattern = re.compile(r'(?<!\{)\{([^{}]*?)(?:\|([^{}]*?))*\}(?!\})')
    non_nested_spintax_pattern = re.compile(r'\{[^{}]*?(?:\|[^{}]*?)*\}')
    nested_braces_pattern = r"\{[^{}]*\{.*?\}[^{}]*\}"

    # To keep track of used sentences
    used_sentences = set()

    def _replace_spintax(match):
        prefix, options, suffix = match.groups()
        options_list = options.split("|")

        # Filter out already used sentences
        available_options = [option for option in options_list if option not in used_sentences]

        if available_options:
            chosen_option = random.choice(available_options)
            used_sentences.add(chosen_option)  # Mark the chosen option as used
            return prefix + chosen_option + suffix
        else:
            # If all options are used, fallback to a random choice (but this shouldn't normally happen)
            return prefix + random.choice(options_list) + suffix

    # Process nested spintax iteratively
    while True:
        new_text = re.sub(spintax_bracket, _replace_spintax, text)
        text = new_text
        if is_non_nested_spintax(new_text):
            # Find all spintax placeholders
            result = re.findall(r'\{.*?\}', new_text)

            used_sentences_in_non_nested = set()  # To keep track of used sentences

            for item in result:
                temp = item[1:-1].split("|")  # Split options into a list
                # Filter out already used sentences
                available_options = [option for option in temp if option not in used_sentences_in_non_nested]

                if available_options:  # Check if there are any available options left
                    chosen_option = random.choice(available_options)  # Select one option
                    used_sentences_in_non_nested.add(chosen_option)  # Mark this option as used
                    text = text.replace(item, chosen_option, 1)  # Replace only the first occurrence
            break
        # if new_text == text:
        #     break
        # text = new_text

    # Replaces escaped characters (e.g., \{, \}, \|) with their literal counterparts
    text = re.sub(r'\\([{}|])', r'\1', text)
    # Removes double backslashes
    text = re.sub(r'\\{2}', r'\\', text)

    if var.body_type == "Html":
        text = text.replace('[LINEBREAK]', "<br>\n")  # replace linebreaks with
    else:
        text = text.replace('[LINEBREAK]', "\n")

    if var.space_encoding_checkbox:
        if random_boolean():
            text = text.replace(" ", random.choice(var.CONFUSABLES_CHARACTER))

    return text


def is_non_nested_spintax(input_string):
    # Regex to detect nested braces
    nested_braces_pattern = r"\{[^{}]*\{.*?\}[^{}]*\}"
    # Regex to detect non-nested spintax
    non_nested_spintax_pattern = r"\{([^\{\}]+)\}"

    # Check for nested spintax (invalid case)
    if re.search(nested_braces_pattern, input_string):
        return False
    # Check if the string has valid spintax or is a normal string
    # If it matches non-nested spintax or contains no braces, it's valid
    if re.search(non_nested_spintax_pattern, input_string) or '{' not in input_string:
        return True
    # Otherwise, the string is invalid
    return False

if __name__ == "__main__":
    print(__name__)
    print(format_email(var.compose_email_body, 'a', 'b', 'c', 'd', 'e'))
    print(format_email(var.compose_email_subject, 'a', 'b', 'c', 'd', 'e'))
