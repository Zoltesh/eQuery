"""
A test script to test sending a query result to email. Serves as a template. Follow these steps:
1. Create new folder under 'Tasks' and name it whatever descriptive name you want.
2. Create a new .py file with the same name as 'the Tasks' folder.
3. Paste all the code from this file into your new .py file.
4. Modify your new .py file's copied code to do the queries you want and format the email message
as needed.
5. Praise Brayden
"""
from datetime import datetime
import os
import logging
from emailer import Emailer
from queryer import Queryer

# Set up a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Create a file handler
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
now = datetime.now()
filename = now.strftime("%Y%m%d-%H%M%S.log")
handler = logging.FileHandler(os.path.join(log_dir, filename))

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(handler)


def get_query_result():
    """
    Run query(ies) and return the results. You'll need to implement your own custom logic for
    returning the output as needed.
    :return:
    """
    q = Queryer()
    query = ("SELECT TOP 10 *"
             "FROM MyTable")
    result = q.execute_query(query=query)
    return result


def convert_to_message():
    """
    Convert specific query results to specific message. You'll need to implement your own
    custom logic to convert the results into a message.
    :return:
    """
    query_result = get_query_result()
    message = query_result
    return message


def send_query_result_to_email(recipients, subject, body):
    """
    Final action to send results to email
    :param recipients: List of emails to send to
    :param subject: Subject of the email
    :param body: Body of the email, derived from query results
    :return:
    """
    e = Emailer()
    e.send_email(recipients=recipients, subject=subject, body=body)


if __name__ == '__main__':
    # Provide the list of emails that it needs to send to and customize subject/body as needed.
    R = ['email@someemail.com']
    S = 'Test subject'
    B = convert_to_message()
    send_query_result_to_email(recipients=R, subject=S, body=B)
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)
