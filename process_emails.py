from sqlalchemy import exc
from datetime import datetime, timedelta
import json

from database import SessionLocal
from models import Email
from utils import query_db, authenticate


def perform_actions(service, message_id, actions):
    for action in actions:
        body = evaluate_action(action)
        try:
            service.users().messages().modify(
                userId='me', id=message_id, body=body).execute()
            print("Email updated")
        except:
            print("Error while updating the email")
            continue
    

def evaluate_condition(message, field_name, condition, value):
    fields_map = {
        "FROM" : "from_email",
        "TO" : "to_email",
        "SUBJECT" : "subject",
        "DATE" : "date"
    }
    field = fields_map[field_name]
    if field_name == 'DATE':
        if condition == 'IS_LESS_THAN':
            return message[field].date() > (datetime.now() - timedelta(days=value)).date()

        if condition == 'IS_GREATER_THAN':
            return message[field].date() < (datetime.now() - timedelta(days=value)).date()
    else:
        value = value.lower()
        message = message[field].lower()
        if condition == 'CONTAINS':
            return value in message

        if condition == 'NOT_CONTAINS':
            return value not in message
        
        if condition == 'EQUALS':
            return value == message

        if condition == 'NOT_EQUALS':
            return value != message


def evaluate_action(action):
    if action['type'] == 'MARK_READ':
        return {
            'removeLabelIds' : [action['label']]
        }
    if action['type'] == 'MARK_UNREAD':
        return {
            'addLabelIds' : [action['label']]
        }
    if action['type'] == 'MOVE':
        return {
            'addLabelIds' : [action['label']]
        }


def evaluate_rule(emails, rules, apply_type):
    message_ids = []
    for email in emails:
        condition_set = []
        for r in rules:
            condition_set.append(
                evaluate_condition(
                    email, 
                    r['field'], 
                    r['condition'], 
                    r['value'])
                )
        
        if apply_type == 'all':
            flag = all(condition_set)
        else:
            flag = any(condition_set)

        if flag:
            message_ids.append(email['message_id'])

    return message_ids


def get_emails():
    records = query_db(Email)
    emails = [
        {
            "id" : record.id,
            "message_id" : record.message_id,
            "subject" : record.subject,
            "labels" : record.labels,
            "from_email" : record.from_email,
            "to_email" : record.to_email,
            "date" : record.date,
        } for record in records
    ]

    return emails
    

def load_rules(file):
    with open(file, 'r') as f:
        rules = json.load(f)

    return rules

if __name__ == '__main__':
    service = authenticate()
    rules = load_rules('rules.json')
    emails = get_emails()
    
    rule = rules['rule_1']
    rules, apply_type, actions = rule['cohorts'], rule['apply_type'], rule['actions']
    message_ids = evaluate_rule(emails, rules, apply_type)
    
    for message_id in message_ids:
        print("Updating email : ", message_id)
        perform_actions(service, message_id, actions)