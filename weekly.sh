#!/bin/bash
git pull -f
./magic-cones.py --update --drop --decay --email --gh-user pyne-dev
git commit -am "magic update at $(date)"
git push origin master
