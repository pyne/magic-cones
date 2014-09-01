#!/bin/bash
git pull -f
#python -m smtpd -n -c SMTPServer localhost:25 &
./magic-cones.py --update --drop --decay --email --gh-user pyne-dev
