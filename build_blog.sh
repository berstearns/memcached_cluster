#!/bin/bash

source .env
TARGET_DIR=personal-notes
git -C $TARGET_DIR pull || git clone https://github.com/berstearns/personal-notes $TARGET_DIR
