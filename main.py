"""
A simple program to query a database and send emails about them
"""
from emailer import Emailer


def main():
    recipients = ['brayden@falconfulfillment.com']
    e = Emailer()
    e.send_email(recipients=recipients, subject='test', body='test')


if __name__ == '__main__':
    main()
