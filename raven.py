"""This modules sends summary emails.
"""
from __future__ import print_function
import time 
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from report import report

TEXT = """
Current Cone Cache
------------------

{report}
"""

HTML = """
<html>
  <head></head>
  <body>
    <h2>Current Cone Cache</h2>
{report}
  </body>
</html>
"""

def send(trans):
    """Sends an email to the list.
    """
    me = "raven@pyne.io"
    you = "scopatz@gmail.com"
    today = datetime.date.today()

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Magic Cones Report - {0}'.format(today)
    msg['From'] = me
    msg['To'] = you

    # create content
    text = TEXT.format(report=report(trans))
    html = HTML.format(report=report(trans, html=True))
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    # Send the message
    s = smtplib.SMTP('localhost')
    s.sendmail(me, you, msg.as_string())
    s.quit()
