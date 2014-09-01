"""This modules sends summary emails.
"""
from __future__ import print_function
import os
import time 
import datetime
import smtplib
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from report import report
from lawyer import rules

TEXT = """
Current Cone Cache
------------------
Ley line of credit for each player:

{report}

Rules
-----

{rules}
"""

HTML = """
<html>
  <head></head>
  <body>
    <h2>Current Cone Cache</h2>
      Ley line of credit for each player:<br/><br/>
{report}
    <hr/>
    <h2>Rules</h2>
{rules}
  </body>
</html>
"""

def passwd(user):
    fname = '{0}.pw'.format(user.split('@', 1)[0])
    if not os.path.isfile(fname):
        pw = getpass('password for {0}:'.format(user))
        with open(fname, 'w') as f:
            f.write(pw)
    with open(fname, 'r') as f:
        pw = f.read()
    return pw

def send(trans):
    """Sends an email to the list."""
    me = 'pyne.raven@gmail.com'
    you = 'scopatz@gmail.com'
    today = datetime.date.today()

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Magic Cones Report {0}'.format(today)
    msg['From'] = me
    msg['To'] = you

    # create content
    text = TEXT.format(report=report(trans), rules=rules())
    html = HTML.format(report=report(trans, html=True), rules=rules(html=True))
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    # Send the message
    pw = passwd(me)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    #s.ehlo()
    s.starttls()
    #s.ehlo()
    s.login(me, pw)
    s.sendmail(me, you, msg.as_string())
    s.quit()
