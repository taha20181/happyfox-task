import unittest
from utils import authenticate
from fetch_emails import fetch_user_emails
from process_emails import get_emails, load_rules, evaluate_rule, perform_actions

class TestGmailAPI(unittest.TestCase):

    def setUp(self):
        self.service = authenticate()

    def test_fetch_inbox_emails(self):
        message_count = 5
        messages = fetch_user_emails(self.service, message_count)
        self.assertIsInstance(messages, list)
        self.assertGreaterEqual(len(messages), 0)

    def test_fetch_email_details(self):
        messages = get_emails()
        if messages:
            msg = messages[0]
            self.assertIsInstance(msg, dict)
            self.assertIn('id', msg)
        else:
            self.skipTest("No messages in inbox")

    def test_evaluate_rules(self):
        rules = load_rules('rules.json')
        rule = rules['rule_1']
        rules, apply_type = rule['cohorts'], rule['apply_type']
        messages = get_emails()
        matched_messages = evaluate_rule(messages, rules, apply_type)
        self.assertIsInstance(matched_messages, list)

    def test_perform_actions(self):
        rules = load_rules('rules.json')
        rule = rules['rule_1']
        rules, apply_type, actions = rule['cohorts'], rule['apply_type'], rule['actions']
        messages = get_emails()
        matched_messages = evaluate_rule(messages, rules, apply_type)
        for msg in matched_messages:
            perform_actions(self.service, msg['id'], actions)

if __name__ == '__main__':
    unittest.main()