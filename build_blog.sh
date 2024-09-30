#!/bin/bash

source .env
while 1;do
    echo 'sleeping for 30 seconds'
    sleep 30
    echo 'rendering'
    TARGET_DIR=personal-notes
    git -C $TARGET_DIR pull || git clone https://$GIT_USERNAME:$GIT_PASSWORD@github.com/berstearns/personal-notes $TARGET_DIR
    pip install -r personal-notes/blog/requirements.txt
    python3 personal-notes/blog/render.py
    clear
done
